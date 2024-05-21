#coding:utf-8

import boto3
import json
import requests
import urllib
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_federation_token(key_id, secret_key):
   
    session = boto3.Session(
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key
    )

    client = session.client('sts')

    try:
        response = client.get_federation_token(
                Name="IntelBrokers",
                Policy=json.dumps({
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Effect': 'Allow',
                        'Action': '*',
                        'Resource': '*'
                    }]
                })
        )
    except Exception as e:
        return jsonify({
            "error": [
                "Creds are not working!"
            ]
        })

    return response

def generate_signin_url(fed_response):

    try:
        params = {
            'Action': 'getSigninToken',
            'Session': json.dumps({
                'sessionId': fed_response['Credentials']['AccessKeyId'],
                'sessionKey': fed_response['Credentials']['SecretAccessKey'],
                'sessionToken': fed_response['Credentials']['SessionToken']
            })
        }
    except Exception as e:
        return jsonify("error")

    fed_resp = requests.get(url="https://signin.aws.amazon.com/federation", params=params)
    signin_token = fed_resp.json()['SigninToken']

    signin_params = {
        'Action': 'login',
        'Issuer': '',
        'Destination': 'https://console.aws.amazon.com/console/home',
        'SigninToken': signin_token
    }

    signin_url = 'https://signin.aws.amazon.com/federation?' + urllib.parse.urlencode(signin_params) 

    return signin_url

@app.route("/", methods=["GET"])
def get_token_link_json():
    
    # get key_id and secret_key
    get_aws_access_key_id = request.args.get('key_id')
    get_aws_secret_access_key = request.args.get('secret_key')

    if(get_aws_access_key_id is not None and get_aws_secret_access_key is not None):
        try:
            federation_response = get_federation_token(get_aws_access_key_id, get_aws_secret_access_key)
            signin_url = generate_signin_url(federation_response)
            
            try:
                return jsonify({
                    "success": [
                        signin_url
                    ]
                })
            
            except TypeError as e:
                return jsonify({
                    "error": [
                        "Creds are not working!"
                    ]
                })

        except Exception as e:
            return jsonify({
                "error": [
                    e
                ]
            })

    return jsonify({
        "success": [
            "active"
        ],
        "author": "@ Sanggiero"
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1337)
