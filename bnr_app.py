# bnr_app.py
import sys

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6.QtGui import QPixmap

from bnr.crawler import Crawler
from bnr.ui import TableViewWidget


BASE_URL = 'https://bnr.bg/hristobotev/radioteatre/list'

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
