from bs4 import BeautifulSoup
import re

class Scraper:
	def __init__(self, html):
		self.html = html
		self.soup = BeautifulSoup(html, 'html.parser')
		self.date_rx = re.compile(r'(\d{2}\.\d{2}\.\d{2})')


	def get_publications_container(self):
		# pubs_container = self.soup.find('div', id="module_1_1")
		pubs_html = self.soup.select('#module_1_1 .row-fluid>.span8')
		print(len(pubs_html))


		for pub_div in pubs_html:
			# store data needed into a dictionary
			pub_data = {}

			# get date element
			pub_date_div = pub_div.select('.date')

			# extract date from pub_date_div content
			m = self.date_rx.search(pub_date_div.string)
			if m:
				pub_data['date'] = m[1]

			a = pub_div.find('a')
			pub_data['title'] = a.string
			pub_data['url'] = a['href']

			print(pub_data['date'])
