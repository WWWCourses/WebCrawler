import requests
import re
import threading
import time

try:
	from bnr.scraper import Scraper
	from bnr.db import DB
except:
	from scraper import Scraper
	from db import DB

class Crawler():
	def __init__(self, base_url, data_path='./data/'):
		self.base_url = base_url
		self.seed = []
		self.visited = []
		self.data_path = data_path
		self.current_page_number = 1

		self.db = DB()
		# self.db.drop_radiotheaters_table()
		# self.db.create_radiotheaters_table()

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
			with open(filename, 'w',encoding='utf-8') as f:
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

	def get_seed(self, url):
		print(f'Crawling main page {self.current_page_number}: {url}')
		html = self.get_html(url)

		scraper = Scraper(html)
		pubs_urls = scraper.get_pubs_urls()

		# if pubs_urls is not empy => crawl next
		if pubs_urls:
			# prepend 'https://bnr.bg' to pubs_urls:
			pubs_urls = ['https://bnr.bg'+url for url in pubs_urls]

			# concatenate pubs.urls to self.seed
			self.seed = [*self.seed, *pubs_urls]

			# make next page url
			self.current_page_number+=1
			next_page_url = f'{self.base_url}?page_1_1={self.current_page_number}'

			# get urls from next_page_url
			self.get_seed(next_page_url)

	def get_pub_data(self, url):
		print(f'Crawling page: {url}')
		html = self.get_html(url)

		scraper = Scraper(html)
		pub_data = scraper.get_pub_data()

		return pub_data

	def save_pub_data(self,url):
		pub_data = self.get_pub_data(url)
		# print(f'Save to db: ', pub_data)

		self.db.insert_row(pub_data)
		# self.db.conn.close()

	def run(self):
		# get all URLs to be scraped from base_url
		self.get_seed(self.base_url)
		print(f'Seed contains {len(self.seed)} urls')

		# threads_number = len(self.seed)
		self.alive = True

		start = time.time()
		for url in self.seed:
			# tr = threading.Thread(target=self.save_pub_data, args=(url,))
			# tr.start()
			# tr.join()

			# comment above and uncomment next to test without threading:
			self.save_pub_data(url)

		end = time.time()
		print(f'Time elapsed: {end-start}')

		self.alive = False
		print('Crawler finished its job!')

	def is_alive(self):
		return self.alive


if __name__ == '__main__':
	base_url = 'https://bnr.bg/hristobotev/radioteatre/list'
	crawler = Crawler(base_url)
	crawler.run()
