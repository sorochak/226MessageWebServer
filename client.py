#!/usr/bin/env python3

import requests
import sys
import random
import string

KEYLENGTH = 8

PROMPT = 'Please Enter a Message: \n'


#
# PURPOSE:
# Generates and returns a random alphanumeric key of length KEYLENGTH
#
# RETURN
# Returns random alphanumeric key

def getRandKey():
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(KEYLENGTH))


#
# PURPOSE:
# Prompts the user for a message and returns the message
#
# RETURN
# Returns the user's message

def getUserMsg():
    usrMessage = input(PROMPT)
    return usrMessage


#
# PURPOSE:
# Given a host, port, and key, retrieves the message associated with the key from the
# host listening at the given port.  Should this message exist, extracts the next key
# from this message, then uses that key to get the next message.  
# This process is continued until no more messages are found.  
# At that point, the user is prompted for a new message, which is then stored on the server with a new key
# 
# PARAMETERS:
# 'host' contains the host IP or name
# 'port' contains the IP at which the host is listening
# 'key' contains the KEY_SIZE-byte alphanumeric key to be used to retrieve the first message
# 
# RETURN/SIDE EFFECTS:
# N/A
# 

def client(host, port, key):
    
        mostRecentKey = key
        while True:
            data = requests.get('http://127.0.0.1:8000/msgserver/get/' + mostRecentKey)

            print(data.content)

            if data.content != b'':
                mostRecentKey = data.content[:KEYLENGTH].decode()
                print('key: ' + mostRecentKey)
                message = data.content[KEYLENGTH:].decode()
                print('Message: ' + message)
                print('Data Content: ' + data.content.decode())

            else:
                client = requests.session()
                url = 'http://127.0.0.1:8000/msgserver/create/'
                client.get(url)
                newMsg = getUserMsg()
                sendMsg = getRandKey() + newMsg
                print(sendMsg)

                if 'csrftoken' in client.cookies:
                    elements = {'key':mostRecentKey, 'message':sendMsg, 'csrfmiddlewaretoken':client.cookies['csrftoken']}
                    post = client.post(url, data = elements, headers = {'Referer' : url})
                    
                break
           
if len(sys.argv) != 4:
    print(f'{sys.argv[0]} needs 3 argument to transmit')
    sys.exit(-1)

client(sys.argv[1], sys.argv[2], sys.argv[3])