from django.http import JsonResponse
from rest_framework.decorators import api_view
from .myOwnFrameWork import beautifullFuck
        
@api_view(['GET', 'POST'])
def BharatView(request,endpoint=None):

    print(endpoint, request.path)
    response = beautifullFuck(request)
    return JsonResponse(response) # methods must return HttpResponse
    

'''api_view(['GET', 'POST'])
def create_user_01(request):

    response = beautifullFuck(request)
    
    return JsonResponse(response) # methods must return HttpResponse          

@api_view(['GET', 'POST'])
def send_otp_01(request):
    
    response = beautifullFuck(request)
    
    return JsonResponse(response) # methods must return HttpResponse      

@api_view(['GET', 'POST'])
def get_token_01(request):
    
    response = beautifullFuck(request)
    
    return JsonResponse(response) # methods must return HttpResponse      

@api_view(['GET', 'POST'])
def get_user_01(request):
    
    response = beautifullFuck(request,auth=True)
    
    return JsonResponse(response) # methods must return HttpResponse   
'''
''' 
@api_view(['GET', 'POST'])
def get_user_01(request):
    
    obj_logs = ApiLogs()
    if request.method =="POST":

        token = request.META.get('HTTP_AUTH')

        #get and decode token
        decoded_payload = custom_func.func_decode_custom_token(token)
        if "error" in decoded_payload:
            return JsonResponse(decoded_payload)       

        #Getting data base parameter parameter for making connections
        db_param = db_startup_param.func_get_db_param("test")

        print(decoded_payload)
        #setting api endpoint action
        api_action={
            "method":"Appserver.ai_users_01",
            "action":"func_get_user_info"
        }

        #wrapping all API parameter which is required for APPSEVER
        api_param = {**db_param, **api_action,"obj_doc":decoded_payload}
       
        #getting object and processing request 
        
        obj_appserver = appServer.RunApi(obj_logs)

        obj_appserver.method_process_req(api_param)
        
        response = obj_logs.method_get_response()

        return JsonResponse(response) # methods must return HttpResponse  

@api_view(['GET', 'POST'])
def send_otp_01(request):
    
    objOfIAmGod= beautifullFuck(request,"send_otp_01")
    #setting api endpoint action
    apiAction={
        "method":"Appserver.ai_sendotp_01",
        "action":"func_SendOtp"
    }

    objOfIAmGod.methodRunApi(apiAction)

    response = objOfIAmGod.methodGetResponse()
    
    return JsonResponse(response) # methods must return HttpResponse

@api_view(['GET', 'POST'])
def get_token(request):

    objOfIAmGod= beautifullFuck(request,"send_otp_01")
    #setting api endpoint action
    apiAction={
            "method":"Appserver.ai_users_01",
            "action":"func_get_token"
        }

    objOfIAmGod.methodRunApi(apiAction)

    response = objOfIAmGod.methodGetResponse()
    
    return JsonResponse(response) # methods must return HttpResponse
'''
'''@api_view(['GET', 'POST'])
def decode_token(request):

    if request.method=="POST":
        
        get_token = request.data["token"]
        
        #token_to_decode=reqData.encode("utf-8")
        resp_status = custom_func.func_decode_custom_token(get_token)
        return JsonResponse(resp_status)
'''
'''@api_view(['GET', 'POST'])
def get_otp(request):

    obj_logs = ApiLogs()

    if request.method=="POST":
        
        req_body = dict(request.data)

        #Getting data base parameter parameter for making connections
        db_param = db_startup_param.func_get_db_param("test")

        #setting api endpoint action
        api_action={
            "method":"ai_sendotp_01",
            "action":"func_SendOtp"
        }

       #wrapping all API parameter which is required for APPSEVER
        api_param = {**db_param, **api_action,"obj_doc":req_body} 
        
        obj_appserver = appServer.RunApi(obj_logs)

        obj_appserver.method_process_req(api_param)
        
        response = obj_logs.method_get_response()

        return JsonResponse(response)

@api_view(['GET', 'POST'])
def create_event_01(request):

    obj_logs = ApiLogs()    
    if request.method =="POST":
        
        #Get the requested data of new user
        req_body = dict(request.data)
        
        #Getting data base parameter parameter for making connections
        db_param = db_startup_param.func_get_db_param("test")

        #setting api endpoint action
        api_action={
            "method":"Appserver.ai_event_01",
            "action":"func_insert_event"
        }

        #wrapping all API parameter which is required for APPSEVER
        api_param = {**db_param, **api_action,"obj_doc":req_body}
        
        #getting object and processing request 
        obj_appserver = appServer.RunApi(obj_logs)

        obj_appserver.method_process_req(api_param)
        
        response = obj_logs.method_get_response()
        
        return JsonResponse(response) # methods must return HttpResponse      

@api_view(['GET', 'POST'])
def invite_att_01(request):

    obj_logs = ApiLogs()    
    if request.method =="POST":
        
        #Get the requested data of new user
        req_body = dict(request.data)
        
        #Getting data base parameter parameter for making connections
        db_param = db_startup_param.func_get_db_param("test")

        #setting api endpoint action
        api_action={
            "method":"Appserver.ai_event_01",
            "action":"func_invite_att"
        }

        #wrapping all API parameter which is required for APPSEVER
        api_param = {**db_param, **api_action,"obj_doc":req_body}
        
        #getting object and processing request 
        obj_appserver = appServer.RunApi(obj_logs)

        obj_appserver.method_process_req(api_param)
        
        response = obj_logs.method_get_response()
        
        return JsonResponse(response) # methods must return HttpResponse      
'''
