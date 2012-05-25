# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response

#=======================================================#

def index(request):
    return render_to_response('index.html')

#=======================================================#

def get_model (request):
    """
    Sends the conversion table
    """

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

    import uuid
    token = str(uuid.uuid4())
    #TODO: prepare token and session
    welcome_message = {
        "token": token,
        "message_type": u'response',
        "message_format": u'welcome',
        "latest_model_version": 1,
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
    jsonmessage = json.loads(request.POST['jsondata'])
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
