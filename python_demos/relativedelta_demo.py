import datetime
from dateutil.relativedelta import relativedelta

def is_past_year_ago(date):
	now = datetime.datetime.now()
	date_diff = relativedelta(now, date)
	print(date_diff.years)

	return  True if date_diff.months<=12 else False


pub_date = '11.01.21'
pub_date = datetime.datetime.strptime(pub_date, "%d.%m.%y")

is_past_year_ago(pub_date)