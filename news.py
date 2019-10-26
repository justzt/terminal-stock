# -*- coding: utf-8 -*-
import time

import requests
import json

cnstockHistoryNews = ''
xueqiuHistoryNews = ''
gasautoHistoryNews = ''
pageSize = 10


def newsList():
    global cnstockHistoryNews, pageSize

    if cnstockHistoryNews == '':
        pageSize = 50
    url = 'http://xcx.cnstock.com/a/column/getList'
    headers = {'Host': 'xcx.cnstock.com', 'Accept': '*/*',
               'User-Agent': 'SZBAPPUA_ios_2.0.6_59545C1A-6FCE-4F06-ADF3-B3449E920F45_iPhone XS',
               'Accept-Language': 'zh-Hans-CN;q=1'}
    data = {'channel': 'szkx', 'pageNo': '1', 'pageSize': pageSize}
    ctx = requests.post(url=url, headers=headers, data=data)
    ctx.encoding = "utf8"
    result = ctx.text
    dic = json.loads(result)
    news = (dic['data'])['list']
    message = ''
    for i, value in enumerate(news):
        desc = value['desc']
        url = value['shareUrl']
        if desc in cnstockHistoryNews:
            break
        message += desc + '\n' + url + '\n \n'

    if len(message) > 0:
        message += '--cnstock'
        sendMessage(message)
        cnstockHistoryNews = message


def sendMessage(msg):
    headers = {'Content-Type': 'application/json'}
    data = {"msgtype": "text", "text": {"content": msg}}
    url = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=aeb56a85f0413588e1c91332588d2bae86f19b627aae6f4978116786641dfb7f '
    try:
        result = requests.post(url=url, data=json.dumps(data), headers=headers, json=data)
    except Exception as e:
        print(e)


def xueqiunews():
    global xueqiuHistoryNews
    url = 'http://182.92.251.113/v4/statuses/public_timeline_by_category.json?category=6&count=8'
    headers = {'Host': 'api.xueqiu.com',
               'Cookie': 'xq_a_token=119545a68bcdcf6bc76532cad62a2dc4bb78f993;u=4199262269',
               'User-Agent': 'PostmanRuntime/7.18.0'}
    ctx = requests.get(url=url, headers=headers)
    ctx.encoding = "utf8"
    result = ctx.text
    dic = json.loads(result)
    news = dic['list']
    message = ''
    for i, value in enumerate(news):
        data = value['data']
        data = json.loads(data)
        text = data['text']
        if text in xueqiuHistoryNews:
            break
        message += text + '\n \n'

    if len(message) > 0:
        message += '--雪球'
        sendMessage(message)
        xueqiuHistoryNews = message


def gasautoNewsList():
    global gasautoHistoryNews
    url = 'http://api.gasgoo.com/api/news/v2/get_home_list/1?issuetime='
    headers = {'Host': 'api.gasgoo.com', 'User-Agent': 'User-Agent: 1.1.2 (iPhone; iOS 13.1.3; zh_CN)'}
    ctx = requests.get(url=url, headers=headers)
    ctx.encoding = "utf8"
    result = ctx.text
    dic = json.loads(result)
    news = dic['list']
    message = ''
    for i, value in enumerate(news):
        # data = json.loads(value)
        text = value['Title']
        detailId = value['ArticleId']
        if text in gasautoHistoryNews:
            break
        detailUrl = 'https://m.gasgoo.com/news/{}.html'.format(detailId)
        message += text + '\n '+detailUrl+'\n\n'

    if len(message) > 0:
        message += '--盖世'
        sendMessage(message)
        gasautoHistoryNews = message


if __name__ == '__main__':

    while 1:
        newsList()
        xueqiunews()
        gasautoNewsList()
        time.sleep(60*2)
