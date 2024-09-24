from bs4 import BeautifulSoup
import re
import datetime
from dateutil.relativedelta import relativedelta

class Scraper:
	def __init__(self, html):
		self.html = html
		self.soup = BeautifulSoup(html, 'html.parser')


	def is_past_year_ago(self,date):
		now = datetime.datetime.now()
		date_diff = relativedelta(now, date)

		return  True if date_diff.years<1 else False

	def get_pub_date(self,html):
		date_rx = re.compile(r'(\d{2}\.\d{2}\.\d{2})')

		# get date element
		pub_date_div = html.select_one('.date')

		# extract date from pub_date_div content
		m = date_rx.search(str(pub_date_div))
		if m:
			pub_date = m[1]
			pub_date = datetime.datetime.strptime(pub_date, '%d.%m.%y')

		return pub_date


	def get_pubs_urls(self):
		pubs_html = self.soup.select('#module_1_2 .row-fluid > .span8')

		pubs_urls = []

		for pub_div in pubs_html:
			pub_date = self.get_pub_date(pub_div)

			# Retrieve publication details only for entries from the past year
			if self.is_past_year_ago(pub_date):
				a = pub_div.find('a')
				pubs_urls.append(a['href'])

			# print(pub_data['date'])
		print(f'pubs_urls: {pubs_urls}')
		return pubs_urls

	def get_pub_data(self):
		# get publication title:
		title = self.soup.h1.getText(strip=True)

		# get publication date:
		pub_date = self.get_pub_date(self.soup)
		pub_date_str = pub_date.strftime('%Y-%m-%d')

		# get publication content:
		pub_content = self.soup.find('span', itemprop="articleBody").getText(strip=True)

		return {
			'title':title,
			'pub_date_str':pub_date_str,
			'pub_content':pub_content
		}


