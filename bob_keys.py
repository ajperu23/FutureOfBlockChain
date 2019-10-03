import json
import os
from umbral.keys import UmbralPrivateKey, UmbralPublicKey

BOB_PUBLIC_JSON = 'bob.public.json'
BOB_PRIVATE_JSON = 'bob.private.json'


def generate_bob_keys():
    enc_privkey = UmbralPrivateKey.gen_key()
    sig_privkey = UmbralPrivateKey.gen_key()

    bob_privkeys = {
        'enc': enc_privkey.to_bytes().hex(),
        'sig': sig_privkey.to_bytes().hex(),
    }

    with open(BOB_PRIVATE_JSON, 'w') as f:
        json.dump(bob_privkeys, f)

    enc_pubkey = enc_privkey.get_pubkey()
    sig_pubkey = sig_privkey.get_pubkey()
    bob_pubkeys = {
        'enc': enc_pubkey.to_bytes().hex(),
        'sig': sig_pubkey.to_bytes().hex()
    }
    with open(BOB_PUBLIC_JSON, 'w') as f:
        json.dump(bob_pubkeys, f)


def _get_keys(file, key_class):
    if not os.path.isfile(file):
        generate_bob_keys()

    with open(file) as f:
        stored_keys = json.load(f)
    keys = dict()
    for key_type, key_str in stored_keys.items():
        keys[key_type] = key_class.from_bytes(bytes.fromhex(key_str))
    return keys


def get_bob_pubkeys():
    return _get_keys(BOB_PUBLIC_JSON, UmbralPublicKey)


def get_bob_privkeys():
    return _get_keys(BOB_PRIVATE_JSON, UmbralPrivateKey)
