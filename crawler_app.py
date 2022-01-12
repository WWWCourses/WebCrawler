import threading
from lib.crawler import Crawler

class App():



base_url = 'https://bnr.bg/hristobotev/radioteatre/list'
crawler = Crawler(base_url)
crawler.run()

