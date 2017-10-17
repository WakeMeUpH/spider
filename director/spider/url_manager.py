class url_manager(object):
	def __init__(self):
		self.new_urls = set()
		self.old_urls = set()

	def get_url(self):
		#获取一个未爬取的url
		if self.has_new_url():
			new_url = self.new_urls.pop()
			self.old_urls.add(new_url)
			return new_url


	def add_urls(self,urls):
		#加入未爬取的url到new_urls
		if len(urls) != 0:
			for url in urls:
				if url in self.new_urls or url in self.old_urls:
					continue
				self.new_urls.add(url)

	def has_new_url(self):
		return len(self.new_urls) != 0

