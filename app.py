import requests
import threading
import sys
import re
import time
from urllib.parse import urlparse
# made by munsiwoo

access_list = open('access_list.txt', 'r').read()
access_list = access_list.split('\n')
index = 0

def url_check(url) :
	regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	result = re.match(regex, url)

	if(result is None) :
		print('Invalid URL!')
		exit(0)
	else :
		return True

def init_url() :
	global url

	try :
		url = sys.argv[1]
	except :
		print('URL target is missing!')
		exit(0)

	url_check(url)

	if(url[-1] == '/') :
		url = url[:-1]

def check_status() :
	global index

	request_url = url + '/' + access_list[index]
	index += 1

	r = requests.get(request_url, allow_redirects=False)
	
	if(r.status_code != 404) :
		print(r.status_code, request_url)

class Sema(threading.Thread) :
	def run(self) :
		sem.acquire()
		check_status()
		sem.release()

if __name__ == '__main__' :
	init_url()

	sem = threading.Semaphore(20) # 동시에 실행되는 스레드 개수 제한
	thread_num = 100 # 스레드 생성 개수 제한
	threads = []

	off, tmp = (0,0)

	while True :
		for i in range(thread_num) :
			tmp += 1
			threads.append(Sema())
			
			if(tmp == len(access_list)) :
				off = 1
				break

		for th in threads :
			th.start()

		for th in threads :
			th.join()

		threads = []

		if(off) :
			print('End')
			break