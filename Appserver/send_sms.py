import requests
import json

URL = 'https://www.sms4india.com/api/v1/sendCampaign'


# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)

# get response
def func_sendSms(phoneNumber,otp):
    response = sendPostRequest(URL, 
                            '0JB5NGUN31LOCPTB1ISJ5VQLY0JJ5O2F', 
                            'QSJJ67BN41YGBRJH', 
                            'stage', 
                             phoneNumber, 
                            'gk.411995@gmail.com', 
                             otp)
    """
    Note:-
        you must provide apikey, secretkey, usetype, mobile, senderid and message values
        and then requst to api
    """
    # print response if you want
    print("response",response.text)
    return dict(json.loads(response.text))

