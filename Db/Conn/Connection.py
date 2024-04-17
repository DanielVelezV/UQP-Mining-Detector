import pymongo


client = pymongo.MongoClient("localhost", 27017)

DB = client.get_database("UQPDb")

UQPDC = DB["UQPData"]

UQPMoonC = DB["UQPMoons"]

