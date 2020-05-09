from Appserver import SendEmail,send_sms
import datetime,os,sys
from datetime import timedelta


def func_SendOtp(obj_model,obj_doc):
    try:
        otp=""

        if "userEmail" in obj_doc:
            receiver_email = obj_doc["userEmail"]
            sender_email   = "gk.411995@gmail.com"
            password       = "12wedfvbabc"

            # logic for seeing whether email ID already exist for our other users or not 
            myQuery = {"userEmail":receiver_email}
            
            obj_model.find("USERS", myQuery, proj={"_id":1}, check=True, eMsg="user already exist with this emailId. Try another")
            
            otp            = generateOTP()
            result         = SendEmail.SendOtp(sender_email, receiver_email, password, otp)

            if result["status"] != "success":
                obj_model.obj_logs.menthod_log_error(
                    errorType="appserverError",
                    errorMsg="Something went wrong while sending email. Try again!!",
                    errorDesc=result
                )

        if "userPhoneNumber" in  obj_doc: 

            receiver_phone = obj_doc["userPhoneNumber"]
            #checking whether record exist or not
            
            if not("action" in obj_doc and obj_doc["action"] == "forgetPassword"):

                myQuery = {    "$and":
                    [
                        {
                            "userPhoneNumber":receiver_phone 
                        },
                        {
                            "userIpAddress":{"$exists": "true"}
                        }
                    ]
                }
                obj_model.find("USERS", myQuery, proj={"_id":1}, check=True, eMsg="User already exists with this phone number. Try another")

            #generating otp, sending messages
            otp     = generateOTP()
            
            result = send_sms.func_sendSms(receiver_phone, "Your otp is : " + otp)
            
            #if sending message fails then logging and returning
            if result["status"] != "success":
                obj_model.obj_logs.menthod_log_error(
                    errorType="appserverError",
                    errorMsg=result["message"],
                    errorDesc=result
                )

        #logic for storing and updating the otp with Ip address in OTPS collection in order to verify while doing sign up
        filter = obj_doc
        
        update = {"$set":{**obj_doc,"otp":otp, "lastModified":str(datetime.datetime.now())}}
        
        obj_model.update("OTPS",filter,update,upsert=True) 
        
        obj_model.obj_logs.method_log_success(
        success = {
            "Msg":"OTP Sent"
        })

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == 'ManualError': return 
        obj_model.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)    

# function to generate OTP 
def generateOTP() : 
    # import library 
    import math, random 
    # Declare a string variable   
    # which stores all string  
    string = '0123456789'
    OTP = "" 
    length = len(string) 
    for i in range(5) : 
        OTP += string[math.floor(random.random() * length)] 
        i=i
  
    return OTP 