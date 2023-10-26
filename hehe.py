#!/usr/bin/python
# -*- coding:utf-8 -*-
import hmac
from base64 import b64encode
from hashlib import sha256
from json import dumps
from time import time
from urllib import parse
from requests import post  # conda install requests

# 网址
URL = 'https://oapi.dingtalk.com/robot/send?'
# 群标识
ACCESS_TOKEN = 'xxxxxxxxxxxxxxx'
# 加签
SIGN = 'xxxxxxxxxxxxx'
# 请求头
HEADERS = {'content-type': 'application/json'}


def get_params():
    # 钉钉文档-加签方法：https://open.dingtalk.com/document/robots/customize-robot-security-settings
    timestamp = str(round(time() * 1000))
    secret_enc = SIGN.encode('utf-8')
    string_to_sign_enc = '{}\n{}'.format(timestamp, SIGN).encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=sha256).digest()
    sign = parse.quote_plus(b64encode(hmac_code))
    # 返回请求参数
    return {
        'access_token': ACCESS_TOKEN,
        'sign': sign,
        'timestamp': timestamp,
    }


def send(content):
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
        },
        "at": {
            "atMobiles": [
                "钉钉手机号"
            ],
            "isAtAll": False
        },
    }
    data = dumps(data)
    print(post(url=URL, headers=HEADERS, data=data, params=get_params()))



if __name__ == '__main__':
    send('告警测试')


