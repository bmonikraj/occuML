from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.template import Context, loader, Template
from django.views.decorators.csrf import ensure_csrf_cookie     #FOr csrf in production server MUST
import json
import mongoDB
import machineLearn

@ensure_csrf_cookie   #for csrf in production server MUST
# Create your views here.

def index(request):
    temp = loader.get_template("index.html")
    return HttpResponse(temp.render())

def result(request):
    temp = loader.get_template("result.html")
    if request.session.get('loginCheck')==1:
        return HttpResponse(temp.render())
    return HttpResponse("<script>window.open('/','_self');</script>")

def mongoConn(request):
    if request.method == 'POST':
        if request.is_ajax():
            if str(request.POST.get('jsonData'))=='logout':
                request.session['loginCheck']=0
                return HttpResponse("1")

            jsonRequest = str(request.POST.get('jsonData'))
            jsonRequestObj = json.loads(jsonRequest)
            condition = jsonRequestObj['task']
            if condition=='Register':
                regHandler = mongoDB.mongoHandle
                RES = regHandler.registerUser(regHandler, str(jsonRequestObj['email']), str(jsonRequestObj['pwd']))
                return HttpResponse(str(RES))

            if condition=='Login':
                logHandler = mongoDB.mongoHandle
                RES = logHandler.loginUser(logHandler, str(jsonRequestObj['email']), str(jsonRequestObj['pwd']))
                if RES==1:
                    request.session['loginCheck']=1
                return HttpResponse(str(RES))

            if condition!='Register' and condition!='Login':
                upHandler = mongoDB.mongoHandle
                upHandler.deleteLastData(upHandler)
                oc=1
                if str(jsonRequestObj['Occupancy'])=='rgb(255, 0, 0)':
                    oc = 0
                if str(jsonRequestObj['Occupancy'])=='rgb(0, 255, 0)':
                    oc = 1
                upHandler.insertNewData(upHandler, float(jsonRequestObj['Temperature']), float(jsonRequestObj['Humidity']), float(jsonRequestObj['Light']), float(jsonRequestObj['CO2']), float(jsonRequestObj['HumidityRatio']), oc)
                return HttpResponse("UD")
    return HttpResponse("Hitting")


def m_learn(request):
    if request.method == 'POST':
        if request.is_ajax():
            jsonRequest = str(request.POST.get('jsonData'))
            jsonRequestObj = json.loads(jsonRequest)
            condition = jsonRequestObj['task']
            if condition=='decide':
                print "hitting ML server..."
                mlHandler = machineLearn.ml()
                status = mlHandler.decide(float(jsonRequestObj['Temperature']), float(jsonRequestObj['Humidity']), float(jsonRequestObj['Light']), float(jsonRequestObj['CO2']), float(jsonRequestObj['HumidityRatio']))
                return HttpResponse(str(status))
    return HttpResponse("Expert is down!")