from lib.crawler import Crawler


if __name__ == '__main__':
	seed = [
		# 'https://www.autokelly.bg/',
		# 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm',
		# 'https://bnr.bg/hristobotev/radioteatre/list',
		# 'https://bnr.bg/lyubopitno/list',
		# 'https://www.jobs.bg/front_job_search.php?add_sh=1&from_hp=1&keywords%5B%5D=python',
		# 'https://bnr.bg/lyubopitno/list',
		'https://bnr.bg/hristobotev/radioteatre/list'
	]
	data_path = "./data/"
	crawler = Crawler(seed, data_path)
	crawler.run()
