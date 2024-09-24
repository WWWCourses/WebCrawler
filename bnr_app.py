# bnr_app.py
import sys
from time import strftime
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QPixmap

from bnr.crawler import Crawler
from bnr.db import DB

import datetime

BASE_URL = 'https://bnr.bg/hristobotev/radioteatre/list'

class TableView(qtw.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.db = DB()

        if not self.db.conn:
            qtw.QMessageBox.critical(
                None,
                "Database Error!",
                "Database Error: %s" % con.lastError().databaseText(),
            )
            return False

        self.data = self.db.select_all_data()
        self.column_names = self.db.get_column_names()

        model = self.setup_model()

        self.filter_proxy_model = qtc.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(model)
        self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(1)

        self.setModel(self.filter_proxy_model)

        self.setup_gui()

    def setup_gui(self):
        rows_count = self.model().rowCount()
        cols_count = self.model().columnCount()

        self.setMinimumWidth(cols_count * 230)
        self.setMinimumHeight(rows_count * 40)

        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.setColumnWidth(3, 300)

        self.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)

        self.setSortingEnabled(True)
        self.sortByColumn(0, qtc.Qt.SortOrder.AscendingOrder)

    def setup_model(self):
        model = qtg.QStandardItemModel()
        model.setHorizontalHeaderLabels(self.column_names)

        for i, row in enumerate(self.data):
            items = []
            for field in row:
                item = qtg.QStandardItem()
                if isinstance(field, datetime.date):
                    field = field.strftime('%d.%m.%Y')
                elif isinstance(field, str) and len(field) > 100:
                    item.setData(field, qtc.Qt.ItemDataRole.UserRole)
                    field = field[0:50] + '...'

                item.setData(field, qtc.Qt.ItemDataRole.DisplayRole)
                items.append(item)

            model.insertRow(i, items)

        return model

    @qtc.pyqtSlot(int)
    def set_filter_column(self, index):
        self.filter_proxy_model.setFilterKeyColumn(index)

    def get_last_updated_date(self):
        last_updated_date = self.db.get_last_updated_date()
        if last_updated_date:
            return last_updated_date.strftime('%d.%m.%y, %H:%M:%S')


class TableViewWidget(qtw.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

        self.setup_gui()

    def setup_gui(self):
        self.tableView = TableView()
        tableViewWidth = self.tableView.frameGeometry().width()

        lblTitle = qtw.QLabel()
        label_msg = f'Radiotheaters publications as crawlled on {self.tableView.get_last_updated_date()}'
        lblTitle.setText(label_msg)
        lblTitle.setStyleSheet('font-size: 30px; margin:20px auto; color: orange;')
        lblTitle.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        filterLabel = qtw.QLabel('Filter by column: ')

        filterLineEdit = qtw.QLineEdit()
        filterLineEdit.textChanged.connect(self.tableView.filter_proxy_model.setFilterRegularExpression)

        comboBox = qtw.QComboBox()
        comboBox.addItems(["{0}".format(col) for col in self.tableView.column_names])
        comboBox.setCurrentText('title')
        comboBox.currentIndexChanged.connect(lambda idx: self.tableView.set_filter_column(idx))

        filterBoxLayout = qtw.QHBoxLayout()
        filterBoxLayout.addWidget(filterLabel)
        filterBoxLayout.addWidget(comboBox)
        filterBoxLayout.addWidget(filterLineEdit)

        btnClose = qtw.QPushButton('Close')
        btnClose.clicked.connect(lambda _: self.close() and self.parent.close())

        layout = qtw.QVBoxLayout()
        layout.addWidget(lblTitle)
        layout.addLayout(filterBoxLayout)
        layout.addWidget(self.tableView)
        layout.addWidget(btnClose)

        self.setLayout(layout)
        self.setFixedWidth(tableViewWidth)

    def close_all(self):
        self.parent.close()
        self.close()

    @qtc.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.tableView.filter_proxy_model.setFilterKeyColumn(index)


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.crawler = Crawler(BASE_URL)

        self.setWindowTitle('BNR Crawler')

        layout = qtw.QVBoxLayout()

        # Add the image
        img_label = qtw.QLabel(self)
        pixmap = QPixmap('./images/DALL·E 2024-09-24 13.04.34 - A dark, misty room with an old-fashioned radio glowing faintly on a wooden table. A cute, spider-like creature with mechanical legs and gears is emerg.webp')
        # Resize the image
        pixmap = pixmap.scaled(600, 400, qtc.Qt.AspectRatioMode.KeepAspectRatio)
        # img_label.setFixedSize(600, 300)  # Adjust the size as needed
        img_label.setPixmap(pixmap)
        img_label.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(img_label)

        btnsLayout = qtw.QHBoxLayout()
        btnCrawlerRun = qtw.QPushButton('Run Crawler')
        self.btnShowData = qtw.QPushButton('Show Data')

        btnsLayout.addWidget(btnCrawlerRun)
        btnsLayout.addWidget(self.btnShowData)
        layout.addLayout(btnsLayout)

        # Add stretch to make sure buttons are visible
        layout.addStretch()

        self.btnShowData.clicked.connect(self.show_data)
        btnCrawlerRun.clicked.connect(self.crawler.run)

        layout.addSpacing(10)

        mainWidget = qtw.QWidget()
        mainWidget.setLayout(layout)

        self.setCentralWidget(mainWidget)

        self.show()

    def show_data(self):
        self.tableViewWidget = TableViewWidget(parent=self)
        self.tableViewWidget.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
