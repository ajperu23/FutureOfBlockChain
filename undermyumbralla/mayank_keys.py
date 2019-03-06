import json
import os
from umbral.keys import UmbralPrivateKey, UmbralPublicKey

MAYANK_PUBLIC_JSON = 'mayank.public.json'
MAYANK_PRIVATE_JSON = 'mayank.private.json'


def generate_mayank_keys():
    enc_privkey = UmbralPrivateKey.gen_key()
    sig_privkey = UmbralPrivateKey.gen_key()

    mayank_privkeys = {
        'enc': enc_privkey.to_bytes().hex(),
        'sig': sig_privkey.to_bytes().hex(),
    }

    with open(MAYANK_PRIVATE_JSON, 'w') as f:
        json.dump(mayank_privkeys, f)

    enc_pubkey = enc_privkey.get_pubkey()
    sig_pubkey = sig_privkey.get_pubkey()
    mayank_pubkeys = {
        'enc': enc_pubkey.to_bytes().hex(),
        'sig': sig_pubkey.to_bytes().hex()
    }
    with open(MAYANK_PUBLIC_JSON, 'w') as f:
        json.dump(mayank_pubkeys, f)


def _get_keys(file, key_class):
    if not os.path.isfile(file):
        generate_mayank_keys()

    with open(file) as f:
        stored_keys = json.load(f)
    keys = dict()
    for key_type, key_str in stored_keys.items():
        keys[key_type] = key_class.from_bytes(bytes.fromhex(key_str))
    return keys


def get_mayank_pubkeys():
    return _get_keys(MAYANK_PUBLIC_JSON, UmbralPublicKey)


def get_mayank_privkeys():
    return _get_keys(MAYANK_PRIVATE_JSON, UmbralPrivateKey)
