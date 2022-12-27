from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
import os
from flask import Flask
from datetime import datetime
from google.cloud import firestore
import logging
import requests
import json
logging.basicConfig(level=logging.DEBUG)

f = open("b.txt", "a")
# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = 'f06d7fae6ae3189be4ff15ff13e94578'
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = 'xoxb-4518736053846-4547939199377-b0nhB1F38OACzerg18KNLxdP'
slack_client = WebClient(slack_bot_token)



app = Flask(__name__)

with app.app_context():

    @slack_events_adapter.on('message')
    def message(payload):
        event_data = payload['event']
        text = event_data['text']
        userID = event_data['user']
        title =  str(userID)+ "'s issue"
        channel = event_data['channel']
        if "ISSUE" in text:
            text = text.replace("ISSUE","")
            dictionary = {'title':title, 'body':text}
            jsonString = json.dumps(dictionary, indent=3)
            make_request(jsonString)
        
        if "CALCULATE" in text:
            db = firestore.Client()
            doc = db.collection('users').document(userID).get()
            if doc.exists:
                data = doc.to_dict()
                scores = data['scores']
                n = len(scores)
                if n == 0:
                    slack_client.chat_postMessage(channel=channel, text="There is no score with this user ID in the database")
                else:
                    sums = sum(scores)
                    slack_client.chat_postMessage(channel=channel, text=str(sums/n))
            else:
                data = {}
                slack_client.chat_postMessage(channel=channel, text="There is no score with this user ID in the database")
            dt = datetime.now()
            f.write(str(text.replace("CALCULATE", "")) + " " +  str(datetime.timestamp(dt)) + "\n")


    def make_request(request):

       headers = {
        "Content-Type": "application/json",
        }

       # The URL to send the request to
       url = 'http://34.96.84.250:80/check-sentence'
       response = requests.post(url, json=request, headers=headers)

slack_events_adapter.start(host="0.0.0.0",port=4000)

