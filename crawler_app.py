from lib.crawler import Crawler


if __name__ == '__main__':
	base_url = 'https://bnr.bg/hristobotev/radioteatre/list'

	data_path = "./data/"
	crawler = Crawler(base_url, data_path)
	crawler.run()
