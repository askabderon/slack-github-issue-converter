import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from threading import Thread
from datetime import datetime

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token='xoxb-4518736053846-4547939199377-b0nhB1F38OACzerg18KNLxdP')

# ID of the channel you want to send the message to
calculate_channel_id = "C04G50YU78Q"
issue_channel_id = "C04FGM7LXK9" 

f = open("first.txt", "a")


def send_message_to_slack(i):
    try:
        # Call the chat.postMessage method using the WebClient
        dt = datetime.now()
        dtt = datetime.timestamp(dt)
        f.write(str(i) + " " + str(dtt) + "\n")
        result = client.chat_postMessage(
            channel=issue_channel_id, 
            text="ISSUE could you create an issue " + str(i)
        )

    except SlackApiError as e:
        print("Error posting message " + str(e))

threadlist = []
i = 0
while(i<10):
  threadlist.append(Thread(target=send_message_to_slack(i)))
  i+=1


for t in threadlist:
  t.start()

for t in threadlist:
  t.join()

f.close()