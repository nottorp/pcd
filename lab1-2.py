#!/usr/bin/python
import json
from flask import Flask, request, Response
import datetime
import random

# Port for Flask to listen on
PORT = 8888

# Custom error codes and other return codes
HTTP_OK = 200
ERR_NOTFOUND = 404
ERR_TEAPOT = 418
ERR_GIMME_JSON = 479
ERR_MISSING_FIELD = 478

# Bad global data store :)
data = dict()
data[1] = {'title': 'Apples', 'content': "Adam's, Golden, Granny, Stolen, Plastic"}
data[2002] = {'title': '', 'content': 'L10'}

app = Flask(__name__)
random.seed()

def setup():
    app.debug = True

def run():
    app.run(port = PORT)

@app.route('/', methods=['GET'])
def index():
    return versions()

@app.route('/versions', methods=['GET'])
def versions():
    return Response(response='{"protocol-versions": [1]}', mimetype='application/json', status=HTTP_OK)

@app.route('/stfu')
def stfu():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return Response(response='Shutting up!', mimetype="text/plain", status=HTTP_OK)

@app.route('/v1/notes', methods=['GET', 'OPTIONS'])
def v1_list():
    if request.method == 'OPTIONS':
        resp = Response(response='Listed methods', mimetype='text/plain', status=HTTP_OK)
        resp.headers['Allow'] = 'GET, OPTIONS'
        return resp
    res = {}
    res['notes'] = []
    for id, content in data.iteritems():
        tmp = {}
        tmp['id'] = id
        tmp['title'] = content['title']
        res['notes'].append(tmp)
    my_status = HTTP_OK
    # Friday the 13th, 10% probability on each request
    if (datetime.datetime.today().day == 13) and (datetime.datetime.today().weekday() == 4):
        if random.random() > 0.9:
            my_status = ERR_TEAPOT
    return Response(response=json.dumps(res), mimetype='application/json', status=my_status)

def note_exists(note_id_string):
    try:
        note_id_int = int(note_id_string)
    except:
        return -1
    if not data.has_key(note_id_int):
        return -1
    return note_id_int

@app.route('/v1/notes/<note_id>', methods=['GET'])
def v1_note(note_id):
    note_id_int = note_exists(note_id)
    if note_id_int < 0:
        return Response(response="Not Found!", mimetype="text/plain", status=ERR_NOTFOUND)
    res = {}
    res['id'] = note_id_int
    res['title'] = data[note_id_int]['title']
    res['content'] = data[note_id_int]['content']
    return Response(response=json.dumps(res), mimetype='application/json', status=HTTP_OK)

@app.route('/v1/notes/create', methods=['POST'])
def v1_new_note():
    if request.headers['Content-Type'] != 'application/json':
        return Response(response="Gimme JSON!", mimetype='text/plain', status=ERR_GIMME_JSON)
    if not request.json.has_key('title'):
        return Response(response="Mandatory field 'title' missing!", mimetype='text/plain', status=ERR_MISSING_FIELD)
    # Yeah I know, the storage is dumb
    new_id = 1
    while data.has_key(new_id):
        new_id = new_id + 1
    data[new_id] = dict()
    data[new_id]['title'] = request.json['title']
    # This field is optional, but copy it if it's there
    if request.json.has_key('content'):
        data[new_id]['content'] = request.json['content']
    else:
        data[new_id]['content'] = ''
    res = {}
    res['id'] = new_id
    return Response(response=json.dumps(res), mimetype='application/json', status=HTTP_OK)

# These two should be collapsed into one somehow - need a little experimentation with Flask for that
@app.route('/v1/notes/set_title/<note_id>', methods=['PUT'])
def v1_set_title(note_id):
    if request.headers['Content-Type'] != 'application/json':
        return Response(response="Gimme JSON!", mimetype='text/plain', status=ERR_GIMME_JSON)
    if not request.json.has_key('title'):
        return Response(response="Mandatory field 'title' missing!", mimetype='text/plain', status=ERR_MISSING_FIELD)
    note_id_int = note_exists(note_id)
    if note_id_int < 0:
        return Response(response="Not Found!", mimetype="text/plain", status=ERR_NOTFOUND)
    data[note_id_int]['title'] = request.json['title']
    if request.json.has_key('content'):
        data[note_id_int]['content'] = request.json['content']
    return Response(response="Title modified succesfully!", mimetype="text/plain", status=HTTP_OK)

# This and the one above should be collapsed into one somehow - need a little experimentation with Flask for that
@app.route('/v1/notes/set_content/<note_id>', methods=['PUT'])
def v1_set_content(note_id):
    if request.headers['Content-Type'] != 'application/json':
        return Response(response="Gimme JSON!", mimetype='text/plain', status=ERR_GIMME_JSON)
    if not request.json.has_key('content'):
        return Response(response="Mandatory field 'content' missing!", mimetype='text/plain', status=ERR_MISSING_FIELD)
    note_id_int = note_exists(note_id)
    if note_id_int < 0:
        return Response(response="Not Found!", mimetype="text/plain", status=ERR_NOTFOUND)
    print "Content content:", request.json['content']
    data[note_id_int]['content'] = request.json['content']
    print "Content content after:", data[note_id_int]['content']
    return Response(response="Content modified succesfully!", mimetype="text/plain", status=HTTP_OK)

@app.route('/v1/notes/delete/<note_id>', methods=['DELETE'])
def v1_delete(note_id):
    note_id_int = note_exists(note_id)
    if note_id_int < 0:
        return Response(response="Not Found!", mimetype="text/plain", status=ERR_NOTFOUND)
    return Response(response="Note deleted!", mimetype="text/plain", status=HTTP_OK)


if __name__ == "__main__":
    setup()
    run()

