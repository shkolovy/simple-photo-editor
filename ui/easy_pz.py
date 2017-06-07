import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from functools import partial

from img_modifier import img_helper
from img_modifier import color_filter

from PIL import ImageQt

from logging.config import fileConfig
import logging

logger = logging.getLogger()

img_original = None
img_output = None

operations = {
    "color_filter": {
        ""
    },
    "adjusting": {
        "brightness": 0,
        "contrast": 0,
        "sharpness": 0
    },
    "flip_left": False,
    "flip_top": False
}


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
        self.parent = parent

        btn_size = (90, 50)

        rotate_left_btn = QPushButton("↺ 90°")
        rotate_left_btn.setMinimumSize(*btn_size)
        rotate_left_btn.clicked.connect(self.on_rotate_left)

        rotate_right_btn = QPushButton("↻ 90°")
        rotate_right_btn.setMinimumSize(*btn_size)
        rotate_right_btn.clicked.connect(self.on_rotate_right)

        flip_left_btn = QPushButton("⇆")
        flip_left_btn.setMinimumSize(*btn_size)
        flip_left_btn.clicked.connect(self.on_flip_left)

        flip_top_btn = QPushButton("↑↓")
        flip_top_btn.setMinimumSize(*btn_size)
        flip_top_btn.clicked.connect(self.on_flip_top)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(rotate_left_btn)
        btn_layout.addWidget(rotate_right_btn)
        btn_layout.addWidget(QVLine())
        btn_layout.addWidget(flip_left_btn)
        btn_layout.addWidget(flip_top_btn)

        self.setLayout(btn_layout)

    def on_rotate_left(self):
        logger.debug("rotate left")

        global img_output
        img_output = img_helper.rotate(img_output, 90)
        self.parent.parent.place_preview_img(img_output)

    def on_rotate_right(self):
        logger.debug("rotate left")

        global img_output
        img_output = img_helper.rotate(img_output, -90)
        self.parent.parent.place_preview_img(img_output)

    def on_flip_left(self):
        logger.debug("flip left-right")

        global img_output
        img_output = img_helper.flip_left(img_output)
        self.parent.parent.place_preview_img(img_output)

    def on_flip_top(self):
        logger.debug("flip top-bottom")

        global img_output
        img_output = img_helper.flip_top(img_output)
        self.parent.parent.place_preview_img(img_output)


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

    def reset_sliders(self):
        self.brightness_slider.setValue(0)
        self.sharpness_slider.setValue(0)
        self.contrast_slider.setValue(0)

    def on_brightness_slider_released(self):
        logger.debug("brightness selected value: {}".format(self.brightness_slider.value()))
        self.brightness_slider.setToolTip(str(self.brightness_slider.value()))

        factor = _get_converted_point(-100, 100, 0.5, 2, self.brightness_slider.value())
        logger.debug("brightness factor: {}".format(factor))

        img = img_helper.brightness(img_original, factor)
        self.parent.parent.place_preview_img(img)

    def on_sharpness_slider_released(self):
        logger.debug(self.sharpness_slider.value())
        self.sharpness_slider.setToolTip(str(self.sharpness_slider.value()))

        factor = _get_converted_point(-100, 100, 0, 2, self.sharpness_slider.value())
        logger.debug("sharpness factor: {}".format(factor))

        img = img_helper.sharpness(img_original, factor)
        self.parent.parent.place_preview_img(img)

    def on_contrast_slider_released(self):
        logger.debug(self.contrast_slider.value())
        self.contrast_slider.setToolTip(str(self.contrast_slider.value()))

        factor = _get_converted_point(-100, 100, 0.5, 1.5, self.contrast_slider.value())
        logger.debug("contrast factor: {}".format(factor))

        img = img_helper.contrast(img_original, factor)
        self.parent.parent.place_preview_img(img)


class FiltersTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def on_filter_select(self, filter_name, e):
        logger.debug("apply color filter: {}".format(filter_name))

        if filter_name != "none":
            new_img = img_helper.color_filter(img_original, filter_name)
        else:
            new_img = img_original

        global img_output
        img_output = new_img
        self.parent.parent.place_preview_img(new_img)


class MainLayout(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.img_lbl = QLabel('Press Upload to upload the image')
        self.img_lbl.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("Upload")
        upload_btn.setMinimumWidth(100)
        upload_btn.clicked.connect(self.on_upload)
        upload_btn.setStyleSheet("font-weight:bold;")

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setMinimumWidth(100)
        self.reset_btn.clicked.connect(self.on_reset)
        self.reset_btn.setEnabled(False)
        self.reset_btn.setStyleSheet("font-weight:bold;")

        self.save_btn = QPushButton("Save")
        self.save_btn.setMinimumWidth(100)
        self.save_btn.clicked.connect(self.on_save)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("font-weight:bold;")

        self.addWidget(self.img_lbl)
        self.addStretch()

        self.action_tabs = ActionTabs(self)
        self.addWidget(self.action_tabs)
        self.action_tabs.setVisible(False)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(upload_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.save_btn)

        self.addLayout(btn_layout)

    def place_preview_img(self, img):
        preview_pix = ImageQt.toqpixmap(img)
        self.img_lbl.setPixmap(preview_pix)

    def on_save(self):
        logger.debug("open save dialog")
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "QFileDialog.getSaveFileName()", "",
                                                   "Images (*.png *.jpg)")

        if file_name:
            logger.debug("save output imgage to {}".format(file_name))
            img_output.save(file_name)

    def on_upload(self):
        logger.debug("upload")
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open image", "/Users",
                                                   "Images (*.png *jpg)")

        if file_name:
            logger.debug(file_name)

            pix = QPixmap(file_name)
            self.img_lbl.setPixmap(pix)
            self.img_lbl.setScaledContents(True)
            self.action_tabs.setVisible(True)
            self.action_tabs.adjustment_tab.reset_sliders()

            global img_original
            img_original = ImageQt.fromqpixmap(pix)

            global img_output
            img_output = img_original.copy()

            img_filter_thumb = img_helper.resize(img_original, 120, 120)

            main_layout = QHBoxLayout()
            main_layout.setAlignment(Qt.AlignCenter)

            some_lbl = self.create_filter_thumb(img_filter_thumb, "none", "")
            main_layout.addWidget(some_lbl)

            for key, val in color_filter.ColorFilters.filters.items():
                logger.debug("create img thumb for: {}".format(key))

                some_lbl = self.create_filter_thumb(img_filter_thumb, key, val)
                main_layout.addWidget(some_lbl)
                self.action_tabs.filter_tab.setLayout(main_layout)

            self.reset_btn.setEnabled(True)
            self.save_btn.setEnabled(True)

    def create_filter_thumb(self, img_filter_thumb, filter_key, filter_name):
        if filter_key != "none":
            img_filter_preview = img_helper.color_filter(img_filter_thumb, filter_key)
        else:
            img_filter_preview = img_filter_thumb

        preview_pix = ImageQt.toqpixmap(img_filter_preview)

        some_lbl = QLabel()
        some_lbl.setStyleSheet("border:1px solid #ccc;")

        if filter_key != "none":
            some_lbl.setToolTip('Apply <b>{0}</b> filter'.format(filter_name))
        else:
            some_lbl.setToolTip('No filter')

        some_lbl.setCursor(Qt.PointingHandCursor)
        some_lbl.setScaledContents(True)

        some_lbl.setPixmap(preview_pix)

        some_lbl.mousePressEvent = partial(self.action_tabs.filter_tab.on_filter_select, filter_key)

        return some_lbl

    def on_reset(self):
        logger.debug("reset all")

        global img_output
        img_output = img_original.copy()
        self.place_preview_img(img_original)
        self.action_tabs.adjustment_tab.reset_sliders()


class EasyPzUI(QWidget):
    def __init__(self):
        super().__init__()

        self.has_changes = False

        self.main_layout = MainLayout(self)
        self.setLayout(self.main_layout)

        self.setMinimumSize(300, 300)
        self.setMaximumSize(900, 900)
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Easy Peasy - Lemon Squeezy')
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


def _get_converted_point(user_p1, user_p2, p1, p2, x):
    """
    convert user ui slider selected value (x) to PIL value
    user ui slider scale is -100 to 100, PIL scale is -1 to 2
    example:
     - user slected 50
     - pil value is 1.25
    """

    # need to know how much x from p1 to p2
    r = (x - user_p1) / (user_p2 - user_p1)
    return p1 + r * (p2 - p1)


if __name__ == '__main__':
    fileConfig('logging_config.ini')

    app = QApplication(sys.argv)
    win = EasyPzUI()
    sys.exit(app.exec_())

