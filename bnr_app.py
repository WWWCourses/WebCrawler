from itertools import count
import threading
from time import strftime
import os

from lib.crawler import Crawler
from lib.db import DB

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtSql as qtSQL

import datetime

class TableView(qtw.QTableView):
	def __init__(self, *args, **kwargs):
		super().__init__()

		db = DB()
		self.data = db.select_all_data()
		self.column_names = db.get_column_names()

		model = self.setup_model()
		self.setModel(model)

		self.setup_gui()

		# self.showColumn(2)

	def setup_gui(self):
		### set table dimensions:
		# get rows and columns count from model:
		rows_count = self.model().rowCount()
		cols_count = self.model().columnCount()

		self.setMinimumWidth(cols_count*350);
		self.setMinimumHeight(rows_count*40);

		### resize cells to fit the content:
		# self.resizeRowsToContents()
		# self.resizeColumnsToContents()
		# set width of separate columns:
		self.resizeColumnToContents(0)
		self.resizeColumnToContents(1)
		self.setColumnWidth(3, 500)


		# streach table:
		# self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
		# self.horizontalHeader().setStretchLastSection(True)
		# self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
		# self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents);


		# set all cells hight
		# header = self.verticalHeader()
		# header.setDefaultSectionSize(50)
		# header.setSectionResizeMode(qtw.QHeaderView.Fixed)

		# enable columns move
		# self.horizontalHeader().setSectionsMovable(True)

		# enable columns sort
		self.setSortingEnabled(True)
		self.sortByColumn(2,qtc.Qt.AscendingOrder)
		pass

	def setup_model(self):
		model = qtg.QStandardItemModel()
		model.setHorizontalHeaderLabels(self.column_names)

		for i, row in enumerate(self.data):
			# items = [qtg.QStandardItem(str(item)) for item in row]

			items = []
			for field in row:

				if isinstance(field, datetime.date):
					field = field.strftime('%d.%m.%y')


				item = qtg.QStandardItem()
				item.setData(field, qtc.Qt.DisplayRole)
				items.append(item)

			model.insertRow(i, items)


		return model


class MainWindow(qtw.QMainWindow):
	def __init__(self , *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setWindowTitle('BNR Crawler')

		layout = qtw.QVBoxLayout();
		table_caption = qtw.QLabel('Radiotheaters Data')
		table_caption.setObjectName('table_caption')

		# we cannot align label in style (text-align:center) is not supported on labels, so must do it here:
		table_caption.setAlignment(qtc.Qt.AlignCenter)

		layout.addWidget(table_caption)

		self.table_view = TableView()
		layout.addWidget(self.table_view)

		main_widget = qtw.QWidget()
		main_widget.setLayout(layout)

		self.setCentralWidget(main_widget)

		self.show();


if __name__ == '__main__':
	# base_url = 'https://bnr.bg/hristobotev/radioteatre/list'
	# crawler = Crawler(base_url)
	# crawler.run()


	app = qtw.QApplication(sys.argv);

	window = MainWindow()

	sys.exit(app.exec_())
