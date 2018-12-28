import requests

url = "https://qr-test1.chinaums.com/netpay-route-server/api/"

payload = "{\"mid\":\"898460207420001\",\"msgSrc\":\"NETPAY\",\"msgType\":\"bills.getQRCode\",\"notifyUrl\":\"http://www.baidu3.com\",\"orderDesc\":\"abcdeddd\",\"requestTimestamp\":\"2018-12-12 10:36:55\",\"goodsTag\":\"xxxyyy\",\"tid\":\"00000001\",\"instMid\":\"QRPAYDEFAULT\",\"signType\":\"SHA256\",\"sign\":\"\"}"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "c10fac27-b245-4d3b-b52d-45e2d9790517"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)