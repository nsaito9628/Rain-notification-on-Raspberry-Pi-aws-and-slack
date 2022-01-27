#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
from datetime import datetime, timezone, timedelta

URL = os.environ['URL']
JST = timezone(timedelta(hours=+9), 'JST')

def post_slack():
    now = datetime.now(JST).strftime('%H:%M')

     #各ワークスペースでWebhook URLを設定
    post_url = URL #各ワークスペースでWebhook URLを設定

    requests.post(post_url, data=json.dumps(
                    {
                    "username": "雨が降ってきましたよ!",
                    'text': now + "に降り始めたよ=^^=;;"
                    }
                ))


def lambda_handler(event, context):
    
    t = datetime.now(JST)
    if 6 <= t.hour <=18:
        post_slack()