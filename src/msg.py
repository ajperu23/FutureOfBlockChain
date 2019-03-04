import random
import time
import msgpack

from nucypher.data_sources import DataSource


FILENAME = 'data.msgpack'

# Alicia defined a label to categorize all her heart-related data ❤️
# All DataSources that produce this type of data will use this label.
DEFAULT_LABEL = b"message"


def generate_message(policy_pubkey,  msg_data,
                                label: bytes = DEFAULT_LABEL):

    data_source = DataSource(policy_pubkey_enc=policy_pubkey,
                             label=label)

    data_source_public_key = bytes(data_source.stamp)

    # heart_rate = 80
    now = time.time()

    kits = list()
    # for _ in range(samples):
        # Simulated heart rate data
        # Normal resting heart rate for adults: between 60 to 100 BPM
    # heart_rate = random.randint(max(60, heart_rate-5),
                                # min(100, heart_rate+5))
    # now += 3

    # need to replace with user input
    user_input = {
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

    # if save_as_file:
    #     with open(FILENAME, "wb") as file:
    #         msgpack.dump(data, file, use_bin_type=True)

    return data
