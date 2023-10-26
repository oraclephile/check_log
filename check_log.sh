####################################################
# Copyright (C) 2022 ==ZHANG FEI== All rights reserved.
# File Name: check_log.sh
# Author: ZHANG FEI
# mail:chonphile@gmail.com
#Created Time:五  8/12 16:11:33 2022
####################################################
#!/bin/bash
#获取当前时间戳
set -ex
_min_num=$1
_log_num=$2
_now_timeStamp=$(date +%s)

#获取当前时间分钟数
#_now_min=`date -r 1649407783 "+%Y-%m-%d %H:%M"`

echo "${_now_timeStamp}"
#echo ${_now_min}
#获取文件后缀
function FileSuffix() {
     local filename="$1"
     if [ -n "$filename" ]; then
         echo "${filename##*.}"
     fi
}

#获取文件前缀
function FilePrefix() {
     local filename="$1"
     if [ -n "$filename" ]; then
         echo "${filename%.*}"
     fi
}

#判定文件后缀
function IsSuffix() {
     local filename="$1"
     local suffix="$2"
     if [ "$(FileSuffix "${filename}")" = "$suffix" ]; then
         return 0
     else
         return 1
     fi
}

#判定文件前缀
function IsPrefix() {
     local filename="$1"
     local prefix="$2"
     if [ "$(FilePrefix "${filename}")" = "$prefix" ]; then
         return 0
     else
         return 1
     fi
}
#判断操作系统
function get_os() {
  a=$(uname  -a)
  b="Darwin"
  c="centos"
  d="ubuntu"
  if [[ $a =~ $b ]];then
      echo "mac"
  elif [[ $a =~ $c ]];then
      echo "centos"
  elif [[ $a =~ $d ]];then
      echo "ubuntu"
  else
      echo $a
  fi
}
#获取分钟字符串
function get_now_min() {
    os=$(get_os)
    if [[ ${os} =~ "mac" ]]; then
      _now_min=$(date -r "${1}" "+%Y-%m-%d %H:%M")
    else
      _now_min=$(date -d @"${1}"  "+%Y-%m-%d %H:%M")
    fi
    echo ${_now_min}
}
#不同操作系统获取临时分钟时间字符串_tmp_
function get_min_tmp() {
    os=$(get_os)
    if [[ ${os} =~ "mac" ]]; then
      _now_min=$(date -r "${1}" "+%Y%m%d%H%M")
    else
      _now_min=$(date -d @"${1}"  "+%Y%m%d%H%M")
    fi
    echo "${_now_min}"
}
function get_xmins_ago () {
    _min_num=$1
    os=$(get_os)
    if [[ ${os} =~ "mac" ]]; then
      _xmins_ago_timeStamp=$(($_now_timeStamp-$_min_num*60))
    else
      _xmins_ago_timeStamp=$(($_now_timeStamp-$_min_num*60))
    fi
    #_x=`expr $_now_timeStamp-$_min_num*60`
    #echo $_xmins_ago_timeStamp
    get_now_min $_xmins_ago_timeStamp
}
#按分钟设置临时文件名称
function get_xmins_ago_tmp_file () {
    _min_num=$1
    os=`get_os`
    if [[ ${os} =~ "mac" ]]; then
      _xmins_ago_timeStamp=$(($_now_timeStamp-$_min_num*60))
    else
      _xmins_ago_timeStamp=$(($_now_timeStamp-$_min_num*60))
    fi
    #_x=`expr $_now_timeStamp-$_min_num*60`
    #echo $_xmins_ago_timeStamp
    _t=`get_min_tmp $_xmins_ago_timeStamp`

    echo $_t
}
function build_tmp_error_file () {
  for (( i = 0; i <= $_min_num; i++ ))
    do
    echo $i
    _t=$(get_xmins_ago ${i})
    echo "当前时间："$_t
    _f=$(get_xmins_ago_tmp_file ${i})
    echo "##########_f"$_f
    #tail -n $_log_num $1 |awk '{if($4=="Error" || $4=="ERROR" || $4=="error"){print $0}}' > "/tmp/"$_f
    #tail -n $_log_num $1|grep "$_t" |awk '{if($4=="ERROR"){print $0}}' > "/tmp/"$_f
    touch "/tmp/_tmp_."$_f
    #_t_log=`tail -n $_log_num $1|grep "$_t"`
    if [[ -z `tail -n $_log_num $1|awk '{print $1" "$2}'|grep "$_t"` ]] || [[ `tail -n $_log_num $1|grep "$_t"` = "" ]];then
	echo "当前时间没有错误日志"
    else
    	tail -n $_log_num $1|grep "$_t" > "/tmp/_tmp_."$_f
    fi
  done
}
#清理前置的临时文件
function clean_tmp_file () {
  /bin/rm -rf /tmp/_tmp_*
}
#根据实际情况报警
function call_110 () {
  _host=$(hostname)
  while read line
  do
    _app=$(echo $line | awk -F " " '{print $1}')     #获取变量
    _log=$(echo $line | awk -F " " '{print $2}')
    clean_tmp_file
    build_tmp_error_file "$_log"
    _message=$(cat /tmp/_tmp_.*)
    #不区分大小写
    #_total=$(echo "$_message"|grep -iw error |wc -l)
    #区分大小写
    _total=$(echo "$_message"|grep ERROR |wc -l)
    #echo $_message
    echo "_app:"$_app
    echo "_log:"$_log
    echo "_total:"$_total
    #python3 onekey110.py 127.0.0.1 测试主机 测试报警 10
    if [ $_total -gt 0 ];then
      python3 onekey110.py $_host $_app $_total
    fi
  done <apps.txt
}
call_110
