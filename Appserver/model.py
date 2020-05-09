import pymongo
from pymongo import MongoClient
from pymongo import errors
import datetime

class Model():

    obj_db     = ""
    obj_client = ""
    obj_data   = []

    def __init__(self, obj_logs):
        self.obj_logs    =  obj_logs
        self.objOfApiLog =  obj_logs

    def getConnection(self, host, dbName):
        try:
            client = MongoClient(host)           
            db     = client.get_database(dbName)

        except Exception as e:
            self.obj_logs.menthod_log_error(
                errorType="dataServerError",
                errorMsg="Something went wrong",
                errorDesc=str(e)
            )
        else:
            self.obj_logs.method_reurned_parameter(
                conn = db,
                client = client          
            )
            self.obj_db     = db
            self.obj_client = client

    def closeConnection(self, client=None):

        try:
           if client == None:
                client = self.obj_client
           client.close()

        except Exception as e:
            self.obj_logs.menthod_log_warning(
                errorType="dataServerError",
                errorMsg="Something went wrong",
                errorDesc=str(e)
            )

        else:
            self.obj_logs.method_reurned_parameter(
                obj_con_close=True         
            )

    def insertRecord(self,collection_name , docObj,db=None, many = False):

        try:
            if  db == None:
                db = self.obj_db
         
            users = db[collection_name]

            if many == True:
                result = users.insert_many(docObj)
            else:
                result = users.insert_one(docObj)

        except Exception as e:
            self.obj_logs.menthod_log_error(
                errorType="dataServerError",
                errorMsg="Something went wrong while inserting record",
                errorDesc=str(e)
            )
        else:
            self.obj_logs.method_log_success(
                success = {
                    "Msg":"Record inserted successfully",
                    "desc":str(result)
                })

    def find(self,collection_name , query , proj={"_id":0}, check=False,db=None, many=False,stopIfRecordNotExist=False,eMsg=""):
        self.obj_data = []
        result=[]
        try:
            if db == None:
                db = self.obj_db
     
            users = db[collection_name]
            
            if many == True:
                for doc in users.find(query,proj):                
                    self.obj_data.append(doc)
                    result.append(doc)

            else:
                result = users.find_one(query,proj)
                self.obj_data = result 
        
            if result != None and check==True:
                self.obj_logs.menthod_log_error(
                    errorType="appServerError",
                    errorMsg  = eMsg,
                    errorDesc = "Record already exists in collection : " + collection_name + " for query: " + str(query)
                )
        
            if stopIfRecordNotExist == True and result == None:
                self.obj_logs.menthod_log_error(
                    errorType="appServerError",
                    errorMsg  = eMsg,
                    errorDesc = "Record not exists in collection : " + collection_name + " for query: " + str(query)
                )

        except Exception as e:
            if not(str(e)=="ManualError"):
                self.obj_logs.menthod_log_error(
                        errorType ="dataServerError",
                        errorMsg  = "Something went wrong",
                        errorDesc = str(e)
                    )
            else:
                raise Exception("ManualError")

        else:
            self.obj_logs.method_log_success(
                success = {
                    collection_name:result
                })
            #return obj_log

    def update(self,collection_name,filter,update,upsert=False,bypass_document_validation=False, collation=None, array_filters=None, session=None,db=None,many=False):
        try:
            if db == None:
                db = self.obj_db

            users = db[collection_name]
            
            if many == True:
                result = users.update_many(filter,update,upsert)
            else: 
                result = users.update_one(filter,update,upsert)
            
        except Exception as e:
            self.obj_logs.menthod_log_error(
                    errorType="dataServerError",
                    errorMsg  = "Something went wrong",
                    errorDesc = str(e)
                )
        else:
            self.obj_logs.method_log_success(
                success = {
                    collection_name:str(result)
                })
    
    def delete(self,collection_name,query,many=False,db=None):
        
        try:
            if db == None:
                db = self.obj_db

            users=db[collection_name]

            if many == True:
                result = users.delete_many(query)
            else: 
               result = users.delete_many(query)

        except Exception as e:
            self.obj_logs.menthod_log_error(
                    errorType="dataServerError",
                    errorMsg  = "Something went wrong",
                    errorDesc = str(e)
            )

        else:
            self.obj_logs.method_log_success(
            success = {
                collection_name:str(result)
            })




            
        
