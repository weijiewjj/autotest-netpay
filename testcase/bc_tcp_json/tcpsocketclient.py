import json
import random
import unittest
from socket import *

import datetime

from config.netpaytools import SignDispose

HOST ="172.30.252.169"

PORT = 9087

BUFFSIZE=2048

signkey="X2Z6zKRkxxcSzM746mJj6i545rTmaQWzyKirWzHyBcYJtwQZ"

ADDR = (HOST,PORT)

class TCPBar(unittest.TestCase):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mer_orderId = str(random.randrange(1122334455667788, 999999999999999999999999999999))
    #mer_orderId ="87119723068124819109156591090"

    def testbarPay(self):
        tcpClient = socket(AF_INET,SOCK_STREAM)

        tcpClient.connect(ADDR)
        authcode=input("请扫描条码：")
        print("条码是："+authcode)
        data = {'msgType': 'pay',
                       'requestTimestamp':self.now_time,
                       'msgSrc':'ULINK',
                       'msgId':'02S221X0000004992435124935',
                       'mid':'898310077779999',
                       'tid':'00810001',
                       'barCode':authcode,
                       'instMid':'POSTONGDEFAULT',
                       'totalAmount':'1',
                       'refId':'00004992435W',
                       'orderDesc':'xyz',
                       'merOrderId':self.mer_orderId
                       }
        readydata=SignDispose.getSignDict(SignDispose(),data,signkey,"MD5")
        len=str(readydata).__len__()
        print(len)
        #对于纯数字，可以用格式化方法补0
        s = "%08d" % len
        print(s)

        #对于string，使用zfill()方法补0
        #开始发送接收报文...
        tcpClient.send((str(len).zfill(8)+str(readydata)).encode("gbk"))
        responseMessage = tcpClient.recv(BUFFSIZE).decode("gbk")
        responseMessage=responseMessage[8:]
        print(responseMessage)
        print(json.loads(responseMessage).get("errCode"))
        self.assertEqual(json.loads(responseMessage).get("errCode"), "SUCCESS", "pay-CASE fail")

        tcpClient.close()

    def testbarvoid(self):
        tcpClient = socket(AF_INET, SOCK_STREAM)

        tcpClient.connect(ADDR)
        voiddict={
            "merOrderId":self.mer_orderId,
            "mid":"898310077779999",
            "msgSrc":"ULINK",
            "msgType":"cancel",
            "requestTimestamp":self.now_time,
            "tid":"00810001"
        }
        voiddata = SignDispose.getSignDict(SignDispose(), voiddict, signkey, "MD5")
        len = str(voiddata).__len__()


        #begin to send message:
        tcpClient.send((str(len).zfill(8)+str(voiddata)).encode("gbk"))
        responseMessage = tcpClient.recv(BUFFSIZE).decode("gbk")
        responseMessage = responseMessage[8:]
        print(responseMessage)
        self.assertEqual(json.loads(responseMessage).get("errCode"),"SUCCESS","void-CASE fail")
        tcpClient.close()



