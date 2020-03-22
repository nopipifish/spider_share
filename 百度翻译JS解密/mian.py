import execjs
from requests import session
s = session()

def main(word,FROM = "zh" ,TO = "en"):
    transResultDict = getTrans(word , FROM , TO)
    print(transResultDict["trans_result"]["data"][0]["dst"])

def getSign(word):
    with open("main.js" , "r") as f:
        jsCode = f.read()
        js = execjs.compile(jsCode)
    sign = js.call("e",word)
    return sign


def getTrans(word,FROM = "zh" ,TO = "en"):
    headers = {
        'cookie':'BIDUPSID=CD78C4B00D16812BC9F2F91CFDB4B52D; PSTM=1581300224; BAIDUID=CD78C4B00D16812BBC51E6DB95679864:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; BDUSS=TZldkxEQlZDdFREbjRwZ2VDYVludENVUjJzNXI1VndyYnU2VX5BMXQ0enMzbWhlRVFBQUFBJCQAAAAAAAAAAAEAAABQscVKyre1z9fQtcTHprHKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOxRQV7sUUFeb; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; H_PS_PSSID=30744_1446_21108_30788_30823_28702; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1581345470,1581406181,1581836693,1582342354; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1582342354; __yjsv5_shitong=1.0_7_5056be4a7a070588f3b81b9bfb56b242fcf1_300_1582342356477_183.221.11.98_f6395196; yjs_js_security_passport=1fc340bfe9eda0f016361358c0b5caed5de3cb98_1582342357_js; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22dan%22%2C%22text%22%3A%22%u4E39%u9EA6%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D',
        'origin':'https://fanyi.baidu.com',
        'pragma':'no-cache',
        'referer':'https://fanyi.baidu.com/?aldtype=16047',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
    }
    data = {
        'from':FROM,
        'to':TO,
        'query':word,
        'transtype':'realtime',
        'simple_means_flag':'3',
        'sign':getSign(word),
        'token':'e6a0f5d320044dab387a2ddd535a3acc',
        'domain':'common',
    }
    url = "https://fanyi.baidu.com/v2transapi?from={}&to={}".format(FROM,TO)
    res = s.post(url = url , data = data , headers = headers)
    return res.json()

if __name__ == "__main__":
    st = "Why is zhao zeke so stupid?"
    main(st,"en","zh")
