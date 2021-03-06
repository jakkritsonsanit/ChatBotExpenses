#!/usr/bin/python
# -*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import numpy as np
import sys

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageSendMessage, StickerSendMessage,
    AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

sys.path.insert(1, '../src/')
import function

app = Flask(__name__)

lineaccesstoken = 'L/k6gLuWfGzRK3zrWqC7oOYaAOcm7dn/YIQoSZDLx0wlfAU21LSTjY+wXTHheNuHgzmoGUrtWi1SU419k6aF8p63von1KzMQyFW2jQyYln39Ih6UPdqqgAx6mYhXAL/FV9ivYAOK9lc0hTcKX3B6QwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)


####################### new ########################
@app.route('/')
def index():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False, cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '', 200


def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1, 17)
        replyObj = StickerSendMessage(package_id=str(1), sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''

    try:
        if msgType == "text":
            msg = str(event["message"]["text"])
            function.main(msg)
            replyObj = TextSendMessage(text='เรียบร้อยครับ')
            line_bot_api.reply_message(rtoken, replyObj)

        else:
            sk_id = np.random.randint(1, 17)
            replyObj = StickerSendMessage(package_id=str(1), sticker_id=str(sk_id))
            line_bot_api.reply_message(rtoken, replyObj)
    except:
        print('error cannot reply msg')
        replyObj_sk = StickerSendMessage(package_id=str(11537), sticker_id=str(52002755))
        line_bot_api.reply_message(rtoken, replyObj_sk)
        replyObj_txt = TextSendMessage(text='ระบบขัดข้อง')
        line_bot_api.reply_message(rtoken, replyObj_txt)

    return ''


if __name__ == '__main__':
    app.run(debug=True)
