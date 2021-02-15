from flask import Flask, request
from response import send_message
import os, re

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get('FACEBOOK_VERIFY_TOKEN')


def predined_response(message):
    """This is a predefined list of enquiries from the customer."""
    if message == r'[Hh]i':
        return 'Hello, welcome to GD Test. How can I help you?' 
    elif message == 'genuine':
        return 'Yes all our products are genuine'
    elif message == 'stock':
        return 'Hold on please, let me check'
    else:
        return 'Thank you for your time'

def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = predined_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

@app.route("/",methods=['GET','POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"
