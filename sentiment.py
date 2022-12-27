from flask import Flask, request
from google.cloud import language_v1
from datetime import datetime
import json
import requests
from google.cloud import firestore

# Create a Firestore client
db = firestore.Client()
app = Flask(__name__)

webhook_url = "https://api.github.com/repos/askabderon/askabderon.github.io/issues"
auth_token = "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"
f = open("a.txt", "a")

@app.route('/check-sentence', methods=['POST'])
def check_sentence():
    # Extract the sentence from the request data
    data = json.loads(request.json)
    sentence = data['body']
    title = data['title']

    # Set up the Google Cloud Natural Language API client
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"

    # Create a document object with the sentence
    document = {"content": sentence, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF32
    # Check for inappropriate language in the document
    response = client.analyze_sentiment(request={"document": document, "encoding_type": encoding_type})
    sentiment = response.document_sentiment
    userId = title.split('\'')[0]
    doc_ref = db.collection('users').document(userId)
    print('userrr ',userId)
    doc_ref.update({'scores': firestore.ArrayUnion([sentiment.score])})
    print(sentiment.score)
    if(sentiment.score > -0.3):
        # Set the request headers
        headers = {
            "Authorization": f"token {auth_token}",
            "Content-Type": "application/json",
        }

        # Set the request payload
        payload = {
            "title": title,
            "body": sentence,
        }

        # Send the POST request to create the issue
        response = requests.post(webhook_url, json=payload, headers=headers)
        dt = datetime.now()
        f.write(str(sentence) + " " + str(datetime.timestamp(dt)) + "\n")
    return 'OK'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
