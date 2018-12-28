import random
import unittest
from _md5 import md5

import datetime
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
#mer_orderId="144096524370652490676434226606"



class TestPublicWechatPay(unittest.TestCase):
    """ 测试微信银联渠道公众号跳转查询以及退货 """
    signkey = "1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def test_a_GetUrl_jump(self):
        """ 测试公众号跳转类页面并进行支付"""
        querystring = {"totalAmount":"1","msgSrc":"NETPAY","mid":"898310088884444","tid":"12345678","instMid":"QRPAYDEFAULT",
               "merOrderId":"255320436381421351056767323525","sign":"ecd155ddc4d1cf799c98c30b5e8970da",
               "sub_openId":"oOUAZv7VMkNx31zcDpzbq3IEigXs"}
        assert isinstance(querystring,dict)
        #处理dict字段内容：
        querystring["merOrderId"]=mer_orderId
        querystring["mid"]="898460147840001"
        querystring.pop("sign")
        querystring.pop("sub_openId")
        digest=''
        for key in sorted(querystring):
            digest=digest+key+'='+querystring.get(key)+'&'

        digest=digest[:-1]+self.signkey
        print(digest)

        querystring.setdefault("sign",md5(digest.encode('utf-8')).hexdigest())
        payload = ""
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTEW Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.0.54_r849063.501 NetType/WIFI",
            'cache-control': "no-cache",
            'Postman-Token': "491b8234-daa0-49d1-acea-aac6ebeb936d"
            }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        print(type(response))
        assert isinstance(response,requests.models.Response)
        print(response.url)

        ##二维码的高级用法
        QRCodeWithLogo.getQRCode(QRCodeWithLogo(),response.url,"qrcode.png","icon.png")
        Image.open("qrcode.png").resize((360,360)).show()



    def test_b_Querypay(self):
        """ 对支付过的交易进行查询"""
        payquery= "{\"merOrderId\":\""+mer_orderId+"\"," \
          "\"mid\":\"898460147840001\"," \
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

    def test_c_Refund(self):
        """ 银联微信渠道公众号支付进行退货交易"""
        refunddict={
            "msgType": "refund",
            "msgSrc": "NETPAY",
            "mid": "898460147840001",
            "merOrderId": mer_orderId,
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
        response = requests.request("POST", url2, data=str(refunddict), headers=headers)
        print(refunddict)
        print(response.text)
        self.assertEqual(response.json().get("errCode"), "SUCCESS","微信公众号渠道退款失败")
