class outputer:
	
	def save(self,datas):
		try:
			f = open("directors.txt",'w')
			for data in datas:
				f.write(data)
				f.write('\n')
				#print("in outputer: %s"%(data))
			#f.close()
		except:
			print("read file error!")
