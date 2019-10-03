from nucypher.characters.lawful import Bob, Ursula
from nucypher.config.characters import AliceConfiguration
from nucypher.config.storages import LocalFileBasedNodeStorage
from nucypher.crypto.powers import DecryptingPower, SigningPower
from nucypher.network.middleware import RestMiddleware
from nucypher.utilities.logging import SimpleObserver

import datetime
import os
import shutil
import maya
import json
import sys
from twisted.logger import globalLogPublisher


POLICY_FILENAME = "policy-metadata.json"

######################
# Boring setup stuff #
######################
#
# # Twisted Logger
globalLogPublisher.addObserver(SimpleObserver())
#
TEMP_ALICE_DIR = "alice-files".format(os.path.dirname(os.path.abspath(__file__)))

# We expect the url of the seednode as the first argument.
SEEDNODE_URL = '146.169.192.138:11500'


#######################################
# Alicia, the Authority of the Policy #
#######################################


# We get a persistent Alice.
# If we had an existing Alicia in disk, let's get it from there

passphrase = "TEST_ALICE_INSECURE_DEVELOPMENT_PASSWORD"
# trying to create our own alice

# If anything fails, let's create Alicia from scratch
# Remove previous demo files and create new ones

shutil.rmtree(TEMP_ALICE_DIR, ignore_errors=True)

ursula = Ursula.from_seed_and_stake_info(seed_uri=SEEDNODE_URL,
                                         federated_only=True,
                                         minimum_stake=0)

alice_config = AliceConfiguration(
    config_root=os.path.join(TEMP_ALICE_DIR),
    is_me=True,
    known_nodes={ursula},
    start_learning_now=False,
    federated_only=True,
    learn_on_same_thread=True,
)

alice_config.initialize(password=passphrase)

alice_config.keyring.unlock(password=passphrase)
alice = alice_config.produce()

# We will save Alicia's config to a file for later use
alice_config_file = alice_config.to_configuration_file()

# Let's get to learn about the NuCypher network
alice.start_learning_loop(now=True)

# At this point, Alicia is fully operational and can create policies.
# The Policy Label is a bytestring that categorizes the data that Alicia wants to share.
# Note: we add some random chars to create different policies, only for demonstration purposes
label = "chat"+os.urandom(4).hex()
label = label.encode()

# Alicia can create the public key associated to the policy label,
# even before creating any associated policy.
policy_pubkey = alice.get_policy_pubkey_from_label(label)

print("The policy public key for "
      "label '{}' is {}".format(label.decode("utf-8"), policy_pubkey.to_bytes().hex()))

# Data Sources can produce encrypted data for access policies
# that **don't exist yet**.
# In this example, we create a local file with encrypted data, containing
# heart rate measurements from a heart monitor


# Alicia now wants to share data associated with this label.
# To do so, she needs the public key of the recipient.
# In this example, we generate it on the fly (for demonstration purposes)
from bob_keys import get_bob_pubkeys
bob_pubkeys = get_bob_pubkeys()

powers_and_material = {
    DecryptingPower: bob_pubkeys['enc'],
    SigningPower: bob_pubkeys['sig']
}

# We create a view of the Bob who's going to be granted access.
bob_strange = Bob.from_public_keys(powers_and_material=powers_and_material,
                                      federated_only=True)

# Here are our remaining Policy details, such as:
# - Policy duration
policy_end_datetime = maya.now() + datetime.timedelta(days=5)
# - m-out-of-n: This means Alicia splits the re-encryption key in 5 pieces and
#               she requires Bob to seek collaboration of at least 3 Ursulas
m, n = 3, 5


# With this information, Alicia creates a policy granting access to Bob.
# The policy is sent to the NuCypher network.
print("Creating access policy for the Bob...")
policy = alice.grant(bob=bob_strange,
                      label=label,
                      m=m,
                      n=n,
                      expiration=policy_end_datetime)
print("Done!")


# For the demo, we need a way to share with Bob some additional info
# about the policy, so we store it in a JSON file
policy_info = {
    "policy_pubkey": policy.public_key.to_bytes().hex(),
    "alice_sig_pubkey": bytes(alice.stamp).hex(),
    "label": label.decode("utf-8"),
}

filename = POLICY_FILENAME
with open(filename, 'w') as f:
    json.dump(policy_info, f)

