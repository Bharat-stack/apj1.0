import inspect

class ApiLogs:

    obj_error    = ""
    var_error    = False
    obj_recieved = ""
    obj_success = {"msg":"bhag bhosadike"}
    obj_returned = "" 
    obj_response = ""
    obj_conn     = ""
    obj_client   = ""
    var_warning  = False
    objWarning   = "" 
    request=""

    def menthod_log_error(self, **kwargs):

        tracker =  "progName = " + str(inspect.stack()[0][1]) + ",lineNum = " + str(inspect.stack()[0][2]) \
        + ", code=" + str(inspect.stack()[0][3]) \
        +"-->" \
        + "progName = " + str(inspect.stack()[1][1]) + ",lineNum = " + str(inspect.stack()[1][2]) \
        + ", code=" + str(inspect.stack()[1][3]) \
        +"-->" \
        + "progName = " + str(inspect.stack()[2][1]) + ",lineNum = " + str(inspect.stack()[2][2]) \
        + ", code=" + str(inspect.stack()[2][3]) \
        +"-->" \
        + "progName = " + str(inspect.stack()[3][1]) + ",lineNum = " + str(inspect.stack()[3][2]) \
        + ", code=" + str(inspect.stack()[3][3]) \
        +"-->" \
        + "progName = " + str(inspect.stack()[4][1]) + ",lineNum = " + str(inspect.stack()[4][2]) \
        + ", code=" + str(inspect.stack()[4][3])       
        
       
        
        self.obj_error={
            "error":{**kwargs,**{"errorFrom":tracker}}
        }

        self.var_error = True
        
        if "errorType" in kwargs and kwargs["errorType"] != "fatal":
            raise Exception('ManualError')
        

    def menthod_log_warning(self, **kwargs):

        self.objWarning = {
            "warning":{**kwargs,"errorFrom":inspect.stack()}
        }
        self.var_warning == True
          
    
    def method_log_success(self, **kwargs):

        self.obj_success = kwargs
        
        if "success" in kwargs:
            self.obj_returned = kwargs["success"]

    def method_send_parameter(self, **kwargs):

        self.obj_recieved = kwargs

    def method_reurned_parameter(self, **kwargs):

        self.obj_returned = kwargs
        #self.var_error    = False

    def method_get_response(self,**kwargs):
        
        #print("apiLog", self.var_error, dict(self.obj_error), self.obj_success)
        if self.var_error == True:
           return  dict(self.obj_error)
        elif self.var_warning == True:
           return dict({**self.obj_success,**self.objWarning})
        else:
            return dict(self.obj_success)   
        




       
