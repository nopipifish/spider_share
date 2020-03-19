import execjs
import requests

def main(word,tl = "en"):
    res = getTrans(word,tl)
    print("翻译结果：",(res.json())[0][0][0])

def getTk(word):
    with open("main.js" , "r") as f:
        ctx = execjs.compile(f.read())
    return ctx.call("eu" , word)

def getTrans(word , tl):
    url = "https://translate.google.cn/translate_a/single?"
    params = {
        'client':'webapp',
        'sl':'auto',      
        'tl':tl,        
        'hl':'zh-CN',     
        "dt":["at","bd","ex","ld","md","qca","rw","rm","ss","t"],
        'otf':'1',
        'ssel':'0',
        'tsel':'0',
        'kc':'1',
        'tk':getTk(word),
        'q':word,
    }
    headers = {
        'cookie':'_ga=GA1.3.1597232252.1583203337; NID=199=WyfB826oJKtFD68RJJckPmkpzBKCAzpg_br42veGETl-RB8P0O12Jey8ay96Zd9S8maKVaMcKVI3_uux2P8c3XBY893AO1rEGTUAhFjXgOgES9EDUFXnAWS9B9_QDim93rwjCkrBSLJNLZWd1KQus9Pu3V8E175fykYSp7HuFww; _gid=GA1.3.43748189.1583565218; 1P_JAR=2020-3-7-12',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4068.4 Safari/537.36',
    }
    res = requests.get(url = url , params = params , headers = headers)
    return res

if __name__ == "__main__":
    needTransWord = "沧海桑田"
    main(needTransWord)
    
