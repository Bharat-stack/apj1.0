import pickle
import pathlib
import os
import sys
def funcCreateApi(obj_model,obj_doc):
    try:
        #tempData=obj_doc.pop("url")
        url = obj_doc["url"]
        print(obj_doc)
        obj_doc.pop("url")
        objData={url:obj_doc
        }

        print("doc111111111111111111111111 /n",objData)

        mydict={}
        file=r"\files\apiaction.pkl"
        dirPath=pathlib.Path().absolute()

        myFile = str(dirPath) + str(file)
        
        
        # read python dict back from the file

        if os.path.isfile(myFile) == True: 
            pkl_file = open(myFile, 'rb')
            mydict = pickle.load(pkl_file)
            pkl_file.close()
    
        firstKey=str(next(iter(objData)))

        pyFileName= str(objData[firstKey]["api"]["method"])

        pyFlileToCreate = str(dirPath) +"\\"+ pyFileName.replace(".", "\\") + ".py"
        
        funcInsideMethod= objData[firstKey]["api"]["action"]
        
        lFileExists = os.path.isfile(pyFlileToCreate)

        if  lFileExists== True:
            for doc in mydict:
                print("a",mydict[doc])
                if mydict[doc]["api"]["action"] == funcInsideMethod:
                    obj_model.obj_logs.method_log_success(msg = 'bhai ye action phle se hi api me hai. Gandu doosra dekh')
                    return
        
        # update dict and write to the file again
        mydict.update(objData)
    

        output = open(myFile, 'wb')
        pickle.dump(mydict, output)
        output.close()

        notes="''' Please refer below function while making an APIs\nFor logging success use: obj_model.obj_logs.method_log_success()\nFor logging success use: obj_model.obj_logs.menthod_log_error'''"

        if lFileExists != True:
            out=open(pyFlileToCreate,"w")
            out.write(notes)
            out.write("\n\n\n") 

            out.write("import sys, os\n\n")      

            out.write("def "+funcInsideMethod+"(objModel,objData):\n")
            out.write("    try:\n         objModel.obj_logs.method_log_success(msg = 'lund choosle mera')\n\n")
            out.write("    except Exception as e:\n")
            out.write("        exc_type, exc_obj, exc_tb = sys.exc_info()\n")
            out.write("        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]\n")
            out.write("        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]\n")
            out.write("        if str(e) == 'ManualError': return \n")
            out.write("        objModel.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)")
            out.close

        if lFileExists== True:
            out=open(pyFlileToCreate,"a")
            out.write("\n\n\n")
            out.write("def "+funcInsideMethod+"(objModel,objData):\n")
            out.write("    try:\n         objModel.obj_logs.method_log_success(msg = 'lund choosle mera')\n\n")
            out.write("    except Exception as e:\n")
            out.write("        exc_type, exc_obj, exc_tb = sys.exc_info()\n")
            out.write("        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]\n")
            out.write("        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]\n")
            out.write("        if str(e) == 'ManualError': return \n")
            out.write("        objModel.obj_logs.menthod_log_error(errorType='fatal',errorMsg='Something went wrong',errorDesc=descList)")
            out.close

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        descList=[str(exc_type), str(fname), str(exc_tb.tb_lineno),str(e)]
        if str(e) == "ManualError":
                    return 0
        obj_model.obj_logs.menthod_log_error(
            errorType="fatal",
            errorMsg="Something went wrong",
            errorDesc=descList
        ) 