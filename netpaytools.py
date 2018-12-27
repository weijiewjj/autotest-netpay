import configparser
import json
from _md5 import md5
from _sha256 import sha256


class EnvServerConfig:
    def __init__(self):
        self.cf=configparser.ConfigParser()
        self.cf.read("./config.ini")
    # def getDEV(self,address):
    #     value=self.cf.get("dev",address)
    #     return value
    # def getGreen(self,address):
    #     url=self.cf.get("green",address)
    #     return url
    # def getTest(self,address):
    #     url=self.cf.get("test",address)
    #     return url
    def getValue(self,session,address):
        url=self.cf.get(session,address)
        return url

class SignDispose:
    def __init__(self):
        return

    def getSignDict(self,dictdata,signkey,encryption):
        digeststr=""
        sign=""

        for key in sorted(dictdata):
            if (isinstance(dictdata.get(key), list)):
                print(json.dumps(dictdata.get(key)).replace(' ', ''))
                digeststr = digeststr + key + '=' + json.dumps(dictdata.get(key)).replace(' ', '') + '&'
            else:
                digeststr = digeststr + key + '=' + str(dictdata.get(key)) + '&'

        digeststr = digeststr[:-1] + signkey
        if(encryption=='SHA256'):
            sign = dictdata.setdefault('sign', sha256(digeststr.encode('utf-8')).hexdigest())
        else:
            sign = dictdata.setdefault('sign', md5(digeststr.encode('utf-8')).hexdigest())

        return dictdata

    def getSignDictWithSpace(self,dictdata,signkey,encryption):
        digeststr=""
        sign=""

        for key in sorted(dictdata):
            digeststr = digeststr + key + '=' + str(dictdata.get(key)) + '&'

        digeststr = digeststr[:-1] + signkey
        if(encryption=='SHA256'):
            sign = dictdata.setdefault('sign', sha256(digeststr.encode('utf-8')).hexdigest())
        else:
            sign = dictdata.setdefault('sign', md5(digeststr.encode('utf-8')).hexdigest())

        return dictdata
