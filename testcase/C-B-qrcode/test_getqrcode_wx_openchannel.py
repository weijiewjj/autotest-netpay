import json

import datetime
import random
import unittest
from _sha256 import sha256

import qrcode
import requests
from _md5 import md5

from PIL import Image

from config.netpaytools import SignDispose
url = "https://qr-test2.chinaums.com/netpay-route-server/api/"
billNo = str(random.randrange(1122334455667788, 999999999999999999999999999999))
class GetOnceCodeOpenchannel(unittest.TestCase):
    now_time= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_date=datetime.datetime.now().strftime('%Y-%m-%d')
    encryption='SHA256'
    signkey = "1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"


    def testgetOnceQRCode(self):
        """ 获取一次性二维码，并发起转清微信渠道支付"""
        payload = "{\"mid\":\"898310077778888\"," \
                  "\"msgSrc\":\"NETPAY\"," \
                  "\"msgType\":\"bills.getQRCode\"," \
                  "\"notifyUrl\":\"http://www.baidu3.com\"," \
                  "\"orderDesc\":\"测试交易\"," \
                  "\"requestTimestamp\":\"" + self.now_time + "\"," \
                                                         "\"billNo\":\"" + billNo + "\"," \
                                                                                    "\"totalAmount\":\"1\",\"tid\":\"00000001\"," \
                                                                                    "\"instMid\":\"QRPAYDEFAULT\"}"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "e86a132b-d502-4ae4-b4e5-b2ebd2360df1"
        }
        payloaddict = SignDispose.getSignDict(SignDispose(), json.loads(payload), self.signkey,'MD5')
        payload = str(payloaddict)
        response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
        #print(response.text)
        img = qrcode.make(response.json().get("billQRCode"))
        img.save("./onceqrcode.png")
        image = Image.open("./onceqrcode.png")
        image.resize((360, 360)).show()

    def testQRCodeQuery(self):
        """  发起二维码支付结果查询，查询成功 """
        queryload={'msgType':'bills.query',
                 'msgSrc':'NETPAY',
                 'mid':'898310077778888',
                 'billDate':self.now_date,
                 'billNo':billNo,
                 'tid':'12345678',
                 'instMid':'QRPAYDEFAULT',

                 'requestTimestamp':self.now_time,

                 'signType':'SHA256'
                }
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "d7c1fc99-98e7-4c7c-8d3e-6d859ecaeeeb"
            }
        queryloaddict = SignDispose.getSignDict(SignDispose(), queryload, self.signkey,self.encryption)
        response = requests.request("POST", url, data=str(queryloaddict), headers=headers)
        print(response.text)
        self.assertEqual(response.json().get("errCode"),"SUCCESS","支付成功，查询成功")

    def testQRCodeRefund(self):
        """ 微信转清渠道二维码交易发起退货交易"""
        refunddict={
            "msgType": "bills.refund",
            "msgSrc": "NETPAY",
            "mid": "898310077778888",
            "billDate": self.now_date,
            "billNo": billNo,
            "refundAmount": "1",
            "tid": "12345678",
            "instMid": "QRPAYDEFAULT",
            "msgId": "1234567890",
            "requestTimestamp": self.now_time,
            "signType": "SHA256"

        }

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "85ced8b8-2144-4f56-b0c7-e17e4949d6a7"
        }

        refunddict=SignDispose.getSignDict(SignDispose(),refunddict,self.signkey,'SHA256')
        response = requests.request("POST", url, data=str(refunddict), headers=headers)
        self.assertEqual(response.json().get("errCode"), "SUCCESS", "退货成功")
        print(response.text)


