import requests
from time import time
from random import randint
import hashlib


s=requests.session()

def getDict(voc,salt,ts,sign,bv,headers):
    url="http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    data={
        'i':voc,
        'from':' AUTO',
        'to':' AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':salt,
        'sign':sign,
        'ts':ts,
        'bv':bv,
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_REALTlME',
    }
    res=s.post(url,data=data,headers=headers)
    return res.json()

def getTs():
    ts=str(int(time()*10**3))
    salt=ts+str(randint(0,9))
    return str(ts),str(salt)

def getMd5(string):
    string=string.encode("utf-8")
    md5=hashlib.md5(string).hexdigest()
    return md5

def getResult(js):
    return js['translateResult'][0][0]['tgt']

def main(voc):
    headers={
        'Cookie':'_ntes_nnid=3788cc3f27b4b460daa0bf67160ee609,1565867124511; OUTFOX_SEARCH_USER_ID_NCOO=1326901157.6728864; OUTFOX_SEARCH_USER_ID=-1007044514@218.89.243.138; JSESSIONID=aaaDKchW_rb0w4icUBeax; ___rl__test__cookies=1580622386185',
        'Host':'fanyi.youdao.com',
        'Origin':'http://fanyi.youdao.com',
        'Referer':'http://fanyi.youdao.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    }
    bv=getMd5(headers['User-Agent'])
    ts,salt=getTs()
    sign=getMd5("fanyideskweb" + voc + salt + "n%A-rKaT5fb[Gy?;N5@Tj")
    js=getDict(voc,salt,ts,sign,bv,headers)
    result=getResult(js)
    return result

if __name__ =="__main__":
    print(main("这就是js逆向的结果").encode("utf-8"))




