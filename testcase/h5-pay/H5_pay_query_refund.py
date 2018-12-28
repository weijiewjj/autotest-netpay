import random
import unittest

import requests
import time

from PIL import Image

from config.createqrcodeimg import QRCodeWithLogo
from config.netpaytools import SignDispose

class TestH5PayQueryRefund(unittest.TestCase):
    """ alipay-h5-pay-refund"""
    url = "https://qr-test3.chinaums.com/netpay-portal/webpay/pay.do"
    mer_orderId = str(random.randrange(1122334455667788, 999999999999999999999999999999))
    #mer_orderId ="2018122022001478510598796503"


    signkey = "1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"
    def testH5Pay(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        querystring = {"msgType":"trade.h5Pay",
                       "merAppId":"http%3A%2F%2Fwww.wangzhenongyao.com",
                       "requestTimestamp":now_time,
                       "msgSrc":"NETPAY",
                       "mid":"898310077779999",
                       "tid":"12345678",
                       "instMid":"H5DEFAULT",
                       "totalAmount":"1",
                       "sceneType":"AND_WAP",
                       "merOrderId":self.mer_orderId,
                       "merAppName":"wangzhenongyao",
                       "returnUrl":"https://qr-test3.chinaums.com/netpay-portal/alipay2/h5Pay.do",
                       "signType":"MD5"
        }

        SignDispose.getSignDict(SignDispose(),querystring,self.signkey,"MD5")

        payload = ""
        headers = {
            'User-Agent': "MicroMessenger/4.5.255",
            'HTTP_USER_AGENT': "HTTP_USER_AGENT",
            'cache-control': "no-cache",
            'Postman-Token': "d810ccfc-58aa-43ee-ae42-c51c3151d92c"
            }

        response = requests.request("GET", self.url, data=payload, headers=headers, params=querystring)

        print(response.url)

        #将重定向链接转成二维码扫一扫，使用qycode 和 pil的高级用法
        QRCodeWithLogo.getQRCode(QRCodeWithLogo(),response.url,"h5qrcode.png","h5icon.png")
        Image.open("h5qrcode.png").resize((360, 360)).show()

    def testH5Query(self):
        """ alipay-h5-query"""
        url = "http://172.30.252.169:9078"
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')

        payload = "{\"merOrderId\":\""+self.mer_orderId+"\"," \
                  "\"mid\":\"898310077779999\"," \
                  "\"instMid\":\"H5DEFAULT\"," \
                  "\"msgSrc\":\"NETPAY\"," \
                  "\"msgType\":\"query\"," \
                  "\"requestTimestamp\":\""+now_time+"\"," \
                  "\"tid\":\"00000001\"}"
        headers = {
            'cache-control': "no-cache",
            'Postman-Token': "e4f5eb12-fdc9-44a0-9b58-ae418e92a0d5"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        self.assertEqual(response.json().get("errCode"),"SUCCESS","h5支付查询失败"+response.json().get("errCode"))

        print(response.text)
    def testH5Refund(self):
        """alipay-h5-refund"""
        url = "http://172.30.252.169:9078"
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')

        payload = "{\"merOrderId\":\""+self.mer_orderId+"\"," \
                  "\"mid\":\"898310077779999\"," \
                  "\"instMid\":\"H5DEFAULT\"," \
                  "\"msgSrc\":\"NETPAY\"," \
                  "\"msgType\":\"refund\"," \
                  "\"requestTimestamp\":\""+now_time+"\"," \
                  "\"refundAmount\":\"1\",\"tid\":\"00000001\"}"
        headers = {
            'cache-control': "no-cache",
            'Postman-Token': "67e9d5da-9b97-4f56-8c13-c4ed382382e8"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        self.assertEqual(response.json().get("errCode"), "SUCCESS", "h5支付退款失败" + response.json().get("errCode"))

        print(response.text)
