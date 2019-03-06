
#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import msg 

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

import mayank_builder

mayank, policy_pubkey, arjuns_sig_pubkey, label = mayank_builder.generate_mayank()

first = True
receive_counter = 0
username = ""

def receive():
    """Handles receiving of messages."""
    global receive_counter
    while True:
        try:
            """receives msgpack"""
            data = client_socket.recv(BUFSIZ)
            if receive_counter < 2:
                data = data.decode("utf8")
                msg_list.insert(tkinter.END, data) #display on tkinter
            else:
                # print("receive:", data)
                # print(type(data))
                msg = mayank_builder.decrypting_msg(data, policy_pubkey, label, arjuns_sig_pubkey, mayank)
                msg_list.insert(tkinter.END, msg) #display on tkinter
            receive_counter += 1
            
        except OSError as e:  # Possibly client has left the chat.
            continue


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg_data = my_msg.get()
    global first
    global username

    if msg_data == "{quit}":
        client_socket.send(bytes("{quit}", "utf8"))
        client_socket.close()
        os._exit(0)
        top.quit()

    if first: # for the first message (user sends name)
        username = msg_data
        send_data = bytes(msg_data, "utf8")
        first = False
    else:
        send_data = msg.generate_message(policy_pubkey, msg_data, username, label)

    my_msg.set("")  # Clears input field.

    """sends the encryoted message as msgpack"""
    client_socket.send(send_data);

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("UnderMyUmbralla")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type ...")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
# HOST = input('Enter host: ')
HOST = "146.169.205.219"
PORT = 33000

BUFSIZ = 4096
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
