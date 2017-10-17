from bs4 import BeautifulSoup
import re

class html_parser(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass
	
	def get_urls(self,text):
		#从下载页面中获取urls
		#<a href="https://movie.douban.com/subject/1292052/" class="">
		soup = BeautifulSoup(text,'html.parser')
		urls = set()
		#print("hello1")
		#links = soup.find_all('a',href=re.compile(r"/item/*?"))
		links = soup.find_all('a',href=re.compile(r"https://movie.douban.com/subject/.*?/"),class_=None)

		for link in links:
			urls.add(link['href'])
			#print(link['href'])
		return urls
		

	def get_datas(self,text):
		#从下载页面获取需要数据
		#num = 0
		soup = BeautifulSoup(text,'html.parser')
		datas = list()
		titles = list()
		dires = soup.find_all('a',rel = 'v:directedBy')

		#<span property="v:itemreviewed">肖申克的救赎 The Shawshank Redemption</span>
		info = soup.find_all('span',property="v:itemreviewed")
		for dire in dires:
			datas.append(dire.string)
			#num += 1
			#print("top %d :%s"%(num,dire.string))
		
		#for title in info:
		#	titles.append(info.string)
		#	print(info.string)


		return datas








		