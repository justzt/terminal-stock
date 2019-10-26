# -*- coding: utf-8 -*-
from threading import Thread

from reprint import output
import time
import datetime
import random
from terminalColor import bcolors
import requests
import sys
import _thread
import os

mystock = {}

stocks = ''

url = "http://hq.sinajs.cn/list="

stop = 0
displayStockName = 0
colored = 0


def readData():
    f = open('my_stock.dat', 'r')
    stockList = f.read().split('\n')
    global stocks, mystock, mystockCode
    for item in stockList:
        if item != '':
            itemList = item.split()
            stocks += itemList[0] + ','
            mystock[itemList[0]] = (itemList[1], itemList[2]) if len(itemList) == 3 else None
    stocks = stocks[:-1]
    f.close()


def getTime():
    return time.strftime('%Y-%m-%d %A %p %X', time.localtime(time.time()))


def highOrLow(a, b):
    return bcolors.RED if a >= b else bcolors.GREEN


def warning(abs, color):
    if color == bcolors.RED and abs > 3:
        return bcolors.MAGENTA
    if color == bcolors.GREEN and abs <= -2:
        return bcolors.BLUE
    return color


def printStock():
    global output_lines, displayStockName, colored
    ctx = requests.get(url + stocks)
    ctx.encoding = "gb2312"
    data = ctx.text
    # print type(data)
    line = data.split('\n')
    index = 0
    # print(bcolors.WHITE+"代码      名称         昨收        今开     最高        最低       现价     涨幅      浮动数额       盈亏比例
    # 成本金额"+bcolors.ENDC)
    print(
        bcolors.WHITE + "CODE           NM         Close      Open        Hi         Low       Now        %         "
                        "Lost" + bcolors.ENDC)
    for stock in line:
        stockInfo = stock.split(',')
        if stockInfo[0]:
            # var hq_str_s_sh000001="上证指数
            temp = stockInfo[0].split('_')[2].replace('"', '').split('=')
            code = temp[0]
            name = temp[1] if displayStockName == 1 else '------'
            name = name[0:2]

            todayBeginPrice = float(stockInfo[1])
            yersterdayEndPrice = float(stockInfo[2])
            currentPrice = float(stockInfo[3])
            todayMaxPrice = float(stockInfo[4])
            todayMinPrice = float(stockInfo[5])
            abs = (currentPrice / yersterdayEndPrice - 1) * 100
            per = u'--  ' if '%.2f' % todayBeginPrice == '0.00' else ('%+.2f' % (abs)) + '%'

            # 红涨绿跌
            todayBeginPriceColor = highOrLow(todayBeginPrice, yersterdayEndPrice)
            currentPriceColor = highOrLow(currentPrice, yersterdayEndPrice)
            todayMaxPriceColor = highOrLow(todayMaxPrice, yersterdayEndPrice)
            todayMinPriceColor = highOrLow(todayMinPrice, yersterdayEndPrice)
            perColor = currentPriceColor
            perColor = warning(abs, perColor)
            if colored == 0:
                currentPriceColor = perColor = bcolors.WHITE

            stockCost = 0
            stockQuantity = 0
            floatMoney = 0
            stockRatio = 0
            floatMoneyColor = bcolors.WHITE
            randValue = u'%.2f' % random.random()
            dif = u'%.2f' % (currentPrice - yersterdayEndPrice)
            output_lines[index] = (bcolors.WHITE + "{0:<14}" + bcolors.ENDC
                                   + bcolors.WHITE + "{1:<12}" + bcolors.ENDC
                                   + bcolors.WHITE + "{2:>14}" + bcolors.ENDC
                                   + bcolors.WHITE + "{3:>10}" + bcolors.ENDC
                                   + bcolors.WHITE + "{4:>14}" + bcolors.ENDC
                                   + bcolors.WHITE + "{5:>14}" + bcolors.ENDC
                                   + currentPriceColor + "{6:>14}" + bcolors.ENDC
                                   + perColor + "{7:>14}" + bcolors.ENDC
                                   + bcolors.WHITE + "{8:>14}" + bcolors.ENDC).format(code,  # 0
                                                                                      name,  # 1
                                                                                      yersterdayEndPrice,  # 2
                                                                                      todayBeginPrice,  # 3
                                                                                      todayMaxPrice,  # 4
                                                                                      todayMinPrice,  # 5
                                                                                      currentPrice,  # 6
                                                                                      per,
                                                                                      dif
                                                                                      )

        index += 1


def reciveCmd():
    global stop, displayStockName, colored
    cmd = input("")
    print("第一个参数：" + cmd)
    if cmd == 'q':
        stop = 1
        terminate()
    elif cmd == 'n' or cmd == '1':
        cleanScreen()
        displayStockName = not displayStockName
        printStock()
    elif cmd == 'c':
        colored = not colored
    time.sleep(1)
    reciveCmd()


def cleanScreen():
    os.system("clear && printf '\e[3J'")


def terminate():
    cleanScreen()
    os._exit(1)


if __name__ == '__main__':
    readData()
    t = Thread(target=reciveCmd, args=())
    t.start()

    with output(initial_len=50, interval=0) as output_lines:
        while True:
            if stop == 1:
                terminate()
            printStock()
            time.sleep(3)
