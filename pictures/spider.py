import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
import re
import pymongo
from config import *
from hashlib import md5
import os
from mutiprocessing import Pool


client = pymongo.MongoClient(MONGO_URL,connect = False)
db = client[MONGO_DB]

#构造请求，获取服务器的json返回数据

def get_page_index(offset,keyword):
	data = {
			'offset':offset,
			'format':'json',
			'keyword':keyword,
			'autoload':'true',
			'count':'20',
			'cur_tab':3	
			}

	url = 'https://www.toutiao.com/search_content/?' + urlencode(data)

	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		else:
			return None

	except RequestException:
		print("请求索引页失败")
		return None


#对某一请求得到的数据进行解析，获取该页的详细图片地址

def parse_page_index(html):
	data = json.loads(html)
	if data and 'data' in data.keys():
		for item in data.get('data'):
			yield item.get('article_url')


def get_detail_page(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		print("请求详情页面出错")
		return None



#在这里出现了一点小问题，现在网页的内容与之前有些差别，json.loads时不能成功，仔细检查后发现匹配正则时多匹配了一组引号，导致
#loads后仍然是str类型，修改后发现仍然不能成功，这是因为gallery的值已经被转码，于是用正则替换了所有的'/'，终于将字符
#json.loads成功，得到key为url的值
def parse_detail_page(html,url):
	pattern = re.compile('BASE_DATA.galleryInfo = (.*?);',re.S)
	result = re.search(pattern,html)
	data = result.group(1)

	pattern_title = re.compile('title:(.*?),',re.S)
	#print(result)
	result2 = re.search(pattern_title,data)
	#print(data)
	title = result2.group(1)

	pattern_image = re.compile('gallery: JSON.parse\("(.*?)"\)')

	result3 = re.search(pattern_image,data)
	#print(result3.group(1))
	jsonStr = re.sub(r'\\{1,2}', '',result3.group(1))
	#print(jsonStr)


	if result3:

		data_image = json.loads(jsonStr)

		if data_image and 'sub_images' in data_image.keys():
			sub_images = data_image.get('sub_images')
			images = [item.get('url') for item in sub_images]
			for image in images:
				download_image(image)
			return {"title":title,
					"url":url,
					"images":images}


def save_to_mongo(result):
	if db[MONGO_TABLE].insert(result):
		print("存储到MongoDB成功")
		return True
	return False


def download_image(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			save_image(response.content)
		return None
	except RequestException:
		print("下载图片出错")
		return None

def save_image(content):
	file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
	if not os.path.exists(file_path):
		with open(file_path,'wb') as f:
			f.write(content)
			f.close()



def main(offset):
	text = get_page_index(offset,KEY_WORD)
	#print(text)

	for url in parse_page_index(text):
		html = get_detail_page(url)
		result = parse_detail_page(html,url)
		if result:
			save_to_mongo(result)
		#print(result)



if __name__ == "__main__":
	groups = [x * 20 for x in range(GROUP_START,GROUP_END + 1)]
	pool = Pool()
	pool(main,groups)


 