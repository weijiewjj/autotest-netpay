import random
import unittest
from _md5 import md5

import datetime
from urllib.parse import urlencode

import requests

import json
#变量初始化，从配置文件中读取服务器地址
from config.netpaytools import SignDispose
from PIL import Image
from config.createqrcodeimg import QRCodeWithLogo


#cf=configparser.ConfigParser()
#cf.read("./config/config.ini")
#url=cf.get("dev","dev_portal_url")
#url2=cf.get("dev","dev_address")
url = "https://qr-test1.chinaums.com/netpay-portal/webpay/pay.do"
url2 = "http://144.131.252.39:9098"
mer_orderId = str(random.randrange(1122334455667788,999999999999999999999999999999))
#mer_orderId="281552727315189662061941739298"

class TestPublicWechatPay(unittest.TestCase):
    """ 测试支付宝渠道公众号跳转分账交易查询以及退货 """
    signkey = "1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def test_a_GetUrl_jump(self):
        """ 测试公众号跳转类页面分账并进行支付，headers需配置支付宝客户端useragent"""
        querystring = {"totalAmount":"3","msgSrc":"NETPAY","mid":"898340149000030","tid":"12345678","instMid":"QRPAYDEFAULT",
                      "merOrderId":mer_orderId,"platformAmount":"1","divisionFlag":"true","msgType":"trade.jsPay",
                     'subOrders':[{'totalAmount':'1','mid':'898310075230001'},{'totalAmount':'1','mid':'898310075230002'}]}
        # querystring = {"totalAmount": "3", "msgSrc": "NETPAY", "mid": "898340149000030", "tid": "12345678",
        #                "instMid": "QRPAYDEFAULT",
        #                "merOrderId": mer_orderId, "platformAmount": "1", "divisionFlag": "true",
        #                'subOrders': [{"totalAmount":"1","mid":"898310075230001"},
        #                              {"totalAmount":"1","mid":"898310075230002"}]}

        querystring=SignDispose.getSignDictWithSpace(SignDispose(),querystring,self.signkey,"MD5")
        #querystring = SignDispose.getSignDict(SignDispose(), querystring, self.signkey, "MD5")
        payload = ""
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; U; Android 4.2.1; zh-cn; HUAWEI G610-T00 Build/HuaweiG610-T00)AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 AlipayDefined(nt:WIFI,ws:360|640|1.5) AliApp(AP/9.0.1.073001) AlipayClient/9.0.1.073001 GCanvas/1.4.2.15",
            'cache-control': "no-cache",
            'Postman-Token': "491b8234-daa0-49d1-acea-aac6ebeb936d"
            }

        response = requests.request("GET", url, data=payload, headers=headers, params=urlencode(querystring))

        print("param is:"+str(querystring))

        print(type(response))
        assert isinstance(response,requests.models.Response)
        print(response.url)

        ##二维码的高级用法
        QRCodeWithLogo.getQRCode(QRCodeWithLogo(),response.url,"qrcode.png","alicon.png")
        Image.open("qrcode.png").resize((360,360)).show()



    def test_b_Querypay(self):
        """ 支付宝支付过的交易进行查询"""
        payquery= "{\"merOrderId\":\""+mer_orderId+"\"," \
          "\"mid\":\"898340149000030\"," \
          "\"msgSrc\":\"NETPAY\"," \
          "\"msgType\":\"query\"," \
          "\"requestTimestamp\":\""+self.now_time+"\"," \
          "\"tid\":\"00000001\"}"
        headers = {
        'cache-control': "no-cache",
        'Postman-Token': "37db237c-1d7a-4e70-9179-fa4b7ae27559"
        }
        payquerydict = SignDispose.getSignDict(SignDispose(), json.loads(payquery), self.signkey, 'MD5')
        response = requests.request("POST", url2, data=str(payquerydict), headers=headers)
        print(response.text)
        self.assertEqual(response.json().get("errCode"),"SUCCESS","查询失败")

    def test_c_Refund_1(self):
        """ 支付宝公众号支付进行退货交易"""
        refunddict={
            "msgType": "refund",
            "msgSrc": "NETPAY",
            "mid": "898340149000030",
            "merOrderId": mer_orderId,
            "refundAmount": "2",

            "tid": "12345678",
            "instMid": "QRPAYDEFAULT",
            "platformAmount":"1",
            "msgId": "1234567890",
            "requestTimestamp": self.now_time,
            "signType": "SHA256",
            "subOrders": [{'totalAmount': '1', 'mid': '898310075230002'}]
        }

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "85ced8b8-2144-4f56-b0c7-e17e4949d6a7"
        }

        refunddict=SignDispose.getSignDict(SignDispose(),refunddict,self.signkey,'SHA256')
        response = requests.request("POST", url2, data=str(refunddict), headers=headers)
        print(refunddict)
        print(response.text)
        self.assertEqual(response.json().get("errCode"), "SUCCESS","微信公众号渠道退款失败")

    def test_c_Refund_2(self):
        """ 支付宝渠道公众号支付进行退货交易"""
        refunddict={
            "msgType": "refund",
            "msgSrc": "NETPAY",
            "mid": "898340149000030",
            "merOrderId": mer_orderId,
            "refundAmount": "1",

            "tid": "12345678",
            "instMid": "QRPAYDEFAULT",
            "platformAmount":"0",
            "msgId": "1234567890",
            "requestTimestamp": self.now_time,
            "signType": "SHA256",
            "subOrders": [{'totalAmount': '1', 'mid': '898310075230001'}]
        }

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "85ced8b8-2144-4f56-b0c7-e17e4949d6a7"
        }

        refunddict=SignDispose.getSignDict(SignDispose(),refunddict,self.signkey,'SHA256')
        response = requests.request("POST", url2, data=str(refunddict), headers=headers)
        print(refunddict)
        print(response.text)
        self.assertEqual(response.json().get("errCode"), "SUCCESS","微信公众号渠道退款失败")
