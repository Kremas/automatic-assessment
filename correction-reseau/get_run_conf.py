#!/usr/bin/env python

import paramiko
import time
from getpass import getpass

# get conn informations / credentials
ip = input("IP address: ")
port = input("Port: ")
username = input("Username: ")
password = getpass()

# establish connection
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, port=port, username=username, password=password,
               look_for_keys=False, allow_agent=False
              )

# invoke remote shell
conn = client.invoke_shell()
output = conn.recv(65535)
print(output)

# send command and get output
# j'ai mis un cat d'un show run pcq j'ai pas de routeur/switch sous la main 
# donc je me co à mon rpi
conn.send("cat R2.txt\n")
time.sleep(1)
output = conn.recv(65535)
print(output)

with open("ouput.txt", "wb") as f:
    f.write(output)

