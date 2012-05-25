# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
#=======================================================#

def index(request):
    return render_to_response('index.html')

#=======================================================#

def get_model (request):
    """
    Sends the conversion table
    """

    #fb = settings.FIdER_BACKEND_URL
    #mdl = sendMessageToServer("", fb+"/get_model/last", "GET")

    #fields_table = json.loads(mdl)
    fields_table = {
        'Node' : {
            'LocationNote' : 'str',
            'Tipologia': 'str',
            'Address' : 'str',
            'Neighborhood': 'str',
        },
        'Well' : {
            'Name' : 'str',
            'RETE' : 'str',
            'Address' : 'str',
            'Closure' : 'str',
            'Width' : 'int',
            'Length' : 'int'
        },
        'Duct' : {
            'Length': 'int',
            'Tube': 'str',
            'CODICE': 'str',
            'RETE': 'str',
            'Infrastructure': 'str'
        }

    }

    return HttpResponse(json.dumps(fields_table), mimetype="application/json")

def start_token (request):
    """
    Answers the registration request and sends the "unique" token
    """


    fb = settings.FIdER_BACKEND_URL
    mdl = sendMessageToServer("", fb+"/get_model/last", "GET")
    
    v = json.loads(mdl)
    v = v['version']

    import uuid
    token = str(uuid.uuid4())
    #TODO: prepare token and session
    welcome_message = {
        "token": token,
        "message_type": u'response',
        "message_format": u'welcome',
        "latest_model_version": v,
    }

    return HttpResponse(json.dumps(welcome_message), mimetype="application/json")

def approve_manifest (request):
    """
    Approves the manifest and confirms the creation of the softproxy on the main server
    """

    print "Answering manifest request"

    manifestapproval = {
        "message_type" : u'response',
        "message_format" : u'manifest',
        "approved": True,
        "message": "Manifest approved"
    }

    return HttpResponse(json.dumps(manifestapproval), mimetype="application/json")

def request_write (request):
    """
    Answers a write request message
    """
    jsonmessage = json.loads(request.REQUEST.get('jsondata', None))
    writes = jsonmessage['data']['upsert'].keys()
    response_write = {
        "token": jsonmessage['token'],
        "message_type": u'response',
        "message_format": u'write',
        "acknowledge": {
            "upsert": writes,
            "delete": []
        },
        "anomalies": []
    }

    return HttpResponse(json.dumps(response_write), mimetype="application/json")



def sendMessageToServer (jsonmessage, url, method):
    """
    Sends a json message to the main server and returns success if the response code is correct
    :param jsonmessage: data to be sent to the server, already in json format (json.dumps())
    :param url:
    :param method:
    :return: response from server
    """


    #TODO: placeholder, implement, note that cannot be async if we want to keep the full comm cycle in this one only; should we also keep the full response from the other server?

    datalen = len(jsonmessage)
    headers = {'Content-Type': 'application/json', 'Content-Length': datalen}

    req = urllib2.Request(url, jsonmessage, headers)
    conn = urllib2.urlopen(req)

    return conn.read()


