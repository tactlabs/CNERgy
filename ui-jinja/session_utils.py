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

import datetime

# Local import
import date_utils
import security_utils
import web_utils


'''
    Session Format:
    ip_userid_expireat_salt

    IP Userid ExpireAt LocalSalt

    Sample:

'''

C13R_SALT           = "smite_me_oh_mighty_smiter"
EXPIRE_TIME_MINUTES = 20

VALID_SESSION      = 0
BROKEN_SESSION_ID  = 1
SESSION_EXPIRED    = 2
IP_MISMATCH        = 3
USERID_MISMATCH    = 4
INVALID_SESSION_ID = 5

def get_session_base(userid):
    
    # sessionid format: ip_userid_expireat_salt

    ip = web_utils.get_ip()
    current_time_millis = date_utils.get_current_time_millis()
    expire_time_millis = current_time_millis + (EXPIRE_TIME_MINUTES * 60 * 1000)

    session_base = ip + '_' + str(userid) + '_' + str(expire_time_millis) + '_' + C13R_SALT 
    session_base_end = security_utils.encode_base(session_base)

    return session_base_end

def validate_sessionid(sid):
    """
        Session Format:
        ip_userid_expireat_salt

        result:
        0 - valid session
        1 - broken session id
        2 - sessoin expired
        3 - ip mismatch
        4 - userid mismatch
        5 - invalid session id

    """

    if(sid is None):
        return False, INVALID_SESSION_ID

    decoded_session_id = security_utils.decode_base(sid)

    print('decoded_session_id : ', decoded_session_id)

    # 1 - broken session id
    if(not decoded_session_id):
        return False, BROKEN_SESSION_ID

    # 1 - broken session id
    if('_' not in decoded_session_id):
        return False, BROKEN_SESSION_ID

    session_parts = decoded_session_id.split('_')

    userid = int(session_parts[1])

    # 4 - userid mismatch
    # TODO: Please fix this later
    '''
    if(userid != SAMPLE_USERID):
        return False, USERID_MISMATCH
    '''

    session_userip = session_parts[0]

    # 3 - ip mismatch
    ip = web_utils.get_ip()
    if(session_userip != ip):
        return False, IP_MISMATCH

    # check session whether it is expired or not
    future_expire_millis = int(session_parts[2])
    current_time_millis = date_utils.get_current_time_millis()

    seconds_left = (future_expire_millis - current_time_millis) / 1000

    print('Time left in seconds : ', int(seconds_left))

    # 2 - sessoin expired
    if(seconds_left < 0):
        return False, SESSION_EXPIRED

    return True, VALID_SESSION


def created_sessionid(userid):

    return get_session_base(userid)

def get_userid_from_sid(sid):

    decoded_session_id = security_utils.decode_base(sid)

    session_parts = decoded_session_id.split('_')

    userid = int(session_parts[1])

    return userid
    

