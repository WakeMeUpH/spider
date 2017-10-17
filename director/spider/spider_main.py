import url_manager,downloader,html_parser,outputer

class  spider_main(object):
	"""docstring for  spider_main"""
	def __init__(self):
		self.page = 0
		self.cur_url = r"https://movie.douban.com/top250?start={page}&filter=&type="
		self.URL_manager = url_manager.url_manager()
		self.Downloader = downloader.downloader()
		self.Outputer = outputer.outputer()
		self.Parser = html_parser.html_parser()

	def get_urls(self):
		while(self.page<4):
			#得到当前页面的url
			url = self.cur_url.format(page = self.page*25)

			#获取当前页面所有内容
			text = self.Downloader.download(url)

			#将下载页面进行解析的得到需要的url
			urls = self.Parser.get_urls(text)

			#将当前获取的url加入url管理器中
			self.URL_manager.add_urls(urls)

			#继续下一页的url添加
			self.page += 1

	def craw(self):
		print("开始搜集导演信息")
		datas = list()
		titles = list()
		#data = list()
		num = 0
		while self.URL_manager.has_new_url():
			try:
				#获取一个电影详情页面的url
				url = self.URL_manager.get_url()

				#将这个页面下载
				text = self.Downloader.download(url)

				#对这个页面进行解析，获得需要的内容
				data= self.Parser.get_datas(text)
				for item in data:
					datas.append(item)
					#titles.append(title)
					print("top %d:%s"%(num,item))
					num += 1
			except:
				print("craw failed!")
		
		#将数据存入本地
		self.Outputer.save(datas)
		print("done")

def main():
	ins = spider_main()
	ins.get_urls()
	ins.craw()


if __name__ == "__main__":
	main()





