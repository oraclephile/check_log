####################################################
# Copyright (C) 2022 ==ZHANG FEI== All rights reserved.
# File Name: init_check.sh
# Author: ZHANG FEI
# mail:chonphile@gmail.com
#Created Time:五  8/12 15:52:23 2022
####################################################
#!/bin/bash
#安装python依赖
pip3 install requests
pip3 install aliyun-python-sdk-core-v3
pip3 install aliyun-python-sdk-rds
pip3 install aliyun-python-sdk-dts
pip3 install aliyun-python-sdk-core
pip3 install aliyun-python-sdk-ecs
pip3 install aliyun-python-sdk-dyvmsapi
pip3 install yagmail
#扫描服务并初始化配置文件
ps -ef|grep java |awk -F "-Dlog.home=/www/" '{print $2}' |grep -v '^$' |awk '{print $1" /www/"$1"/logs/error.log"}' > /opt/script/check_log/apps.txt
#创建定时任务
echo "*/5 * * * * cd /opt/script/check_log && /bin/bash check_log.sh 5 40000" > /opt/script/check_log/check_log.cron
crontab /opt/script/check_log/check_log.cron
