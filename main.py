import requests
from time import time,localtime,strftime,sleep
import re
import json
from datetime import datetime
nowTime = datetime.now()
"""
使用：
1.需要安装requests库
2.在main函数中使用writeSummaryData()，writeWorldData()或者writeChinaData()然后运行，
	就可以将总览/国际/中国的数据写入对应的csv文件。
3.csv文件的名称：后面的是获取数据的日期+数据更新时间点。
	这样做的好处：当网页数据更新后，生成的csv不会覆盖原来的数据
4.csv文件中第一行是当前数据更新的时间
"""

# 如果需要每隔一段时间自动生成csv，可以把main函数换成以下：
# def main():
# 	while True:
# 		writeSummaryData()
# 		writeWorldData()
# 		writeChinaData()
# 		# 一个小时生成一次数据，3600的单位是秒
# 		sleep(3600)
# 然后把脚本挂在电脑上


def main():
	writeSummaryData()
	writeWorldData()
	writeChinaData()

# 以下两个函数是中国数据的脚本，可以按需更改第一个函数
def writeChinaData():
	dataIter = getChinaData(res).__iter__()
	chickTime = dataIter.__next__()
	with open("ChinaData\\ChinaData%s+"%(nowTime.strftime("%Y-%m-%d"))+chickTime+".csv","w") as f:
		f.write("更新时间："+chickTime+"\n")
		f.write("省/市名称"+","+"现存确诊"+","+"累计确诊"+","+"疑似"+","+"累计治愈"+","+"累计死亡"+","+"地址ID\n\n")
		while True:
			try:
				data = dataIter.__next__()
				f.write(str(data['provinceName'])+","+str(data['currentConfirmedCount'])+","+str(data['confirmedCount'])+","+str(data['suspectedCount'])+","+str(data['curedCount'])+","+str(data['deadCount'])+","+str(data['locationId'])+"\n")
				for cityData in data['cities']:
					f.write(str(cityData['cityName'])+","+str(cityData['currentConfirmedCount'])+","+str(cityData['confirmedCount'])+","+str(cityData['suspectedCount'])+","+str(cityData['curedCount'])+","+str(cityData['deadCount'])+","+str(cityData['locationId'])+"\n")
				f.write("\n\n")
			except StopIteration:
				break

def getChinaData(res):
	summaryData = re.findall("window.getStatisticsService =(.*?)}catch",res.text)[0]
	summaryData = json.loads(summaryData)
	deadLine = int(summaryData['modifyTime'])
	deadLine = strftime("%Y-%m-%d %H-%M", localtime(deadLine/1000))
	print(deadLine)
	yield deadLine
	chinaDataStr = re.findall(" window.getAreaStat =(.*?)}catch" , res.text)[0]
	chinaDataList = json.loads(chinaDataStr)
	print("获取了多少个省的数据：" , len(chinaDataList))
	for chinaData in chinaDataList:
		yield chinaData

# 以下两个函数是国际数据的脚本，可以按需更改第一个函数
def writeWorldData():
	dataIter = getWorldData(res).__iter__()
	chickTime = dataIter.__next__()
	with open("WorldData\\WorldData%s+%s.csv"%(nowTime.strftime("%Y-%m-%d"),chickTime),"w") as f:
		f.write("更新时间："+chickTime+"\n")
		f.write("所属洲"+","+"国名"+","+"国名简写"+","+"现存确诊"+","+"累计确诊"+","+"疑似"+","+"累计治愈"+","+"累计死亡"+","+"地址ID\n")
		while True:
			try:
				data = dataIter.__next__()
				f.write(str(data['continents'])+","+str(data['provinceName'])+","+str(data['countryShortCode'])+","+str(data['currentConfirmedCount'])+","+str(data['confirmedCount'])+","+str(data['suspectedCount'])+","+str(data['curedCount'])+","+str(data['deadCount'])+","+str(data['locationId'])+"\n")
			except StopIteration:
				break

def getWorldData(res):
	summaryData = re.findall("window.getStatisticsService =(.*?)}catch",res.text)[0]
	summaryData = json.loads(summaryData)
	deadLine = int(summaryData['modifyTime'])
	deadLine = strftime("%Y-%m-%d %H-%M", localtime(deadLine/1000))
	print(deadLine)
	yield deadLine
	worldDataStr = re.findall("window.getListByCountryTypeService2true = (.*?)}catch" , res.text)[0]
	worldDataList = json.loads(worldDataStr)
	print("获取了多少个国家数据：",len(worldDataList))
	for worldData in worldDataList:
		yield worldData

def writeSummaryData():
	summaryData = getSummaryData(res)
	deadLine = summaryData['modifyTime']
	chickTime = strftime("%Y-%m-%d %H-%M", localtime(deadLine/1000))
	with open("SummaryData\\SummaryData%s+%s.csv"%(nowTime.strftime("%Y-%m-%d"),chickTime),"w") as f:
		f.write("更新时间："+chickTime + "\n" + "国内总览" + "\n")
		f.write("现存确诊" + "," + str(summaryData["currentConfirmedCount"])+ "," + "较昨日" + "," + str(summaryData["currentConfirmedIncr"]) + "\n")
		f.write("累计确诊" + "," + str(summaryData["confirmedCount"])+ "," + "较昨日" + "," + str(summaryData["confirmedIncr"]) + "\n")
		f.write("现存疑似" + "," + str(summaryData["suspectedCount"])+ "," + "较昨日" + "," + str(summaryData["suspectedIncr"]) + "\n")
		f.write("累计治愈" + "," + str(summaryData["curedCount"])+ "," + "较昨日" + "," + str(summaryData["curedIncr"]) + "\n")
		f.write("累计死亡" + "," + str(summaryData["deadCount"])+ "," + "较昨日" + "," + str(summaryData["deadIncr"]) + "\n")
		f.write("现存重症" + "," + str(summaryData["seriousCount"])+ "," + "较昨日" + "," + str(summaryData["seriousIncr"]) + "\n")
		f.write("\n国外总览\n")
		f.write("现存确诊" + "," + str(summaryData["foreignStatistics"]["currentConfirmedCount"])+ "," + "较昨日" + "," + str(summaryData["foreignStatistics"]["currentConfirmedIncr"]) +"\n")
		f.write("累计确诊" + "," + str(summaryData["foreignStatistics"]["confirmedCount"])+ "," + "较昨日" + "," + str(summaryData["foreignStatistics"]["confirmedIncr"])+"\n")
		f.write("现存疑似" + "," + str(summaryData["foreignStatistics"]["suspectedCount"])+ "," + "较昨日" + "," + str(summaryData["foreignStatistics"]["suspectedIncr"]) + "\n")
		f.write("累计治愈" + "," + str(summaryData["foreignStatistics"]["curedCount"])+ "," + "较昨日" + "," + str(summaryData["foreignStatistics"]["curedIncr"])+"\n")
		f.write("累计死亡" + "," + str(summaryData["foreignStatistics"]["deadCount"])+ "," + "较昨日" + "," + str(summaryData["foreignStatistics"]["deadIncr"]) + "\n")



def getSummaryData(res):
	summaryData = re.findall("window.getStatisticsService =(.*?)}catch" , res.text)[0]
	summaryData = json.loads(summaryData)
	return summaryData

def getResponse():
	url = "https://ncov.dxy.cn/ncovh5/view/pneumonia?"
	params = {
		'scene':'2',
		'clicktime':time(),
		'enterid':time(),
		'from':'groupmessage',
		'isappinstalled':'0',
	}
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4068.4 Safari/537.36"
	}
	res = requests.get(url = url , params = params , headers = headers)
	res.encoding = "utf-8"
	return res

if __name__ == '__main__':
	res = getResponse()
	main()
