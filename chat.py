# encoding=utf8  
from urllib import parse,request
import datetime
import _thread
import schedule
import itchat
import time
import sys  
import urllib.request
import json
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

readBookStartDay = datetime.datetime(2019, 3, 7)

# 数据提供类
class DataUtil():
	# 获取天气信息
	def getWeatherData(cityname):
		# 阿凡达数据 
		url = ' http://api.avatardata.cn/Weather/Query?key=45fca859897f439cbb47bd3ad2d86b9a&cityname=%E4%B8%8A%E6%B5%B7'
		req = urllib.request.urlopen(url)
		res = req.read().decode('utf-8')
		print(res) 
		text = DataUtil.parseInfo_afd(res)
		#输出内容(python3默认获取到的是16进制'bytes'类型数据 Unicode编码，如果如需可读输出则需decode解码成对应编码):b'\xe7\x99\xbb\xe5\xbd\x95\xe6\x88\x90\xe5\x8a\x9f'
		
		return text

	# 简单的数据修饰封装
	def parseInfo_afd(jsons):
		# 将string 转换为字典对象
		jsonData = json.loads(jsons)
		textInfo = '早上好，今天又是元气满满的一天哟.\n'
		data = jsonData['result']['weather'][0]['date']
		week = jsonData['result']['weather'][0]['week']
		nongli = jsonData['result']['weather'][0]['nongli']
		city_name = jsonData['result']['realtime']['city_name']
		lowTemperature = jsonData['result']['weather'][0]['info']['dawn'][2]
		highTemperature = jsonData['result']['weather'][0]['info']['day'][2]
		weather = jsonData['result']['weather'][0]['info']['day'][1]
		wind = jsonData['result']['weather'][0]['info']['day'][4]

		textInfo = textInfo + '今天是' + data + '号\n'
		textInfo = textInfo + '农历:' + nongli + ',星期' + week + '\n'
		textInfo = textInfo + city_name + '气温：' + lowTemperature + '-' + highTemperature + '度，' + weather + ' ' + wind + '\n\n'
		textInfo = textInfo + '穿衣指数：' + jsonData['result']['life']['info']['chuanyi'][0] + ' - ' + jsonData['result']['life']['info']['chuanyi'][1] + '\n\n'
		textInfo = textInfo + '运动指数：' + jsonData['result']['life']['info']['yundong'][0] + ' - ' + jsonData['result']['life']['info']['yundong'][1] + '\n\n'
		textInfo = textInfo + '感冒指数：' + jsonData['result']['life']['info']['ganmao'][0] + ' - ' + jsonData['result']['life']['info']['ganmao'][1]  + '\n\n'
		textInfo = textInfo + '紫外线指数：' + jsonData['result']['life']['info']['ziwaixian'][0] + ' - ' + jsonData['result']['life']['info']['ziwaixian'][1]  + '\n\n'
		textInfo = textInfo + 'by：小可爱的贴心秘书' + '\n\n'
		return textInfo
		# 提取故事的第一天

	def getBookInfo( filePath): #文件路径，
		radioList = [] #微信每次最多只能发送的字符是有限制的，我每25行发送一次信息
		row = 0
		tempInfo = textInfo = '睡前故事：张嘉佳 - 《从你的全世界路过》.\n\n'
		readFlag = False #是否读取
		today = datetime.datetime.now()
		dayCount = (today - readBookStartDay).days + 1
		for line in open(filePath):
			if (line.find('night.' + str(dayCount)) > -1): # 开始读数据
				readFlag = True
				continue
			if (line.find('night.' + str(dayCount+1)) > -1): # 读完一天数据结束
				break
			if readFlag:
				row += 1
				tempInfo += line
				# 微信每次最多只能发送的字符是有限制的，我每25行发送一次信息
				if row == 25:
					radioList.append(tempInfo)
					tempInfo = ''
					row = 0
		tempInfo += '\n晚安\n' + 'by：小可爱的贴心秘书' + '\n'
		radioList.append(tempInfo)
		# common.txtToMp3(radioList) #文字生成语音 发送语音
		print(radioList)
		return radioList
		
	def getBingPhoto(index):
		# index 对应的是 必应 index天的壁纸
		url = ' http://www.bing.com/HPImageArchive.aspx?format=js&idx=' + index + '&n=1&nc=1469612460690&pid=hp&video=1'
		html = urllib.request.urlopen(url).read().decode('utf-8')

		photoData = json.loads(html)
		# 这是壁纸的 url
		photoUrl = 'https://cn.bing.com' + photoData['images'][0]['url']
		photoReason = photoData['images'][0]['copyright']
		photoReason = photoReason.split(' ')[0]
		photo = urllib.request.urlopen(photoUrl).read()

		# 下载壁纸刀本地
		with open('./bing.jpg', 'wb') as f:
			# img = open_url(photoUrl)
			if photo:
				f.write(photo)
		print("图片已保存")

		# 把壁纸的介绍写到壁纸上
		# 设置所使用的字体
		font = ImageFont.truetype("simhei.ttf",35)
		imageFile = "./bing.jpg"
		im1 = Image.open(imageFile)
		# 画图，把壁纸的介绍写到壁纸上
		draw = ImageDraw.Draw(im1)
		draw.text((im1.size[0]/2.5, im1.size[1]-50), photoReason, (255, 255, 255), font=font)  # 设置文字位置/内容/颜色/字体
		draw = ImageDraw.Draw(im1)  # Just draw it!
		# 另存图片
		im1.save("./bing.jpg")
		
	
		 
class WeChat():

	def login(self):
		itchat.auto_login(hotReload=True)  # 登录，会下载二维码给手机扫描登录，hotReload设置为True表示以后自动登录 
		friends = itchat.search_friends(name='Alice')  # 获取微信好友信息
		userName = friends[0]['UserName']
		itchat.send('哈喽 小可爱', toUserName=userName)  # 发送信息给指定好友 
		
		itchat.run()  # 让itchat一直运行
		 
	def getFriend(self,name):
		friends = itchat.search_friends(name = name)  # 获取微信好友列表，如果设置update=True将从服务器刷新列表
		userName = friends[0]['UserName']
		return userName

	def getFriends(self):
		friends = itchat.get_friends(update=True)[0:]
		return friends
		
# 推送每日早报
	def dailyInfo(self):
		print('dailyInfo do')
		shanghai = DataUtil.getWeatherData('上海') 
		yfei = wechat.getFriend('Alice')
		wechat.sendMessage(shanghai, yfei)
		
		 
		
# 推送睡前故事
	def readStory(self):
		print('readStory do')
		stroy = DataUtil.getBookInfo('./从你的全世界路过.txt')
		today = datetime.datetime.now()
		dayCount = (today - readBookStartDay).days 
		DataUtil.getBingPhoto(str(dayCount)) 
		yfei = wechat.getFriend('Alice') 
		for txt in stroy:
			wechat.sendMessage(txt, yfei)

		# 发送壁纸
		itchat.send_image('./bing.jpg', toUserName=yfei)
		
	def sendMessage(self, message, name):
		itchat.send(message, toUserName=name)
		
wechat = WeChat() #这里是封装的 itchat
# 开启微信登录线程，需要单独占个线程
_thread.start_new_thread(wechat.login, ( ))

# 配置定时任务
# 开启早间天气预报 定时任务
schedule.every().day.at("16:27").do(wechat.dailyInfo)
# 开启睡前故事 定时任务
schedule.every().day.at("16:40").do(wechat.readStory)
while True:
	schedule.run_pending()
	time.sleep(1)