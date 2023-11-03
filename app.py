import slack
import os
import json
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
from controllers.langchain_helper import llm_chain
from datetime import datetime
from controllers.users import handle_new_user, update_balance
from icecream import ic
from db import transactions_collection, users_collection
from helper import hash_generator

SLACK_BOT_API_KEY = os.environ['SLACK_BOT_API_KEY']
SIGNING_SECRET = os.environ['SIGNING_SECRET']

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SIGNING_SECRET,'/slack/events', app)

client = slack.WebClient(token=SLACK_BOT_API_KEY)
BOT_ID = client.api_call("auth.test")['user_id']



@slack_events_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    app_id = event.get('app_id')
    bot_id = event.get('bot_id')
    client_msg_id = event.get('client_msg_id')
    text = event.get('text')
    text = text.replace("\n", " ")
    ic(event)
    if user_id != None and user_id != BOT_ID and app_id == None and bot_id == None and client_msg_id != None :
        if transaction_details := transactions_collection.find_one({"client_msg_id": client_msg_id},{"_id": 0}):
            pass
            # client.chat_postMessage(channel=channel_id, text="This Shows that a duplicate request was sent to the Slack Webhook Again.")
        else:
            handle_new_user(user_id)
            result = llm_chain.run(text)
            try:
                result_lst = json.loads(result)
                data = {
                    "client_msg_id": client_msg_id,
                    "user_id": user_id,
                    "text": text,
                    "channel_id": channel_id,
                    "transactions": result_lst,
                    "datetime": datetime.now(),
                    }
                transactions_collection.insert_one(data)
                update_balance(user_id, result_lst)
                client.chat_postMessage(channel=channel_id, text="Transaction Recorded")
                if user_details := users_collection.find_one({"user_id": user_id}, {"_id": 0}):
                    balance = user_details.get("balance")
                    client.chat_postMessage(channel=channel_id, text=f"You current balance is {balance}")
            except Exception as e:
                client.chat_postMessage(channel=channel_id, text="Failed to record transaction! Please rewrite!")

@app.route("/slack/balance", methods=['POST'])
def show_balance():
    form_data = request.form
    channel_id = form_data.get('channel_id')
    user_id = form_data.get('user_id')
    trigger_id = form_data.get('trigger_id')
    command = form_data.get('command')
    data = {
    "trigger_id": trigger_id,
    "user_id": user_id,
    "command": command,
    "channel_id": channel_id,
    }
    balance = 0
    if user_details := users_collection.find_one({"user_id": user_id}, {"_id": 0}):
        balance = user_details.get("balance")
    return f"You current balance is {balance}"