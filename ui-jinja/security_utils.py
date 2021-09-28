#!/usr/bin/env python
# -*- coding: utf-8 -*-
# the above line is to avoid 'SyntaxError: Non-UTF-8 code starting with' error

'''
Created on 

Course work: 

@author: raja

Source:
    
'''

# Import necessary modules
from flask_bcrypt import Bcrypt

import base64
import binascii

bcrypt = Bcrypt()

def hash_password(password):

    return bcrypt.generate_password_hash(password)

def match_password(db_password, password):

    return bcrypt.check_password_hash(db_password, password)

def encode_base(message):
    
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode_base(base64_message):

    try:
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
    except binascii.Error as e:
        print(e)

        return None

    return message