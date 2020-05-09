''' Please refer below function while making an APIs
For logging success use: obj_model.obj_logs.method_log_success()
For logging success use: obj_model.obj_logs.menthod_log_error'''


import sys, os

def delete(objModel,objData):
    try:
        objModel.delete("USERS",objData)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == 'ManualError': return 
        objModel.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)