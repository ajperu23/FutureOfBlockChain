import random
import time
import msgpack
import json

from nucypher.data_sources import DataSource

# Alice defined a label to chat
# All DataSources that produce this type of data will use this label.

def generate_message(policy_pubkey,  msg_data, username, label):

    data_source = DataSource(policy_pubkey_enc=policy_pubkey,
                             label=label)

    data_source_public_key = bytes(data_source.stamp)

    now = time.time()

    kits = list()

    user_input = {
        'name' : username,
        'msg': msg_data,
        'timestamp': now,
    }

    plaintext = msgpack.dumps(user_input, use_bin_type=True)
    message_kit, _signature = data_source.encrypt_message(plaintext)

    kit_bytes = message_kit.to_bytes()
    kits.append(kit_bytes)

    data = {
        'data_source': data_source_public_key,
        'kits': kits,
    }

    final_msg = msgpack.dumps(data, use_bin_type=True)

    return final_msg
