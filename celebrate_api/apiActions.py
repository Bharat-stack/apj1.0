import pickle
import pathlib
import os


class Action:
    auth=""
    Actions={
        "/api/createapi":{
            "requestType":"POST",
            "validation":"createapiSerializers",
            "api":{
                "method":"Appserver.apiconfg",
                "action":"funcCreateApi"
            }
        },

        "/api/sendotp01":{
            "requestType":"POST",
            "validation":"sendOtpSerializers",
            "api":{
                "method":"Appserver.ai_sendotp_01",
                "action":"func_SendOtp"
            }
        },
        "/api/signup01":{
            "requestType":"POST",
            "validation":"signupSerializers",
            "api":{
                "method":"Appserver.ai_users_01",
                "action":"func_insert_user"
            }
        },
        "/api/login01":{
            "requestType":"POST",
            "validation":"loginSerializers",
            "api":{
                "method":"Appserver.ai_users_01",
                "action":"func_get_token"
            }
        },
        "/api/getuser01":{
            "requestType":"POST",
            "validation":"getuserSerializers",
            "auth":"True",
            "api":{
                "method":"Appserver.ai_users_01",
                "action":"func_get_user_info"
            }
        },
        "/api/test01":{
            "requestType":"POST",
            "validation":"testSerializers",
            "auth":"True",
            "api":{
                "method":"Appserver.ai_users_01",
                "action":"func_get_user_info"
            }
        }
    }

    def __init__(self, objOfApiLog):
        self.objOfApiLog = objOfApiLog
        file=r"\files\apiaction.pkl"
        dirPath=pathlib.Path().absolute()
        myFile = str(dirPath) + str(file)

        if os.path.isfile(myFile) == True: 
            pkl_file = open(myFile, 'rb')
            mydict = pickle.load(pkl_file)
            pkl_file.close()
            
            self.Actions.update(mydict)
            

    def methodGetApiAction(self):
        
        #getting path(url) from api log
        path   =self.objOfApiLog.request.path
        actions = self.Actions #getting all Action in local variable

        if path in actions:
            doc=actions[path]
            print("doc", doc)
            action = actions[path]["api"]
            self.apiAction= action
            
            requestType=doc["requestType"]

            print(requestType,"gfhjjfg")

            if requestType != self.objOfApiLog.request.method:
                self.objOfApiLog.menthod_log_error(
                    errorType="ApiActionNotFound",
                    errorMsg="Invalid request method = " + requestType,
                    errorDesc="Invalid request method. Try with method = " + self.objOfApiLog.request.method   
                )                

            if "auth" in doc:
                self.auth=True
            
            if "validation" in doc:
                import importlib
                module = importlib.import_module("celebrate_api.serializer")
                #print(self.objOfApiLog.request.data)
                class_ = getattr(module, doc["validation"])
                instance = class_(data=self.objOfApiLog.request.data)
                #class_ = getattr(serializers, doc["validation"])
                #instance = sendOtpSerializers(data=self.objOfApiLog.request.data)
                #function =  getattr(serializers, doc["validation"])
                #valid_ser = function(data=self.objOfApiLog.request.data)
                if not instance.is_valid():
                    self.objOfApiLog.menthod_log_error(
                        errorType="validationError",
                        errorMsg="Invalid json request",
                        errorDesc=instance.errors
                    )
        else:
            self.objOfApiLog.menthod_log_error(
                    errorType="ApiActionNotFound",
                    errorMsg="Invalid URL",
                    errorDesc="Actions of Api has not been defined"
                )
            