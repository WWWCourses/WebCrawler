import datetime

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

from bnr.db import DB


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

        filterComboBox = qtw.QComboBox()
        filterComboBox.addItems([f"{col}" for col in self.tableView.column_names])
        filterComboBox.setCurrentText('title')
        filterComboBox.currentIndexChanged.connect(lambda idx: self.tableView.set_filter_column(idx))

        filterLineEdit = qtw.QLineEdit()
        filterLineEdit.textChanged.connect(self.tableView.filter_proxy_model.setFilterRegularExpression)


        filterBoxLayout = qtw.QHBoxLayout()
        filterBoxLayout.addWidget(filterLabel)
        filterBoxLayout.addWidget(filterComboBox)
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
    def on_filterComboBox_currentIndexChanged(self, index):
        self.tableView.filter_proxy_model.setFilterKeyColumn(index)

