
import datetime
from datetime import timedelta

import jwt

def func_create_custom_token(payload):

    token=jwt.encode(payload, "dont tell anyone")
    token = token.decode("utf-8")
    return token

def func_decode_custom_token(encode_token):
    

    try:
        payload = jwt.decode(encode_token, "dont tell anyone")

        #validate decoded payload 
        if not(len(payload) == 2 and "userPhoneNumber" in payload 
            and len(payload["userPhoneNumber"]) > 2   
            and "userPassword" in payload 
            and len(payload["userPassword"])) > 2:
             return {"error":{"errorType":"apiInterfaceError", "errorMsg":"Access denied","errorDesc":"decoded payload is invalid"}}

    except Exception as e:
        payload = {
            "error":{
                "errorType":"apiInterfaceError",
                "errorMsg" :"Access denied",
                "errorDesc":str(e) 
            }
        }   
    
    return payload

def func_compare_token(to_token, from_token):

    if to_token == from_token:
        return True
    else:
        return False     





def func_get_time_diff(date1, date2=""):
    
    '''
       "date1": should be less than date date2
       "date2": should be more date1, if left blank then it will opt current date  
        
    '''
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    #    date1 = '2016-04-16 10:01:28.585'
    #   date2 = '2016-03-10 09:56:28.067'

    if date2 == "":
        date2 = str(datetime.datetime.now())

    diff = datetime.datetime.strptime(date2, datetimeFormat)\
        - datetime.datetime.strptime(date1, datetimeFormat)
    

    obj_diff = {"days"    : diff.days, 
                "hours"   : diff.total_seconds()/(60*60),
                "minutes" : diff.total_seconds()/(60),
                "seconds" : diff.total_seconds(),
                }

    return obj_diff

#print(func_get_time_diff('2020-03-10 09:56:28.067'))