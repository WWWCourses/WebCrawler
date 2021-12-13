import requests
import re
import threading
from bs4 import BeautifulSoup as bs

class Crawler():
	def __init__(self, seed, data_path):
		self.seed = seed
		self.data_path = data_path

	def make_filename(self,url):
		""" Extracts domain from a url.
			Prepend data_path and append '.html'

			:param url: string

			return <domain>.html string
		"""
		rx = re.compile(r'^https?:\/\/(?:www.)?([^\/]+)\/?')
		m = rx.search(url)
		if m:
			filename = self.data_path + m[1]  + '.html'
			# print(filename)
			return filename
		else:
			print(f'Can not get domain from {url}')
			exit(-1)

	def write_to_file(self,filename, content):
		""" Write string to given filename
				:param filename: string
				:param content: sring
		"""
		try:
			with open(filename, 'w') as f:
				f.write(content)
		except FileNotFoundError:
			print(f'File {filename} does not exists!')
		except Exception as e:
			print(f'Can not write to file: {filename}: {str(e)}')
			exit(-1)

	def get_html(self,url):
		# GET request without SSL verification:
		try:
			r = requests.get(url)
		except requests.RequestException:
			# try with SSL verification disabled.
			# this is just a dirty workaraound
			# check https://levelup.gitconnected.com/solve-the-dreadful-certificate-issues-in-python-requests-module-2020d922c72f
			r = requests.get(url,verify=False)
		except Exception as e:
			print('Ca not get url: {url}: {str(e)}!')
			exit(-1)

		# set content encoding explicitely
		r.encoding="utf-8"

		# if we have the html => save it into file
		if r.ok:
			html = r.text

		return html

	def crawl_page(self, url):
		html = self.get_html(url)
		filename = self.make_filename(url)
		self.write_to_file(filename, html)

	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""
		for url in self.seed:
			tr = threading.Thread(target=self.crawl_page(url))
			tr.start()

if __name__ == '__main__':
	seed = [
		'https://www.autokelly.bg/',
		'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm',
		'https://bnr.bg/hristobotev/radioteatre/list',
		'https://bnr.bg/lyubopitno/list',
		'https://www.jobs.bg/front_job_search.php?add_sh=1&from_hp=1&keywords%5B%5D=python',
		'https://bnr.bg/lyubopitno/list'
	]
	crawler = Crawler(seed, "../data/")
	crawler.run()
