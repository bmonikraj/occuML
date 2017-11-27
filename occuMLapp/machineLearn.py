import mongoDB
import numpy
from sklearn.ensemble import RandomForestClassifier
import time

class ml:
    def decide(self,temp,hum,lig,co2,rehu):
        print time.asctime()
        monH = mongoDB.mongoHandle
        search = monH.findAllData(monH)
        arrX=[]
        sY=[]
        for i in range(0,search.count()):
            subarr=[]
            subarr.append(search[i]['Temperature'])
            subarr.append(search[i]['Humidity'])
            subarr.append(search[i]['Light'])
            subarr.append(search[i]['CO2'])
            subarr.append(search[i]['HumidityRatio'])
            arrX.append(subarr)
            sY.append(search[i]['Occupancy'])
        narX = numpy.array(arrX)
        narY = numpy.array(sY)
        rf = RandomForestClassifier(n_estimators=12,max_features=None)
        rf.fit(narX,narY)
        testX = []
        testX.append(temp)
        testX.append(hum)
        testX.append(lig)
        testX.append(co2)
        testX.append(rehu)
        ntestX = numpy.array(testX)
        testY = rf.predict(ntestX)
        print time.asctime()
        print testY[0]
        if float(testY[0])>0.5:
            return "OC"
        else:
            return "NO"



