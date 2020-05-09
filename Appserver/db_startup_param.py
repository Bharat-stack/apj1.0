

def func_get_db_param(self, db="test"):

    if db == "test":
        return {"host":"mongodb+srv://admin:admin123@dbcelebrate-pu5ja.mongodb.net/test?retryWrites=true&w=majority",
                "db"  : "dbCelebrate"
        }
