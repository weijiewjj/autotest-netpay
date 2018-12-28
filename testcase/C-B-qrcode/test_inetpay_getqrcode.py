import json

import datetime
import unittest
from _sha256 import sha256

import qrcode
import requests
from _md5 import md5

from PIL import Image


class GetINetpayCode(unittest.TestCase):
    now_time= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    signkey="XFwGdip3eBPxxa6ZjRpGtKKWthiXykrAQCzP3T3324fbmBkS"

    url = "http://10.11.116.17:9097"

#payload = "{\"msgType\":\"unionpay.preCreate\",\"tipType\":\"percent\",\"requestTimestamp\":\"2018-12-11 15:02:53\",\"msgSrc\":\"INETPAY_WEB\",\"mid\":\"8983401490012345\",\"feeType\":\"156\",\"tid\":\"88880001\",\"transactionAmount\":\"11\",\"tipPercentage\":\"10.9\",\"qrcType\":11,\"sign\":\"abcxyzaaa\"}"

#json.loads(payload)
    def testgetINetpayQRCode(self):
        strdict={
            "msgType": "unionpay.preCreate",
            "tipType": "percent",
            "requestTimestamp": self.now_time,
            "msgSrc": "IULINK",
            "mid": "123456789012345",
            "feeType": "156",
            "tid": "88880001",
            "transactionAmount": "11",
            "tipPercentage": "10.9",
            "qrcType": "11"
        }

        voiddigest=""
        for key in sorted(strdict):
            voiddigest = voiddigest + key + "=" + strdict.get(key) + '&'


        print(voiddigest[:-1])
        voiddigest = voiddigest[:-1] + self.signkey

        strdict.setdefault("sign",sha256(voiddigest.encode('utf-8')).hexdigest())
        response = requests.request("POST", self.url, data=str(strdict))

        print(response.text)
        img=qrcode.make(response.json().get("qrCodeContent"))
        img.save("./inetpay-unionpaycode.png")
        Image.open("./inetpay-unionpaycode.png").resize((360,360)).show()

