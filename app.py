# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import shelve
import config
import send_msg

import requests
import pymessenger
from flask import Flask, request

app = Flask(__name__)
bot = pymessenger.Bot(config.PAGE_ACCESS_TOKEN)
db = shelve.open("ClientRequestHistory1", writeback=True)

appeal = "appeal"
other = "other"
menu = "main"
start_button_pushed = "start_button_pushed"


@app.route('/from_siebel', methods=['GET', 'POST'])
def hello():
    found_id = ""
    found_msg = ""

    msg = re.search('<kt:X_MESSAGE_BODY>(.+?)</kt:X_MESSAGE_BODY>', str(request.data))
    if msg:
        found_msg = str(msg.group(1))

    session_id = re.search('<kt:X_SESSION_ID>(.+?)</kt:X_SESSION_ID>', str(request.data))
    if session_id:
        found_id = str(session_id.group(1))

    if found_id == "":
        return "Session Id was empty! Nothing was sent to client.", 200
    elif found_msg == "":
        return "Message was empty! Nothing was sent to client.", 200
    else:
        bot.send_text_message(found_id, found_msg)
        log('message send to: ' + found_id + ' ' + found_msg)
        return "Message successfully sent to client.", 200


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == config.VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    #log(str(data))

    db = shelve.open("ClientRequestHistory1", writeback=True)

    if data["object"] == "page":
        for entry in data["entry"]:
            if entry.get("changes"):
                for changes_event in entry["changes"]:
                    if changes_event.get("field"):
                        log("--field-- "+changes_event.get("field"))
            if entry.get("messaging"):
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("sender"):
                        # start_msg()
                        start_button()
                        sender_id = messaging_event["sender"]["id"]
                        log("--sender " + sender_id)
                        if str(sender_id) not in db:
                            db[str(sender_id)] = 'endd'
                            db[str(sender_id+'_phone')] = str('not')
                            #log(sender_id + ' set to endd')

                        if sender_id != "716102388568840":
                            if messaging_event.get("postback"):
                                log("--postback")
                                payload = messaging_event["postback"]["payload"]
                                if payload == start_button_pushed:
                                    db[str(sender_id)] = 'endd'
                                    #log(sender_id + ' set to endd')
                                    log(sender_id + " " + db[str(sender_id)])
                                    bot.send_text_message(sender_id, config.GreetingMessageLine)
                                    send_quick_message(sender_id, config.WelcomeMessageLineAll)
                                db.close()
                                return "ok", 200

                            if messaging_event.get("message"):
                                log("--message")
                                if messaging_event.get("message").get("quick_reply"):
                                    if messaging_event["message"]["quick_reply"]["payload"] == appeal:  #выбрано создать обращение
                                        db[str(sender_id)] = 'start'
                                        log(appeal)
                                        #log(sender_id + ' set to start')
                                        log(sender_id + " " + db[str(sender_id)])
                                        bot.send_text_message(sender_id, config.RequestMessageLineAll)
                                    if messaging_event["message"]["quick_reply"]["payload"] == other:   #выбрано другие услуги
                                        log(other)
                                        send_quick_message_template(sender_id, config.OtherServicesLine1)
                                    if messaging_event["message"]["quick_reply"]["payload"] == menu:    #выбрано перейти в главное меню
                                        log(menu)
                                        db[str(sender_id)] = 'endd'
                                        #log(sender_id + ' set to endd')
                                        db[str(sender_id+'_phone')] = str('not')
                                        log(sender_id + '_phone deleted')
                                        log(sender_id + " " + db[str(sender_id)])
                                        send_quick_message(sender_id, config.WelcomeMessageLineAll)
                                    db.close()
                                    return "ok", 200

                                elif messaging_event.get("message").get("text"):
                                    message_text = messaging_event["message"]["text"]
                                    log("--text")
                                    log(message_text.encode('utf-8'))

                                    log("if in db-----text")
                                    if str(sender_id) in db:
                                        log("if start-----text")
                                        log(str(sender_id) + " " + db[str(sender_id)])
                                        if db[str(sender_id)] == str("start"):
                                            if str(sender_id+'_phone') in db:
                                                ph = db[str(sender_id)+"_phone"]
                                                if ph == str('not'):
                                                    log(str(sender_id)+"_phone"+' IS_EMPTY')
                                                    if check_phone(message_text) == 1:
                                                        db[str(sender_id)+"_phone"] = str(message_text)
                                                        log(db[str(sender_id)+"_phone"] + ' saved')
                                                        bot.send_text_message(sender_id, config.RequestMessageLine4)
                                                    else:
                                                        log('It is not a phone number!')
                                                        main_menu(sender_id, config.SendPhoneRertyMessageLineAll)
                                                else:
                                                    log(str(sender_id)+"_phone"+' IS_NOT_EMPTY')
                                                    # send message
                                                    send_msg.send(db[str(sender_id+"_phone")], message_text.encode('utf-8'), sender_id)
                                                    log(sender_id + '_phone sent')
                                                    db[str(sender_id)] = 'endd'
                                                    log(sender_id + ' set to endd')
                                                    db[str(sender_id)+'_phone'] = 'not'
                                                    log(sender_id + '_phone deleted')
                                                    send_quick_message(sender_id, config.AddRequestMessageLineAll)
                                        else:
                                            send_quick_message(sender_id, config.WelcomeMessageLineAll)
                                        db.close()
                                        return "ok", 200

                                    send_quick_message(sender_id, config.WelcomeMessageLineAll)
                                    db.close()
                                    return "ok", 200

                                elif messaging_event.get("message").get("attachments"):
                                    log("if in db-----attach")
                                    if str(sender_id) in db:
                                        log("if start-----attach")
                                        log(sender_id + " " + db[str(sender_id)])
                                        if db[str(sender_id)] == "start":
                                            main_menu(sender_id, config.SendRertyMessageLineAll)
                                        else:
                                            send_quick_message(sender_id, config.WelcomeMessageLineAll)
                                        db.close()
                                        return "ok", 200
                                    else:
                                        send_quick_message(sender_id, config.WelcomeMessageLineAll)
                                        db.close()
                                        return "ok", 200

                            if messaging_event.get("delivery"):  # delivery confirmation
                                log("--------------------------------------------------delivery")

                            if messaging_event.get("option"):  # optin confirmation
                                log("--------------------------------------------------option")
    db.close()
    return "ok", 200


def check_phone(msg):
    pattern = re.compile('^\+?[87][-\(]?\d{3}\)?-? ?\d{3}-? ?\d{2}-? ?\d{2}$')
    if pattern.search(msg):
        log('phone OK')
        return 1
    else:
        log('phone NO')
        return 0


def simulate(recipient_id):
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient":{
            "id": recipient_id
        },
        "sender_action":"typing_on"
    })
    r = requests.post("https://graph.facebook.com/v2.8/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def start_msg():
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "setting_type": "greeting",
        "greeting":[
        {
          "locale":"default",
          "text": config.GreetingMessageLine1
        }
  ]
    })
    r = requests.post("https://graph.facebook.com/v2.8/me/thread_settings", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def start_button():
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "setting_type": "call_to_actions",
        "thread_state": "new_thread",
        "call_to_actions": [
            {
                "payload": start_button_pushed
            }
        ]
    })
    r = requests.post("https://graph.facebook.com/v2.8/me/thread_settings", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_quick_message(recipient_id, text):
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": config.CreateAppeal,
                    "payload": appeal
                },
                {
                    "content_type": "text",
                    "title": config.OtherServices,
                    "payload": other
                }
        ]}
    })

    r = requests.post("https://graph.facebook.com/v2.8/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_quick_message_template(recipient_id, text):
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": config.CreateAppeal,
                    "payload": appeal
                },
                {
                    "content_type": "text",
                    "title": config.OtherServices,
                    "payload": other
                }
            ],
            "attachment":{
                "type":"template",
                "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type":"web_url",
                        "url":config.link,
                        "title":config.GoToWebPage
                    }
                ]}
            }
        }
    })

    r = requests.post("https://graph.facebook.com/v2.8/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def main_menu(recipient_id, text):
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": config.GoToMainMenu,
                    "payload": menu
                }
        ]}
    })

    r = requests.post("https://graph.facebook.com/v2.8/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(host=config.WEBHOOK_LISTEN, port=config.WEBHOOK_PORT)

