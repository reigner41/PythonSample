import requests
import cgi
import cgitb
import os
import ssl
import sys
import json
import datetime
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, abort


class User:
    def jsonglobal():
        content = {}

    def UserDynamoAPI():
        #        postdata = session["User"]
        postdata = User.jsonglobal
        postdatadir = json.dumps(postdata)
        postdataloads = json.loads(postdatadir)
        Username = postdataloads['Username']
        insertemployee = requests.patch(
            'https://acumatica-firebase.firebaseio.com/Employee/'+Username+'.json', json=postdataloads)
        print(insertemployee.json())

    def UserLogin():
        #        postdata = session["User"]
        postdata = User.jsonglobal
        postdatadir = json.dumps(postdata)
        postdataloads = json.loads(postdatadir)
        email = postdataloads['email']
        password = postdataloads['password']
        insertemployee = requests.get(
            'https://acumatica-firebase.firebaseio.com/Users/'+email+'.json')
        employeedir = json.dumps(insertemployee.json())
        employeeloads = json.loads(employeedir)
        password2 = employeeloads['Password']
        if password == password2:
            return render_template('index.html')
