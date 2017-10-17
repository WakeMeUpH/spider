import wordcloud
from PIL import Image
import numpy as np
import jieba
import jieba.analyse
from matplotlib import pyplot as plt

class WC_dires(object):
	"""docstring for WC_dirs"""
	def __init__(self):
		self.path = r"F:/Python_Program/douban/director/spider/directors.txt"

	def Read_text(self):
		lyric = ''
		try:
			f = open(self.path,'r')
			lyric = f.read()
			return lyric
		except:
			print("open file error!")
			return None
		finally:
			f.close()

	def Analyse(self,text):
		results = jieba.analyse.extract_tags(text,topK = 100)
		return results


	def Draw(self,results):
		image = np.array(Image.open(r'F:/Python_Program/douban/director/dires.png'))
		wc = wordcloud.WordCloud(background_color = 'white',max_words = 100,mask = image,stopwords = wordcloud.STOPWORDS,font_path = 'C:\Windows\Fonts\STZHONGS.TTF')
		cut_results = " ".join(results)
		wc.generate(cut_results)
		plt.figure()
		plt.imshow(wc)
		plt.axis("off")
		plt.show()

def main():
	we = WC_dires()
	text = we.Read_text()
	data = we.Analyse(text)
	#for item in data:
	#	print(item)
	we.Draw(data)

if __name__ == "__main__":
	main()








