from pymongo import MongoClient

mongoClient = MongoClient("mongodb://localhost:27017")
db = mongoClient.antimal

def getBaseColl():
    base_Coll = db["antimal"]
    return base_Coll

def getLogColl():
    logColl=db['logCol']
    return logColl