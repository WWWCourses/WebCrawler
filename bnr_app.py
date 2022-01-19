import sys
from time import strftime
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from lib.crawler import Crawler
from lib.db import DB

import datetime
import threading

class TableView(qtw.QTableView):
	def __init__(self, *args, **kwargs):
		super().__init__()

		self.db = DB()
		self.data = self.db.select_all_data()
		self.column_names = self.db.get_column_names()

		model = self.setup_model()
		self.setModel(model)

		self.setup_gui()

		# self.showColumn(2)

	def setup_gui(self):
		### set table dimensions:
		# get rows and columns count from model:
		rows_count = self.model().rowCount()
		cols_count = self.model().columnCount()

		self.setMinimumWidth(cols_count*230);
		self.setMinimumHeight(rows_count*40);

		### resize cells to fit the content:
		# self.resizeRowsToContents()
		# self.resizeColumnsToContents()
		# set width of separate columns:
		self.resizeColumnToContents(0)
		self.resizeColumnToContents(1)
		self.setColumnWidth(3, 300)


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

	def setup_model(self):
		model = qtg.QStandardItemModel()
		model.setHorizontalHeaderLabels(self.column_names)

		for i, row in enumerate(self.data):
			# items = [qtg.QStandardItem(str(item)) for item in row]

			items = []
			for field in row:
				item = qtg.QStandardItem()
				if isinstance(field, datetime.date):
					field = field.strftime('%d.%m.%y')
				elif isinstance(field, str) and len(field)>100:
					# set full string with UserRole for later use:
					item.setData(field, qtc.Qt.UserRole)
					# trim string for display
					field = field[0:50]+'...'

				item.setData(field, qtc.Qt.DisplayRole)
				items.append(item)

			model.insertRow(i, items)


		return model

	def get_last_updated_date(self):
		last_updated_date=self.db.get_last_updated_date()
		return last_updated_date.strftime('%d.%m.%y, %H:%M:%S')

class TableViewWidget(qtw.QWidget):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.parent = parent

		self.setup_gui()

	def setup_gui(self):
		# table view:
		tableView = TableView()
		tableViewWidth = tableView.frameGeometry().width()
		tableViewHeight = tableView.frameGeometry().height()
		print(tableViewWidth, tableViewHeight)

		# label
		lblTitle = qtw.QLabel()
		label_msg = f'Radiotheaters publications as scrolled on {tableView.get_last_updated_date()}'
		lblTitle.setText(label_msg)
		lblTitle.setStyleSheet('''
			font-size: 30px;
			margin:20px auto;
			color: purple;

		''')
		lblTitle.setAlignment(qtc.Qt.AlignCenter)


		# close button
		btnClose = qtw.QPushButton('Close')
		# btnClose.clicked.connect(self.close_all)
		# or with lambda syntax
		btnClose.clicked.connect( lambda _:self.close() and self.parent.close() )

		# main layout
		layout = qtw.QVBoxLayout()
		layout.addWidget(lblTitle)
		layout.addWidget(tableView)
		layout.addWidget(btnClose)

		self.setLayout(layout)

		self.setFixedWidth(tableViewWidth)
		self.setFixedHeight(tableViewHeight)

	def close_all(self):
		self.parent.close()
		self.close()

	def get_current_datetime(self):
		return datetime.datetime.now().strftime('%d.%m.%y, %H:%M:%S')

class MainWindow(qtw.QMainWindow):
	def __init__(self , *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setWindowTitle('BNR Crawler')

		layout = qtw.QVBoxLayout()
		lblTableCaption = qtw.QLabel('Radiotheaters Data')
		lblTableCaption.setObjectName('lblTableCaption')
		lblTableCaption.setAlignment(qtc.Qt.AlignCenter)
		layout.addWidget(lblTableCaption)

		btnsLayout = qtw.QHBoxLayout()
		btnCrawlerRun = qtw.QPushButton('Run Crawler')
		btnShowData = qtw.QPushButton('Show Data')
		btnsLayout.addWidget(btnCrawlerRun)
		btnsLayout.addWidget(btnShowData)
		layout.addLayout(btnsLayout)

		# actions on buttons click:
		btnShowData.clicked.connect(self.show_data)
		btnCrawlerRun.clicked.connect(self.run_crawler)

		# add spacer or just fixed spacing
		layout.addSpacing(10)
		# layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

		mainWidget = qtw.QWidget()
		mainWidget.setLayout(layout)

		self.setCentralWidget(mainWidget)

		self.show();

	def show_data(self):
		self.tableViewWidget = TableViewWidget(parent=self)
		self.tableViewWidget.show()

	def run_crawler(self):
		self.setCursor(qtc.Qt.WaitCursor)
		base_url = 'https://bnr.bg/hristobotev/radioteatre/list'
		crawler = Crawler(base_url)

		crawler.run()

		self.setCursor(qtc.Qt.ArrowCursor)


if __name__ == '__main__':
	app = qtw.QApplication(sys.argv);

	window = MainWindow()

	sys.exit(app.exec_())
