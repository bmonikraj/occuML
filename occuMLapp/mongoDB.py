import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from django.views.decorators.csrf import ensure_csrf_cookie     #FOr csrf in production server MUST
@ensure_csrf_cookie   #for csrf in production server MUST

class mongoHandle:
    def deleteLastData(self):
        c = MongoClient('localhost',27017)
        db = c.occuML
        search = db.data.find({},{"ID":1}).sort('ID', pymongo.ASCENDING).limit(1) #second parameter as PROJECTION, first parameteer as SELECTION
        n = int(search[0]['ID'])
        db.data.delete_one({'ID':n})
        c.close()

    def insertNewData(self,temp,hum,lig,co2,rehu,oc):
        c = MongoClient('localhost',27017)
        db = c.occuML
        #Data comes in the proper document format
        search = db.data.find({}, {"ID": 1}).sort('ID', pymongo.DESCENDING).limit(1)
        newID = search[0]['ID']+1
        db.data.insert_one({"ID":newID,"Temperature":temp,"Humidity":hum,"Light":lig,"CO2":co2,"HumidityRatio":rehu,"Occupancy":oc})
        c.close()

    def findAllData(self):
        c = MongoClient('localhost', 27017)
        db = c.occuML
        # Data comes in the proper document format
        search = db.data.find({})
        c.close()
        return search#Returns The whole data set in BSON Format

    def loginUser(self,email,pwd):
        c = MongoClient('localhost',27017)
        db = c.occuML
        res = db.user.find({"$and": [{"Email": email}, {"Password": pwd}]})
        if res.count()==1:
            return 1#successful login
        else:
            return 0#Unsuccessful Login

    def registerUser(self, email, pwd):
        c = MongoClient('localhost', 27017)
        db = c.occuML
        res = db.user.find({"Email": email})
        if res.count()==0:
            s = db.user.insert_one({"Email":email, "Password":pwd})
            if s==None:
                return 0#Failed Regsitration
            else:
                return 1#Successful Registration
        else:
            return -1#Already exists



