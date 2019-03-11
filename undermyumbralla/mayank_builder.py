import json
import os
import sys
import shutil
import msgpack
import maya
import traceback
from timeit import default_timer as timer

from nucypher.characters.lawful import Bob, Ursula
from nucypher.crypto.kits import UmbralMessageKit
from nucypher.crypto.powers import DecryptingPower, SigningPower
from nucypher.data_sources import DataSource
from nucypher.keystore.keypairs import DecryptingKeypair, SigningKeypair
from nucypher.network.middleware import RestMiddleware

from umbral.keys import UmbralPublicKey

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SEEDNODE_URL = '146.169.192.138:11501'

TEMP_MAYANK_DIR = "{}/mayank-files".format(os.path.dirname(os.path.abspath(__file__)))

#Created this function to be able to attach this to the client side

# Remove previous demo files and create new ones

def generate_mayank():
    shutil.rmtree(TEMP_MAYANK_DIR, ignore_errors=True)

    ursula = Ursula.from_seed_and_stake_info(seed_uri=SEEDNODE_URL,
                                             federated_only=True,
                                             minimum_stake=0)

    # To create a Bob, we need the mayank's private keys previously generated.
    from mayank_keys import get_mayank_privkeys
    mayank_keys = get_mayank_privkeys()

    bob_enc_keypair = DecryptingKeypair(private_key=mayank_keys["enc"])
    bob_sig_keypair = SigningKeypair(private_key=mayank_keys["sig"])
    enc_power = DecryptingPower(keypair=bob_enc_keypair)
    sig_power = SigningPower(keypair=bob_sig_keypair)
    power_ups = [enc_power, sig_power]

    print("Creating the Mayank ...")

    mayank = Bob(
        is_me=True,
        federated_only=True,
        crypto_power_ups=power_ups,
        start_learning_now=True,
        abort_on_learning_error=True,
        known_nodes=[ursula],
        save_metadata=False,
        network_middleware=RestMiddleware(),
    )

    print("Mayank = ", mayank)

    # Join policy created by alice
    with open("policy-metadata.json", 'r') as f:
        policy_data = json.load(f)

    policy_pubkey = UmbralPublicKey.from_bytes(bytes.fromhex(policy_data["policy_pubkey"]))
    arjuns_sig_pubkey = UmbralPublicKey.from_bytes(bytes.fromhex(policy_data["arjun_sig_pubkey"]))
    label = policy_data["label"].encode()

    print("The Mayank joins policy for label '{}'".format(label.decode("utf-8")))
    mayank.join_policy(label, arjuns_sig_pubkey)

    return mayank, policy_pubkey, arjuns_sig_pubkey, label

# here we start decrypting the message

def decrypting_msg(data, policy_pubkey, label, arjuns_sig_pubkey, mayank):
    data = msgpack.loads(data, raw=False)
    print("afterjson", data)
    message_kits = (UmbralMessageKit.from_bytes(k) for k in data['kits'])

    # The mayank also needs to create a view of the Data Source from its public keys
    data_source = DataSource.from_public_keys(
            policy_public_key=policy_pubkey,
            datasource_public_key=data['data_source'],
            label=label
    )

    # NuCypher network to get a re-encrypted version of each MessageKit.
    for message_kit in message_kits:
        try:
            start = timer()
            retrieved_plaintexts = mayank.retrieve(
                message_kit=message_kit,
                data_source=data_source,
                alice_verifying_key=arjuns_sig_pubkey
            )
            end = timer()

            plaintext = msgpack.loads(retrieved_plaintexts[0], raw=False)

            msg = plaintext['msg']
            name = plaintext['name']
            timestamp = maya.MayaDT(plaintext['timestamp'])

            return (name+": "+msg+" ("+str(timestamp)+")")
            
        except Exception as e:
            traceback.print_exc()

