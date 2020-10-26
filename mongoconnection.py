import pymongo

DB = None
DBNAME = ""
DBHOST = "127.0.0.1"
DBConnection = False

def setHost(host):
    global DBHOST
    DBHOST = host

def setDB(name):
    global DBNAME
    DBNAME = name

def setDBConnection(val=True):
    global DBConnection
    DBConnection = val

def getDBConnection():
    return DBConnection

def mongoConnection():
    try:
        setDBConnection()
        dbs = pymongo.MongoClient(DBHOST, 27017)
        global DB
        DB = dbs.get_database(DBNAME)
        print("Connected to " + str(DB) + "\n")
        return DB
    except Exception as error:
        print("Database Connection error: " + str(error))

def getVeiculos():
    try:
        vehicle = DB['recursos'].find()
        radioIds = []
        for car in vehicle:
            radioIds.append(str(car.get("radioId")))
        return radioIds
    except Exception as error:
        print("mongoConnection, getVeiculos Error: " +  str(error))

def getVeiculosFromRecusos():
    try:
        recursos = DB['devices'].find()       
        for rec in recursos:
            if rec.get("nome") == 'API FullTrack2':
                return rec.get("radioList")
    except expression as identifier:
        print("mongoConnection, getVeiculosFromRecusos Error: " +  str(error))

def getFulltrack2Keys():
    try:
        recursos = DB['devices'].find()
        for rec in recursos:
            if rec.get("nome") == 'API FullTrack2':
                keys = {}
                keys["apiKey"] = rec.get("login")
                keys["secretKey"] = rec.get("password")
                return keys
    except Exception as error:
        print("mongoConnection, getFulltrack2Keys Error: " +  str(error))
    