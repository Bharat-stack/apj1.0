from Appserver import db_startup_param
from Appserver.api_log import ApiLogs
from Appserver.appServer import Appserver
import inspect
from rest_framework.decorators import api_view
from .apiActions import Action
from Appserver import custom_func

def beautifullFuck(request,auth=False):
    
    try:
        objOfIAmGod = IAmGod(request)   
        
        if objOfIAmGod.auth == True:
            apiAction={
                "method":"Appserver.ai_users_01",
                "action":"func_permission"
            }
            objOfIAmGod.methodRunApi(apiAction)

        objOfIAmGod.methodRunApi(objOfIAmGod.apiAction)

        #return objOfIAmGod.methodGetResponse()

    except Exception as e:
        if str(e) != "ManualError":
            objOfIAmGod.objOfApiLog.menthod_log_error(
                errorType="fatal",
                errorMsg="Something went wrong",
                errorDesc=str(e)
            )
    finally:
        return objOfIAmGod.methodGetResponse()

class IAmGod:
    def __init__(self,request):      
        try:
            self.apiAction=""
            self.request   = request
            self.reqBody   = request.data
            self.reqHeader = request.META
            self.auth=""
            self.objOfApiLog = ApiLogs()

            self.objOfApiLog.request = request 

            objOfAction = Action(self.objOfApiLog)

            objOfAction.methodGetApiAction()
            
            self.auth=objOfAction.auth

            self.apiAction=objOfAction.apiAction

            #Getting data base parameter parameter for making connections
            db_param = db_startup_param.func_get_db_param("test")

            self.objOfAppServere = Appserver(self.objOfApiLog,db_param["host"],db_param["db"])

        except Exception as e:

            if str(e) != "ManualError":
                self.objOfApiLog.menthod_log_error(
                    errorType="fatal",
                    errorMsg="Something went wrong",
                    errorDesc=str(e)
                )

    def methodRunApi(self,apiAction):

        if self.objOfApiLog.var_error == True:
            if hasattr(self, 'objOfAppServere'):self.objOfAppServere.methodCloseConn()
            return
        
        if apiAction["action"] == "func_permission":
            if not("HTTP_AUTH" in self.request.META):
                self.objOfApiLog.menthod_log_error(
                    errorType="validationError",
                    errorMsg="Something went wrong",
                    errorDesc="token is required"
                )
                return
                

            token = self.request.META.get('HTTP_AUTH') 
            doc = {"token":token}
            
            self.objOfAppServere.method_process_req({**apiAction, "objDoc":doc})
            
            if self.objOfApiLog.var_error == True:
                return

            decoded_payload = custom_func.func_decode_custom_token(token)

            self.reqBody = {**self.reqBody,**decoded_payload}
            return

        if self.request.method=="POST":
            doc = self.reqBody

        self.objOfAppServere.method_process_req({**apiAction, "objDoc":doc})

    def methodGetResponse(self):
        response = self.objOfApiLog.method_get_response()
        return response