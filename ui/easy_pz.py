import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QPixmap

from functools import partial

from img_modifier import img_commander
from img_modifier import color_filter

from PIL import ImageQt

from logging.config import fileConfig
import logging

logger = logging.getLogger()


class ActionTabs(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.filter_tab = FiltersTab(self)
        self.adjusting_tab = AdjustingTab(self)
        self.modification_tab = ModificationTab(self)

        self.addTab(self.filter_tab, "Filters")
        self.addTab(self.adjusting_tab, "Adjusting")
        self.addTab(self.modification_tab, "Modification")

        self.setMaximumHeight(200)


class ModificationTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        some_lbl = QLabel('Hello tab1 Hello tab1 Hello tab1 Hello tab1 ', self)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(some_lbl)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def on_click(self):
        self.parent.parent.img_lbl.setText("ccccc")
        print(111)


class AdjustingTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        some_lbl = QLabel('Hello tab1 Hello tab1 Hello tab1 Hello tab1 ', self)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(some_lbl)
        main_layout.addStretch()
        self.setLayout(main_layout)


class FiltersTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def on_filter_select(self, filter_name, e):
        # self.parent.parent.img_lbl.setText(str(self))
        print(filter_name)


class MainLayout(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.img_lbl = QLabel('Press Upload to upload an image')
        self.img_lbl.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("Upload")
        upload_btn.setMinimumWidth(100)
        upload_btn.clicked.connect(self.on_upload)

        reset_btn = QPushButton("Reset")
        reset_btn.setMinimumWidth(100)
        reset_btn.clicked.connect(self.on_reset)
        reset_btn.setEnabled(False)

        save_btn = QPushButton("Save")
        save_btn.setMinimumWidth(100)
        save_btn.clicked.connect(self.on_save)
        save_btn.setEnabled(False)

        self.addWidget(self.img_lbl)
        self.addStretch()

        self.action_tabs = ActionTabs(self)
        self.addWidget(self.action_tabs)
        # todo: hide it
        self.action_tabs.setVisible(False)

        button_l = QHBoxLayout()
        button_l.setAlignment(Qt.AlignCenter)
        button_l.addWidget(upload_btn)
        button_l.addWidget(reset_btn)
        button_l.addWidget(save_btn)

        self.addLayout(button_l)

    def on_save(self):
        logger.debug("save")
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;Images (*.png *.jpg)")

        if file_name:
            logger.debug(file_name)

    def on_upload(self):
        logger.debug("upload")
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open image", "/Users",
                                                   "Images (*.png *jpg)")

        if file_name:
            logger.debug(file_name)

            pix = QPixmap(file_name)
            self.img_lbl.setScaledContents(True)
            self.img_lbl.setPixmap(pix)
            self.action_tabs.setVisible(True)


            main_layout = QHBoxLayout()
            main_layout.setAlignment(Qt.AlignCenter)

            for f in color_filter.ColorFilters.items:
                imgc = img_commander.ImgCommander(file_name)
                imgc.resize(100, 100)
                imgc.filter(f)
                img = imgc.get_img()

                preview_pix = ImageQt.toqpixmap(img)

                tab = self.action_tabs.filter_tab
                some_lbl = QLabel()
                some_lbl.setStyleSheet("border:1px solid #ccc;")
                some_lbl.setCursor(Qt.PointingHandCursor)
                some_lbl.setScaledContents(True)
                main_layout.addWidget(some_lbl)
                some_lbl.setPixmap(preview_pix)

                some_lbl.mousePressEvent = partial(tab.on_filter_select, f)
                tab.setLayout(main_layout)


    def on_reset(self):
        logger.debug("reset")
        # self.img_lbl.resize(self.img_lbl.width(), 100)


class EasyPzUI(QWidget):
    def __init__(self):
        super().__init__()

        self.has_changes = False

        self.main_layout = MainLayout(self)
        self.setLayout(self.main_layout)

        self.setMinimumSize(300, 300)
        self.setMaximumSize(900, 900)
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Easy Peasy')
        self.center()
        self.show()

    def center(self):
        """align window center"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        logger.debug("close")
        if self.has_changes:
            reply = QMessageBox.question(self, 'You have unsaved changes',
                                         "Are you sure?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def resizeEvent(self, e):
        pass


if __name__ == '__main__':
    fileConfig('logging_config.ini')

    app = QApplication(sys.argv)
    win = EasyPzUI()
    sys.exit(app.exec_())

