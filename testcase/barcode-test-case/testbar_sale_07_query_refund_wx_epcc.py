import configparser
import datetime
import json
import unittest
from _md5 import md5
import random
from time import sleep

import requests

#HTTP-UTF-8-MD5-ENCRYPTION
#url = "http://144.131.254.141:9098"
from config.netpaytools import EnvServerConfig, SignDispose


class TestPayRefund(unittest.TestCase):
     """wechat-epcc-pay-refund"""
     #cf=configparser.ConfigParser()
     #cf.read("../config/config.ini")
     #url=cf.get("test","test_address")
     #url="http://144.131.254.141:9098"
     url=EnvServerConfig.getValue(EnvServerConfig(),"green","green_router_url")


     mer_orderId = str(random.randrange(1122334455667788,999999999999999999999999999999))
     signkey="1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"

     def test_a_Pay01(self):
         """ 微信EPCC渠道条码支付"""
         now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         authcode=input("请扫描条码:")
         print("条码是："+authcode)


         payloaddict={'msgType':'pay',
        'requestTimestamp':now_time,
        'msgSrc':'NETPAY',
        'msgId':'02S221X0000004992435124935',
        'mid':'898310077770000',
        'tid':'00810001',
        'barCode':authcode,
        'instMid':'POSTONGDEFAULT',
        'totalAmount':'1',
        'refId':'00004992435W',
        'orderDesc':'xyz',
        'goods':[{"quantity":"10","price":"3","goodsCategory":"A001","goodsld":"X001","body":"11","goodsName":"pay+refund"}],
        'merOrderId':self.mer_orderId
         }
         headers = {
             'Content-Type': "application/json",
             'cache-control': "no-cache",
             'Postman-Token': "c10fac27-b245-4d3b-b52d-45e2d9790517"
         }

         SignDispose.getSignDict(SignDispose(), payloaddict, self.signkey, "MD5")

         saleresponse = requests.request("POST", self.url, data=str(payloaddict),headers=headers)
         self.assertIn(saleresponse.json().get("errCode"),"SUCCESS","bar-code fail:"+saleresponse.json().get("errCode"))

     def test_b_Query(self):
         " " " 微信EPCC渠道条码支付查询"""
         now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         payquery = "{\"merOrderId\":\"" + self.mer_orderId + "\"," \
                                                         "\"mid\":\"898310077770000\"," \
                                                         "\"msgSrc\":\"NETPAY\"," \
                                                         "\"msgType\":\"query\"," \
                                                         "\"requestTimestamp\":\"" + now_time + "\"," \
                                                                                                     "\"tid\":\"00000001\"}"
         headers = {
             'cache-control': "no-cache",
             'Postman-Token': "37db237c-1d7a-4e70-9179-fa4b7ae27559"
         }
         payquerydict = SignDispose.getSignDict(SignDispose(), json.loads(payquery), self.signkey, "MD5")
         response = requests.request("POST", self.url, data=str(payquerydict), headers=headers)
         print(response.text)
         self.assertEqual(response.json().get("errCode"), "SUCCESS",
                          "barcode-query-unionpay case test result is:--" + response.json().get("errCode"))

     def test_c_Refund(self):
        """ 微信EPCC渠道条码支付退货接口"""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sleep(10)

        refundload = "{\"merOrderId\":\""+self.mer_orderId+"\",\"mid\":\"898310077770000\", \
        \"refundAmount\":\"1\",\"msgSrc\":\"NETPAY\",\"msgType\":\"refund\",\"requestTimestamp\":\""+now_time+"\",\"tid\":\"00000001\"}"

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "c10fac27-b245-4d3b-b52d-45e2d9790517"
        }

        refundloaddict=SignDispose.getSignDict(SignDispose(),json.loads(refundload),self.signkey,"MD5")
        print("请求报文："+str(refundloaddict))
        response = requests.request("POST", self.url, data=str(refundloaddict),headers=headers)

        self.assertIn(response.json().get("errCode"),"SUCCESS","refund fail:"+response.json().get("errCode"))
