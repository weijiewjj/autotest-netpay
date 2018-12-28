import configparser
import datetime
import json
import unittest
from _md5 import md5
import random

import requests

#HTTP-UTF-8-MD5-ENCRYPTION
#url = "http://144.131.254.141:9098"
# cf=configparser.ConfigParser()
# cf.read("../config/config.ini")
# url=cf.get("test","test_address")
from config.netpaytools import EnvServerConfig, SignDispose


class TestPayRefundQuery(unittest.TestCase):
    """Wechat-epcc-pay-refund-refundquery"""
    url = "http://144.131.254.141:9098"
    #url = EnvServerConfig.getValue(EnvServerConfig(),"test","test_router_url")
    #mer_orderId = str(random.randrange(1122334455667788,999999999999999999999999999999))
    mer_orderId="798584736152434349673834957276"
    signkey="1234567890lkkjjhhguuijmjfidfi4urjrjmu4i84jvm"
    #refundOrderId = ''

    def test_a_Pay(self):
        ''' 微信EPCC渠道条码支付 '''
        autocode = input("请扫描微信条码")
        print("条码是" + autocode)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        payloaddict={'msgType':'pay',
        'requestTimestamp':now_time,
        'msgSrc':'NETPAY',
        'msgId':'02S221X0000004992435124935',
        'mid':'898310077770000',
        'tid':'00810001',
        'barCode':autocode,
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
        saleresponse = requests.request("POST", self.url, data=str(payloaddict))


        self.assertIn(saleresponse.json().get("errCode"),["TARGET_FAIL","SUCCESS"],"支付失败errcode："+saleresponse.json().get("errCode"))



    def test_b_Refund(self):
        ''' 微信EPCC渠道条码支付退货和退货查询'''
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        refundload = "{\"merOrderId\":\""+self.mer_orderId+"\",\"mid\":\"898310077770000\", \
                    \"refundAmount\":\"1\",\"msgSrc\":\"NETPAY\",\"msgType\":\"refund\",\"requestTimestamp\":\""+now_time+"\",\"tid\":\"00000001\"}"

        voidDict = SignDispose.getSignDict(SignDispose(),json.loads(refundload),self.signkey,"MD5")
        response = requests.request("POST", self.url, data=str(voidDict))
        print("退货应答："+response.text)
        return response.json().get("refundOrderId")


        self.assertIn(response.json().get("errCode"),["SUCCESS","TARGET_FAIL"],"refund fail"+response.json().get("errCode"))


    def test_c_RefundQuery(self):
        """ wechat-epcc-refundquery"""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        refundqueryload = "{\"merOrderId\":\""+self.test_b_Refund()+"\",\"mid\":\"898310077770000\", \
                            \"refundAmount\":\"1\",\"msgSrc\":\"NETPAY\",\"msgType\":\"refundQuery\",\"requestTimestamp\":\""+now_time+"\",\"tid\":\"00000001\"}"
        print("退货查询请求:"+refundqueryload)

        refundqueryDict = SignDispose.getSignDict(SignDispose(), json.loads(refundqueryload), self.signkey, "MD5")
        refundqueryresponse = requests.request("POST", self.url, data=str(refundqueryDict))

        print("退货查询应答："+refundqueryresponse.text)



        self.assertIn(refundqueryresponse.json().get("errCode"), ["SUCCESS", "TARGET_FAIL"],
                      "refund query fail" + refundqueryresponse.json().get("errCode"))
