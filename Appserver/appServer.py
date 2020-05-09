import importlib
import sys, os

from Appserver.model import Model

class Appserver:

    objLogs = ""

    def  __init__(self, objLogs, host,db):
        self.objLogs = objLogs
        
        #validate will work later on this
        self.objModel = Model(objLogs)
        #print("Appserver") 
        self.objModel.getConnection(host,db)

    def method_process_req(self,reqJsonObj):
        objLogs = self.objLogs
        objModel = self.objModel
        for key in reqJsonObj:
            if key == "action":
                action = reqJsonObj[key]
            if key=="method":
                method = reqJsonObj[key]
            if key=="objDoc":
                objDoc=reqJsonObj[key]
        #Creating connection object, saving these values in logs

        try:
            #getting the class name i.e Appserver API to be called and its method from db processing
            ClassName=  importlib.import_module(method)
            func = getattr(ClassName, action)
            
            #calling Appserver API action and giving required parameter
            func(objModel,objDoc)


            objModel.closeConnection()
        
        except Exception as e:
            objModel.closeConnection()
            if str(e) == "ManualError":
                return 0

            objLogs.menthod_log_error(
                errorType="fatal",
                errorMsg="Something went wrong",
                errorDesc=str(e)
            )
         

    def methodCloseConn(self):
        self.objModel.closeConnection() 