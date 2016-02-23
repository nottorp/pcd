#!/usr/bin/python

import requests
import json
import sys

def test_add(title):
    headers = {'content-type': 'application/json'}
    payload = {'title': title}
    r = requests.post('http://127.0.0.1:8888/v1/new_note', data = json.dumps(payload), headers=headers)
    print "Status code is:", r.status_code
    print "Text is:", r.text

def test_edit(note_id, do_content, text):
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:8888/v1/'
    if do_content:
        url = url + 'set_content/'
        payload = {'content': text}
    else:
        url = url + 'set_title/'
        payload = {'title': text}
    url = url + str(note_id)
    r = requests.put(url, data = json.dumps(payload), headers=headers)
    print "Status code is:", r.status_code
    print "Text is:", r.text

def test_delete(note_id):
    r = requests.delete('http://127.0.0.1:8888/v1/delete/' + str(note_id))
    print "Status code is:", r.status_code
    print "Text is:", r.text

if sys.argv[1] == 'a':
    test_add(sys.argv[2])
elif sys.argv[1] == 'st':
    test_edit(sys.argv[2], False, sys.argv[3])
elif sys.argv[1] == 'sc':
    test_edit(sys.argv[2], True, sys.argv[3])
elif sys.argv[1] == 'd':
    test_delete(sys.argv[2])

