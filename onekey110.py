#!/usr/bin/python
# -*- coding:utf-8 -*-
####################################################
#Version: 2.0
# Copyright (C) 2022 ==ZHANG FEI== All rights reserved.
# File Name: onekey110.py
# Author: ZHANG FEI
# mail:chonphile@gmail.com
# Created Time:四  8/18 13:39:39 2022
# changed Time:2023-08-23 15:40:30 version2.0-钉钉加入[张策]
####################################################
from datetime import datetime
import logging
import os.path
import time
import hmac
from base64 import b64encode
from hashlib import sha256
from json import dumps
from urllib import parse
from requests import post  # conda install requests


# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H', time.localtime(time.time()))
log_path = os.getcwd() + '/logs/'
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_name = log_path + '_localcheck_' + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
fh.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"))
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

#2.0加入钉钉代码开始
# 网址
URL = 'https://oapi.dingtalk.com/robot/send?'
# 群标识
ACCESS_TOKEN = 'xxxxxxxxxxxxxxxx'
# 加签
SIGN = 'xxxxxxxxxxxxxxx'
# 请求头
HEADERS = {'content-type': 'application/json'}


def get_params():
    # 钉钉文档-加签方法：https://open.dingtalk.com/document/robots/customize-robot-security-settings
    timestamp = str(round(time.time() * 1000))
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


def dosend(content):
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
#2.0加入钉钉代码结束

now = datetime.now().strftime("%Y年%m月%d日 %H时%M分")
userList=[
        #要给谁报警就填谁的，一行一个
    {"name":"张三","mail":"zhangsan@gmail.com","phone":"18988888888"},
    {"name":"李四","mail":"lisi@gmail.com","phone":"13588888888"},
         ]

def call(name,phone,hostname,app,message):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkdyvmsapi.request.v20170525.SingleCallByTtsRequest import SingleCallByTtsRequest
    client = AcsClient('xxxxxxxxxxxxx', 'xxxxxxxxxxxxxxx', 'cn-hangzhou')
    name = name
    hostname = hostname
    app = app
    message = message

    policeMainframe = "主机"+hostname+"上的"+app+"应用"+message
    request = SingleCallByTtsRequest()
    request.set_accept_format('json')

    request.set_CalledNumber(phone)
    request.set_TtsCode("TTS_xxxxxxxxxxx")
    #request.set_CalledShowNumber("02088322629")
    request.set_TtsParam("{\"name\":\""+name+"\",\"hostname\":\""+policeMainframe+"\"}")
    print ("{\"name\":\""+name+"\",\"policeMainframe\":\""+policeMainframe+"\"}")

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))

def mail(mails,now,total,hostname,app):
    import yagmail
    now=now
    message = contents()
    try:
        yagmail.SMTP(user="xxxxxxxx",
                password="xxxxxxxxx",
                host='smtp.qiye.aliyun.com').send(
                mails,
                subject='GN-%s日志异常请及时检查'%app,
                contents =
                "<font size=2 color='red'>时间区间：%s</font>\n"
                "<font size=2 color='red'>报错总数：%s</font>\n"
                "<font size=2 color='red'>主机名称：%s</font>\n"
                "<u><font size=3 color='green'>_____详情如下(若触发流控可能只发送邮件而没有电话和短信告警)_____</font></u>\n<font size=1>%s</font>"
                ''%(now,total,hostname,message)
            )
    except Exception as e :
        print(str(mails)+" " + e)

def message(host,server,exc):
    import json
    msg = {}
    msg["date"] = now
    msg["host"] = host
    msg["server"] = server
    msg["exc"] = exc
    msg_json = json.dumps(msg)
    print(msg_json)
    return msg_json

def sendsms(phone,smsinfo):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    client = AcsClient('xxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxx', 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "xxxxxxxxxx")
    request.add_query_param('TemplateCode', "xxxxxxxxxxxxxxx")
    request.add_query_param('TemplateParam', smsinfo)
    response = client.do_action(request)
    print(str(response, encoding='utf-8'))

def contents():
    import os
    pathlog = "/tmp/"
    dataset = []
    files = os.listdir(pathlog)
    for _f in files:
        if '_tmp_.' in _f:
            print ("Found it! " + _f)
            with open("/tmp/%s"%_f, "r") as f:
                lines = f.readlines()
                for line in lines:
                    dataset.append(line)
                    f.close()
    return str(dataset)

if __name__ == '__main__':
    import sys
    _host = sys.argv[1]
    _app = sys.argv[2]
    _total = sys.argv[3]
    print("#"*25)
    print("_host:%s"%_host)
    print("_app:%s"%_app)
    print("_total:%s"%_total)
    mails = []
    for u in userList:
        print(u.get('name'))
        print(u.get('mail'))
        print(u.get('phone'))
        mails.append(u.get('mail'))
  #      logger.info('[%s] 电活告警 %s %s %s %s %s'%(now,u.get('name'),u.get('phone'),_host,_app,'错误日志'))
  #      logger.info('[%s] 电活告警 %s'%(now,call(u.get('name'),u.get('phone'),_host,_app,'错误日志')))
        logger.info('[%s] 短信告警 %s %s %s %s %s'%(now,u.get('name'),u.get('phone'),_host,_app,'错误日志'))
        logger.info('[%s] 短信告警 %s'%(now,sendsms(u.get('phone'),message(_host,_app,'错误日志'))))
    #    
    logger.info('[%s] 邮件告警 %s %s %s %s'%(now,u.get('name'),u.get('phone'),_host,_app))
    mail(mails,now,_total,_host,_app)
    #2.0钉钉加入开始
    dosend('%s\n报错总数:%s\n主机名称:%s\n%s\n详情如下:\n%s'%(now,_total,_host,_app,contents()))
    #2.0钉钉加入结束
