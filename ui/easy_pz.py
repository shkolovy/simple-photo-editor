import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from functools import partial

from img_modifier import img_commander
from img_modifier import color_filter

from PIL import ImageQt

from logging.config import fileConfig
import logging

logger = logging.getLogger()


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class ActionTabs(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.filter_tab = FiltersTab(self)
        self.adjustment_tab = AdjustmentTab(self)
        self.modification_tab = ModificationTab(self)
        self.rotation_tab = RotationTab(self)

        self.addTab(self.filter_tab, "Filters")
        self.addTab(self.adjustment_tab, "Adjusting")
        self.addTab(self.modification_tab, "Modification")
        self.addTab(self.rotation_tab, "Rotation")

        self.setMaximumHeight(190)


class RotationTab(QWidget):
    def __init__(self, parent):
        super().__init__()

        btn_size = (90, 50)

        rotate_left_btn = QPushButton("↺ 90°")
        rotate_left_btn.setMinimumSize(*btn_size)

        rotate_right_btn = QPushButton("↻ 90°")
        rotate_right_btn.setMinimumSize(*btn_size)

        flip_left_btn = QPushButton("⇆")
        flip_left_btn.setMinimumSize(*btn_size)

        flip_top_btn = QPushButton("↑↓")
        flip_top_btn.setMinimumSize(*btn_size)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(rotate_left_btn)
        btn_layout.addWidget(rotate_right_btn)
        btn_layout.addWidget(QVLine())
        btn_layout.addWidget(flip_left_btn)
        btn_layout.addWidget(flip_top_btn)

        self.setLayout(btn_layout)


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


class AdjustmentTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        contrast_lbl = QLabel("Contrast")
        contrast_lbl.setAlignment(Qt.AlignCenter)

        brightness_lbl = QLabel("Brightness")
        brightness_lbl.setAlignment(Qt.AlignCenter)

        sharpness_lbl = QLabel("Sharpness")
        sharpness_lbl.setAlignment(Qt.AlignCenter)

        self.contrast_slider = QSlider(Qt.Horizontal, self)
        self.contrast_slider.setMinimum(-100)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.sliderReleased.connect(self.on_contrast_slider_released)
        self.contrast_slider.setToolTip(str(0))

        self.brightness_slider = QSlider(Qt.Horizontal, self)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.sliderReleased.connect(self.on_brightness_slider_released)
        self.brightness_slider.setToolTip(str(0))

        self.sharpness_slider = QSlider(Qt.Horizontal, self)
        self.sharpness_slider.setMinimum(-100)
        self.sharpness_slider.setMaximum(100)
        self.sharpness_slider.setValue(0)
        self.sharpness_slider.sliderReleased.connect(self.on_sharpness_slider_released)
        self.sharpness_slider.setToolTip(str(0))

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(contrast_lbl)
        main_layout.addWidget(self.contrast_slider)

        main_layout.addWidget(brightness_lbl)
        main_layout.addWidget(self.brightness_slider)

        main_layout.addWidget(sharpness_lbl)
        main_layout.addWidget(self.sharpness_slider)

        self.setLayout(main_layout)

    def on_brightness_slider_released(self):
        logger.debug(self.brightness_slider.value())
        self.brightness_slider.setToolTip(str(self.brightness_slider.value()))

        # self.parent.parent.IMG.brightness(self.brightness_slider.value())
        # img = self.parent.parent.IMG.get_img()
        # preview_pix = ImageQt.toqpixmap(img)
        # self.parent.parent.img_lbl.setPixmap(preview_pix)

    def on_sharpness_slider_released(self):
        logger.debug(self.sharpness_slider.value())
        self.sharpness_slider.setToolTip(str(self.sharpness_slider.value()))

    def on_contrast_slider_released(self):
        logger.debug(self.contrast_slider.value())
        self.contrast_slider.setToolTip(str(self.contrast_slider.value()))


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
        upload_btn.setStyleSheet("font-weight:bold;")

        reset_btn = QPushButton("Reset")
        reset_btn.setMinimumWidth(100)
        reset_btn.clicked.connect(self.on_reset)
        reset_btn.setEnabled(False)
        reset_btn.setStyleSheet("font-weight:bold;")

        save_btn = QPushButton("Save")
        save_btn.setMinimumWidth(100)
        save_btn.clicked.connect(self.on_save)
        save_btn.setEnabled(False)
        save_btn.setStyleSheet("font-weight:bold;")

        self.addWidget(self.img_lbl)
        self.addStretch()

        self.action_tabs = ActionTabs(self)
        self.addWidget(self.action_tabs)
        self.action_tabs.setVisible(False)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(upload_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(save_btn)

        self.addLayout(btn_layout)

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

            self.IMG = img_commander.ImgCommander(file_name)
            self.IMG.resize(200, 200)

            main_layout = QHBoxLayout()
            main_layout.setAlignment(Qt.AlignCenter)

            for key, val in color_filter.ColorFilters.filters.items():
                imgc = img_commander.ImgCommander(file_name)
                imgc.resize(120, 120)
                imgc.filter(key)
                img = imgc.get_img()

                preview_pix = ImageQt.toqpixmap(img)

                tab = self.action_tabs.filter_tab
                some_lbl = QLabel()
                some_lbl.setStyleSheet("border:1px solid #ccc;")
                some_lbl.setToolTip('Apply <b>{0}</b> filter'.format(val))
                some_lbl.setCursor(Qt.PointingHandCursor)
                some_lbl.setScaledContents(True)
                main_layout.addWidget(some_lbl)
                some_lbl.setPixmap(preview_pix)

                some_lbl.mousePressEvent = partial(tab.on_filter_select, key)
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

