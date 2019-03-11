# FutureOfBlockChain
Future of BlockChain Competition Entry

We managaed to create and end to end application which has the potential to message accross WAN. The idea is that there's a main server, which clients can connect to and send messages and the server controls all the information that's been sent and can see which clients are active. 

# Debug and Process
We began setting up virtual environments using python-env and then downloading NuCypher onto it, and bring the Git-Repo from NuCypher to try and plug and play with some of the demos. We configured our own Ursulas and managed to assign them to our own IP and set our own ports and then access them via web browsers.

Issues Encountered:

1) Response has not attribute "data" - potentially a wrong file or the methodology of sending the information is quite weak.
2) No response from teacher ursula when trying to connect them across the network
3) Multitude of install and dependecies errors, which shall be getting fixed.

# Requirements

Pip install nucypher into a virtual environment.
Pip install tkinter.
Python 3.6 is required. 

# Usage
Go to the undermyumbralla folder for all the files. Proceed with the following order on a command line.
Setup nucypher network by running a teacher ursula and a fleet of ursulas with IP addresses configured in the Python files. Run alice_and_policy_two.py to generate access to people in the group chat. Run the server with a given Host and Port. Run the client scripts to allow communication through the tkinter GUI. Press {quit} to quit the chat. 
