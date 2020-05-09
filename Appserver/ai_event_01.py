import bson
def func_insert_event(obj_model,obj_doc):

    # Inserting newly created event
    obj_model.insertOneRecord("EVENTS", obj_doc)
    
    if obj_model.obj_logs.var_error == True:
        return 0

    #getting the user_id from recently created event, to store USERS table
    obj_model.FindOne("EVENTS", obj_doc, proj={"_id":1})

    if obj_model.obj_logs.var_error == True:
        return 0
    
    if obj_model.obj_logs.obj_returned["EVENTS"] == None:
        obj_model.obj_logs.menthod_log_error(
            error = {
                    "error_type":"stop",
                    "msg":"Problem in creating events"
                })
        return 0
     
    event_id = (obj_model.obj_logs.obj_returned["EVENTS"])["_id"]

    filter = {
        "user_id":obj_doc["user_id"],
    }

    update={
        "$set":{"org_event_ids":event_id}
    }
    
    obj_model.updateOne("USERS",filter,update)
    if obj_model.obj_logs.var_error == True:
        return 0
    obj_model.obj_logs.method_log_success(
        success = {
                   "event_id":str(event_id)
                })

def func_invite_att(obj_model,obj_doc):

    '''
        obj_doc = {
            event_id:"dasdasdas"
            attendees:[
	            {user_id:9818051081, Name:"Gauraksha", "qty":"2"},
	            {user_id:9818051081, Name:"Gauraksha","qty":"3"},
	            {user_id:9818051081, Name:"Gauraksha","qty":"4"},

        
            ]
        }  
    '''
    #defining all lists
    listOfNewUsersFromReq = []
    listOfAllUserIdFromReq = []

    # getting all attendees from request in a list
    listOfAttendees = obj_doc["attendees"]
    print("listOfAttendees",listOfAttendees)
    listOfAlreadyInvitedUsers = []
    
    #logic to get all the existing invited people 
    _id = bson.ObjectId(obj_doc["event_id"])

    myQuery = {
        "_id":_id
    }
    
    obj_model.FindOne("EVENTS",myQuery,proj={"att_ids":1,"_id":0},stopIfRecordNotExist=True)
    if obj_model.obj_logs.var_error == True:
        return 0
    
    # storing all preexisting invited people in listOfAlreadyInvitedUsers
    if "att_ids" in obj_model.obj_data:
        listOfAlreadyInvitedUsers = obj_model.obj_data["att_ids"]

    print("listOfAlreadyInvitedUsers",listOfAlreadyInvitedUsers)
    
    print("listOfAttendees",listOfAttendees)
    # Extracting user_id from requests
    for doc in listOfAttendees:
        listOfAllUserIdFromReq.append({"user_id":doc["user_id"]})
    
    filter = {
        "$or":listOfAllUserIdFromReq
    }

    obj_model.FindOne("USERS", filter, proj={"user_id":"1","_id":"0"}, many=True)

    if obj_model.obj_logs.var_error == True:
        return 0
    
    listOfExistingCustomersFromReq = obj_model.obj_data
    
    print("listOfExistingCustomersFromReq",listOfExistingCustomersFromReq)

    print("listOfAllUserIdFromReq",listOfAllUserIdFromReq)
    #getting list of all USERS which are being invited but they are not our existing users
    if len(listOfExistingCustomersFromReq) < len(listOfAllUserIdFromReq):

        for doc in listOfAllUserIdFromReq:
            if not(doc in  listOfExistingCustomersFromReq):
                listOfNewUsersFromReq.append(doc)
        filter=listOfNewUsersFromReq
        print("filter", filter)
        #making them part of our ecosystem of celebration, cheers!!!
        obj_model.insertOneRecord("USERS", filter, many = True)
         
        #checking error in api log
        if obj_model.obj_logs.var_error == True:
            return 0
        print("filter",filter)
        for doc in listOfNewUsersFromReq:
            doc.pop("_id")
        print("listOfNewUsersFromReq",listOfNewUsersFromReq)

    filter = []

    for doc in listOfAllUserIdFromReq:
        filter.append({**doc,"$or":[{"event_att_ids":{"$exists":False}},{"event_att_ids":{"$ne":_id}}]})

    filter = {"$or":filter}
    
    print("filter",filter)
    update = {"$push":{"event_att_ids":{"$each":[_id]}}}

    obj_model.updateOne("USERS",filter,update,many=True) 

    #checking error in api log
    if obj_model.obj_logs.var_error == True:
        return 0
    
    filter = {
        "$or":listOfAllUserIdFromReq
    }
    #getting list of all user_id which recently updated 
    obj_model.FindOne("USERS", filter, proj={"_id":1,"user_id":1}, many=True)

    if obj_model.obj_logs.var_error == True:
        return 0
    
    listOfAll_idOfUsers = obj_model.obj_data 
    
    print("listOfAll_idOfUsers",listOfAll_idOfUsers)

    for doc1 in listOfAttendees:
        for doc2 in listOfAll_idOfUsers:
            if doc1["user_id"] == doc2["user_id"]:
                doc1.update({"_id":doc2["_id"]})
                print("1")
                print("2")

    for doc in listOfAttendees:
        doc.pop("user_id")

    print("listOfAttendees",listOfAttendees)
    
    # getting listOfUpdateAttendees(i.e. attendees which needs to be updated) 
    # and listOfDuplicateAttendees    
    print("listOfAlreadyInvitedUsers",listOfAlreadyInvitedUsers)
    for doc in listOfAlreadyInvitedUsers:
        print("f",doc["_id"])
    
    iCount = 0
    while iCount < len(listOfAlreadyInvitedUsers):
        lFlag = False
        print("f",iCount)
        doc = listOfAlreadyInvitedUsers[iCount]
        print("1",doc["_id"])
        for doc1 in listOfAttendees:
            print("2",doc1["_id"])
            print("2",doc["_id"])
            if doc["_id"] == doc1["_id"]:
                print("3",doc1["_id"])
                print("3",doc["_id"])
                if doc["name"] != doc1["name"] or doc["qty"] != doc1["qty"]:
                    print("c",iCount)
                    listOfAlreadyInvitedUsers.remove(doc)
                    lFlag = True
                else:
                    print(4,doc["_id"])
                    print(4,doc["_id"])
                    listOfAttendees.remove(doc1)
                
        if lFlag == False:
            print("flag",iCount)
            iCount = iCount + 1

    print("listOfAttendees111",listOfAttendees)
    print("listOfAlreadyInvitedUsers",listOfAlreadyInvitedUsers)
    listOfAttendees = listOfAttendees + listOfAlreadyInvitedUsers

    print("listOfAttendees11",listOfAttendees)
    #logic for storing and updating the otp with Ip address in OTPS collection in order to verify while doing sign up
    filter = {
        "_id":_id
    }

    update = {"$set":{"att_ids":listOfAttendees}}

    obj_model.updateOne("EVENTS",filter,update)

    #checking error in api log
    if obj_model.obj_logs.var_error == True:
        return 0
    

    

    