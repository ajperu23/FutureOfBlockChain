import json
import os
from umbral.keys import UmbralPrivateKey, UmbralPublicKey

CHARLIE_PUBLIC_JSON = 'charlie.public.json'
CHARLIE_PRIVATE_JSON = 'charlie.private.json'


def generate_charlie_keys():
    enc_privkey = UmbralPrivateKey.gen_key()
    sig_privkey = UmbralPrivateKey.gen_key()

    charlie_privkeys = {
        'enc': enc_privkey.to_bytes().hex(),
        'sig': sig_privkey.to_bytes().hex(),
    }

    with open(CHARLIE_PRIVATE_JSON, 'w') as f:
        json.dump(charlie_privkeys, f)

    enc_pubkey = enc_privkey.get_pubkey()
    sig_pubkey = sig_privkey.get_pubkey()
    charlie_pubkeys = {
        'enc': enc_pubkey.to_bytes().hex(),
        'sig': sig_pubkey.to_bytes().hex()
    }
    with open(CHARLIE_PUBLIC_JSON, 'w') as f:
        json.dump(charlie_pubkeys, f)


def _get_keys(file, key_class):
    if not os.path.isfile(file):
        generate_charlie_keys()

    with open(file) as f:
        stored_keys = json.load(f)
    keys = dict()
    for key_type, key_str in stored_keys.items():
        keys[key_type] = key_class.from_bytes(bytes.fromhex(key_str))
    return keys


def get_charlie_pubkeys():
    return _get_keys(CHARLIE_PUBLIC_JSON, UmbralPublicKey)


def get_charlie_privkeys():
    return _get_keys(CHARLIE_PRIVATE_JSON, UmbralPrivateKey)
