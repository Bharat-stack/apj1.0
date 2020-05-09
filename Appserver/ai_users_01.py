from Appserver import custom_func
import os,sys
def func_insert_user(obj_model,obj_doc):
    try:
    
        #checking whether record exist with the same userId in USERS table
        myQuery = {
            "userPhoneNumber":obj_doc["userPhoneNumber"]
        }
        
        #checking whether record exist or not
        obj_model.find("USERS", myQuery, proj={"_id":1}, check=True, eMsg="User already exist with this phone number. Try another")
        
        #Verifying OTP
        myQuery = {
            "userPhoneNumber":obj_doc["userPhoneNumber"],
            "userIpAddress":obj_doc["userIpAddress"],
            "otp":obj_doc["otp"] 
        }
        
        obj_model.find("OTPS", myQuery, proj={"otp":1, "lastModified":1})

        if obj_model.obj_logs.obj_returned["OTPS"] == None:
            obj_model.obj_logs.menthod_log_error(
                errorType="appserverError",
                errorMsg="Invalid Otp",
                errorDesc="Invalid OTP"
            )

        lastModified = (obj_model.obj_logs.obj_returned["OTPS"])["lastModified"]
        
        #return if otp expired
        timeDiff = custom_func.func_get_time_diff(lastModified)

        if timeDiff["minutes"] > 1000:
            obj_model.obj_logs.menthod_log_error(
                errorType="appserverError",
                errorMsg="Otp expired",
                errorDesc="otp expired"
            )

        recordToInsert={
            "userPhoneNumber"  :obj_doc["userPhoneNumber"],
            "userIpAddress"   :[obj_doc["userIpAddress"]],
            "userPassword"     :obj_doc["userPassword"],
            "lastLogin"        : str(custom_func.datetime.datetime.now())
        }

        obj_model.insertRecord("USERS", recordToInsert)

        jwtToken = custom_func.func_create_custom_token(
                {
                    "userPhoneNumber" : obj_doc["userPhoneNumber"],
                    "userPassword"    : obj_doc["userPassword"]
                }
            )
        
        obj_model.obj_logs.method_log_success(token = jwtToken)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == 'ManualError': return 
        obj_model.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList) 


def func_get_user_info(obj_model,obj_doc):
    try:
        myQuery = {    "$and":
                [
                    {
                        "userPhoneNumber":obj_doc["userPhoneNumber"] 
                    },
                    {
                        "userPassword":obj_doc["userPassword"]
                    }
                ]
            }
        
        obj_model.find("USERS", myQuery)
        if obj_model.obj_logs.obj_returned["USERS"] == None:
                obj_model.obj_logs.menthod_log_error(
                    errorType="appserverError",
                    errorMsg="Invalid credentials",
                    errorDesc="Invalid credential"
                )

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == 'ManualError': return 
        obj_model.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)


def func_get_token(obj_model,obj_doc):

    try:
        myQuery = {    "$and":
                [
                    {
                        "userPhoneNumber":obj_doc["userPhoneNumber"] 
                    },
                    {
                        "userPassword":obj_doc["userPassword"]
                    }
                ]
            }
        
        obj_model.find("USERS", myQuery, proj={"_id":1},stopIfRecordNotExist=True,eMsg = "Invalid credentials")

        jwtToken = custom_func.func_create_custom_token(
                {
                    "userPhoneNumber" : obj_doc["userPhoneNumber"],
                    "userPassword"    : obj_doc["userPassword"]
                }
            )
        
        obj_model.obj_logs.method_log_success(token = jwtToken)    

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == 'ManualError': return 
        obj_model.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)        

def func_permission(obj_model,obj_doc):
    '''
        {"token":"jhgjhgjyguygjjhgjugjk"}
    '''
    
    try:
        decoded_payload = custom_func.func_decode_custom_token(obj_doc["token"])

        if "error" in decoded_payload:
            obj_model.obj_logs.method_log_success(decoded_payload)

        myQuery = {    "$and":
                [
                    {
                        "userPhoneNumber":decoded_payload["userPhoneNumber"] 
                    },
                    {
                        "userPassword":decoded_payload["userPassword"]
                    }
                ]
            }  

        obj_model.find("USERS", myQuery, proj={"_id":1},stopIfRecordNotExist=True,eMsg = "Permission denied")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == 'ManualError': return 
        obj_model.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)


