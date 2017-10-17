import requests

class downloader(object):
	"""docstring for downloader"""
	
	def download(self,url):
		#如果传入url为空，则返回None
		if url == None:
			return None

		#使用requests加载页面，如果code为200则表示请求成功
		try:
			response = requests.get(url)
			return response.text
		except:
			print("there's some error in downloader")
			return None