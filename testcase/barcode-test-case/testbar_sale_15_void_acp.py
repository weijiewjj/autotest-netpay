import datetime
import json
import random
import unittest
from _md5 import md5

import requests

# HTTP-UTF-8-MD5-ENCRYPTION
# url = "http://144.131.254.141:9098"
from config.netpaytools import EnvServerConfig, SignDispose

'''
cf=configparser.ConfigParser()
cf.read("../config/config.ini")
url = cf.get("test","test_address")
from config.netpaytools import EnvServerConfig
'''
class TestPayVoidCheck(unittest.TestCase):
    """银联云闪付ACP渠道条码支付-撤销"""
    url = EnvServerConfig.getValue(EnvServerConfig(),"green","green_router_url")
    #url ="http://144.131.254.141:9098"
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now_time)
    mer_orderId = str(random.randrange(1122334455667788,999999999999999999999999999999))
    signkey="1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"

    def test_a_BarPay(self):
        ''' 银联云闪付ACP渠道条码支付'''
        authcode = input("请扫描云闪付条码：")
        print("条码是" + authcode)
        payloaddict = {'msgType': 'pay',


                       'requestTimestamp':self.now_time,
                       'msgSrc':'NETPAY',
                       'msgId':'02S221X0000004992435124935',
                       'mid':'898310148160568',
                       'tid':'00810001',
                       'barCode':authcode,
                       'instMid':'POSTONGDEFAULT',
                       'totalAmount':'1',
                       'refId':'00004992435W',
                       'orderDesc':'xyz',
                       'goods':[{"quantity":"10","price":"3","goodsCategory":"A001","goodsld":"X001","body":"11","goodsName":"xyz"}],
                       'merOrderId':self.mer_orderId
                       }
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "c10fac27-b245-4d3b-b52d-45e2d9790517"
        }

        SignDispose.getSignDict(SignDispose(),payloaddict,self.signkey,"MD5")
        saleresponse = requests.request("POST", self.url, data=str(payloaddict),headers=headers)
        self.assertIn(saleresponse.json().get("errCode"), ["SUCCESS", "TARGET_FAIL"],
                      "bar-code pay fail" + saleresponse.json().get("errCode") )

    def test_b_Query(self):
        """ 银联云闪付ACP条码支付查询"""
        payquery= "{\"merOrderId\":\""+mer_orderId+"\"," \
                                                           "\"mid\":\"898310148160568\"," \
                                                           "\"msgSrc\":\"ULINK\"," \
                                                           "\"msgType\":\"query\"," \
                                                           "\"requestTimestamp\":\""+self.now_time+"\"," \
                                                                                              "\"tid\":\"00000001\"," \
                                                                                              "\"sign\":\"fdfdf\"}"
        headers = {
                    'cache-control': "no-cache",
                    'Postman-Token': "37db237c-1d7a-4e70-9179-fa4b7ae27559"
                }
        response = requests.request("POST", url, data=payquery, headers=headers)
        print(response.text)
        self.assertEqual(response.json().get("errCode"),"SUCCESS","barcode-query-unionpay case test result is:--"+response.json().get("errCode"))




    def test_c_BarVoid(self):
        ''' 银联云闪付ACP条码支付撤销'''
        voidload = "{\"merOrderId\":\"" + self.mer_orderId + "\",\"mid\":\"898310148160568\", \
    \"msgSrc\":\"NETPAY\",\"msgType\":\"cancel\",\"requestTimestamp\":\""+self.now_time+"\",\"tid\":\"00000001\"}"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "c10fac27-b245-4d3b-b52d-45e2d9790517"
        }

        voidDict=SignDispose.getSignDict(SignDispose(), json.loads(voidload), self.signkey, "MD5")
        response = requests.request("POST", self.url, data=str(voidDict),headers=headers)
        print(response.text)
        self.assertIn(response.json().get("errCode"), ["SUCCESS", "TARGET_FAIL"],
                      "void fail" + response.json().get("errCode") )