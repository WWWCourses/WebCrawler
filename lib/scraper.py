from bs4 import BeautifulSoup
import re
import datetime
from dateutil.relativedelta import relativedelta

class Scraper:
	def __init__(self, html):
		self.html = html
		self.soup = BeautifulSoup(html, 'html.parser')
		self.date_rx = re.compile(r'(\d{2}\.\d{2}\.\d{2})')


	def is_past_year_ago(self,date):
		now = datetime.datetime.now()
		date_diff = relativedelta(now, date)
		# print(date_diff.months)

		return  True if date_diff.months<=12 else False



	def get_pubs_data(self):
		# pubs_container = self.soup.find('div', id="module_1_1")
		pubs_html = self.soup.select('#module_1_1 .row-fluid > .span8')

		pubs_data = []


		for pub_div in pubs_html:
			# store data needed into a dictionary
			pub_data = {}

			# get date element
			pub_date_div = pub_div.select_one('.date')
			# print(pub_date_div)

			# extract date from pub_date_div content
			m = self.date_rx.search(str(pub_date_div))
			if m:
				pub_date = m[1]
				pub_date = datetime.datetime.strptime(pub_date, "%d.%m.%y")


			# get publication details only if date is past year ago
			if self.is_past_year_ago(pub_date):
				a = pub_div.find('a')
				pub_data['title'] = a.string
				pub_data['url'] = a['href']

				pubs_data.append(pub_data)

			# print(pub_data['date'])

		return pubs_data