import boto3
from flask import Flask, jsonify, request, session
import json
import requests
from datetime import datetime
from pytz import timezone
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User')
userbase = dynamodb.Table('UserBase')
athlete = dynamodb.Table('Athlete')
Athletetype = dynamodb.Table('AthleteType')
AthleteExpirience = dynamodb.Table('AthleteExpirience')
addresstbl = dynamodb.Table('Address')


class Athlete:
    def AthleteTable():
        postdata = session["Athlete"]
        Insert = postdata['Insert']
        userName = Insert['userName']
        athleteType = Insert['athleteType']
        athleteTypeDescription = Insert['athleteTypeDescription']
        posiTion = Insert['posiTion']
        isProfessional = Insert['isProfessional']
        isValidated = Insert['isValidated']
        weiGht = Insert['weiGht']
        deTails = Insert['deTails']
        reSult = Insert['reSult']
        AchieveMents = Insert['achieveMents']
        mdt = timezone('Greenwich')
        now = datetime.now(mdt)
        d1 = now.strftime("%Y-%m-%d %H:%M:%S")
        createdatetime = d1

        athletetypee = {
            'Username': userName,
            'AthleteType': athleteType,
            'AthleteDescription': athleteTypeDescription
        }
        athletetype = Athletetype.put_item(Item=athletetypee)
        athleteExpirienceData = {
            'Username': userName,
            'Details': deTails,
            'Result': reSult,
            'Achievements': AchieveMents,
            'CreatedDate': createdatetime,
            'ModifiedDate': createdatetime

        }
        athleteExpirienceResponse = AthleteExpirience.put_item(
            Item=athleteExpirienceData)
        athletee = {
            'Username': userName,
            'Position': posiTion,
            'IsProfessional': isProfessional,
            'IsValidated': isValidated,
            'Weight': weiGht,
            'CreatedDate': createdatetime,
            'ModifiedDate': createdatetime
        }
        athletex = athlete.put_item(Item=athletee)
        datadir = json.dumps(athletee)
        return {
            "statusCode": 200,
            "body": datadir
        }
