import sys
import ntpath

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from functools import partial

from img_modifier import img_helper
from img_modifier import color_filter

from PIL import ImageQt

from logging.config import fileConfig
import logging

logger = logging.getLogger()

img_original = None
img_output = None

# constants
THUMB_BORDER_COLOR_ACTIVE = "#3893F4"
THUMB_BORDER_COLOR = "#ccc"
BTN_MIN_WIDTH = 120
ROTATION_BTN_SIZE = (70, 30)
THUMB_SIZE = 120

SLIDER_MIN_VAL = -100
SLIDER_MAX_VAL = 100
SLIDER_DEF_VAL = 0


class OPERATIONS:
    COLOR_FILTER = None

    FLIP_LEFT = False
    FLIP_RIGHT = False
    ROTATION_ANGLE = 0

    class ADJUSTING:
        BRIGHTNESS = 0
        SHARPNESS = 0
        CONTRAST = 0

    @staticmethod
    def reset():
        OPERATIONS.ADJUSTING.BRIGHTNESS = 0
        OPERATIONS.ADJUSTING.SHARPNESS = 0
        OPERATIONS.ADJUSTING.CONTRAST = 0

        OPERATIONS.FLIP_LEFT = False
        OPERATIONS.FLIP_RIGHT = False
        OPERATIONS.ROTATION_ANGLE = 0

        OPERATIONS.COLOR_FILTER = None

    @staticmethod
    def has_changes():
        if OPERATIONS.COLOR_FILTER or OPERATIONS.FLIP_LEFT\
                or OPERATIONS.FLIP_RIGHT or OPERATIONS.ROTATION_ANGLE\
                or OPERATIONS.ADJUSTING.CONTRAST or OPERATIONS.ADJUSTING.BRIGHTNESS\
                or OPERATIONS.ADJUSTING.SHARPNESS:
            return True
        else:
            return False


def _get_ratio_height(width, height, r_width):
    return int(r_width/width*height)


def _get_ratio_width(width, height, r_height):
    return int(r_height/height*width)


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


class QVLine(QFrame):
    """Vertical line"""
    """Vertical line"""

    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class ActionTabs(QTabWidget):
    """Action tabs widget"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.filters_tab = FiltersTab(self)
        self.adjustment_tab = AdjustingTab(self)
        self.modification_tab = ModificationTab(self)
        self.rotation_tab = RotationTab(self)

        self.addTab(self.filters_tab, "Filters")
        self.addTab(self.adjustment_tab, "Adjusting")
        self.addTab(self.modification_tab, "Modification")
        self.addTab(self.rotation_tab, "Rotation")

        self.setMaximumHeight(190)


class RotationTab(QWidget):
    """Rotation tab widget"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        rotate_left_btn = QPushButton("↺ 90°")
        rotate_left_btn.setMinimumSize(*ROTATION_BTN_SIZE)
        rotate_left_btn.clicked.connect(self.on_rotate_left)

        rotate_right_btn = QPushButton("↻ 90°")
        rotate_right_btn.setMinimumSize(*ROTATION_BTN_SIZE)
        rotate_right_btn.clicked.connect(self.on_rotate_right)

        flip_left_btn = QPushButton("⇆")
        flip_left_btn.setMinimumSize(*ROTATION_BTN_SIZE)
        flip_left_btn.clicked.connect(self.on_flip_left)

        flip_top_btn = QPushButton("↑↓")
        flip_top_btn.setMinimumSize(*ROTATION_BTN_SIZE)
        flip_top_btn.clicked.connect(self.on_flip_top)

        rotate_lbl = QLabel("Rotate")
        rotate_lbl.setAlignment(Qt.AlignCenter)
        rotate_lbl.setFixedWidth(140)

        flip_lbl = QLabel("Flip")
        flip_lbl.setAlignment(Qt.AlignCenter)
        flip_lbl.setFixedWidth(140)

        lbl_layout = QHBoxLayout()
        lbl_layout.setAlignment(Qt.AlignCenter)
        lbl_layout.addWidget(rotate_lbl)
        lbl_layout.addWidget(flip_lbl)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(rotate_left_btn)
        btn_layout.addWidget(rotate_right_btn)
        btn_layout.addWidget(QVLine())
        btn_layout.addWidget(flip_left_btn)
        btn_layout.addWidget(flip_top_btn)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(lbl_layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

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
    """Modification tab widget"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.width_lbl = QLabel('width:', self)
        self.width_lbl.setFixedWidth(100)

        self.height_lbl = QLabel('height:', self)
        self.height_lbl.setFixedWidth(100)

        self.width_box = QLineEdit(self)
        self.width_box.textEdited.connect(self.on_width_change)
        self.width_box.setMaximumWidth(100)

        self.height_box = QLineEdit(self)
        self.height_box.textEdited.connect(self.on_height_change)
        self.height_box.setMaximumWidth(100)

        self.unit_lbl = QLabel("px")
        self.unit_lbl.setMaximumWidth(50)

        self.ratio_check = QCheckBox('aspect ratio', self)
        self.ratio_check.stateChanged.connect(self.on_ratio_change)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setFixedWidth(90)
        self.apply_btn.clicked.connect(self.on_apply)

        width_layout = QHBoxLayout()
        width_layout.addWidget(self.width_box)
        width_layout.addWidget(self.height_box)
        width_layout.addWidget(self.unit_lbl)

        apply_layout = QHBoxLayout()
        apply_layout.addWidget(self.apply_btn)
        apply_layout.setAlignment(Qt.AlignRight)

        lbl_layout = QHBoxLayout()
        lbl_layout.setAlignment(Qt.AlignLeft)
        lbl_layout.addWidget(self.width_lbl)
        lbl_layout.addWidget(self.height_lbl)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(lbl_layout)
        main_layout.addLayout(width_layout)
        main_layout.addWidget(self.ratio_check)
        main_layout.addLayout(apply_layout)

        self.setLayout(main_layout)

    def set_boxes(self):
        self.width_box.setText(str(img_original.width))
        self.height_box.setText(str(img_original.height))

    def on_width_change(self, e):
        logger.debug(f"type width {self.width_box.text()}")

        if self.ratio_check.isChecked():
            r_height = _get_ratio_height(img_original.width, img_original.height, int(self.width_box.text()))
            self.height_box.setText(str(r_height))

    def on_height_change(self, e):
        logger.debug(f"type height {self.height_box.text()}")

        if self.ratio_check.isChecked():
            r_width = _get_ratio_width(img_original.width, img_original.height, int(self.height_box.text()))
            self.width_box.setText(str(r_width))

    def on_ratio_change(self, e):
        logger.debug("ratio change")

    def on_apply(self, e):
        logger.debug("apply")

        w, h = int(self.width_box.text()), int(self.height_box.text())
        res_img = img_helper.resize(img_output, w, h)
        self.parent.parent.place_preview_img(res_img)


class AdjustingTab(QWidget):
    """Adjusting tab widget"""

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
        self.contrast_slider.setMinimum(SLIDER_MIN_VAL)
        self.contrast_slider.setMaximum(SLIDER_MAX_VAL)
        self.contrast_slider.sliderReleased.connect(self.on_contrast_slider_released)
        self.contrast_slider.setToolTip(str(SLIDER_MAX_VAL))

        self.brightness_slider = QSlider(Qt.Horizontal, self)
        self.brightness_slider.setMinimum(SLIDER_MIN_VAL)
        self.brightness_slider.setMaximum(SLIDER_MAX_VAL)
        self.brightness_slider.sliderReleased.connect(self.on_brightness_slider_released)
        self.brightness_slider.setToolTip(str(SLIDER_MAX_VAL))

        self.sharpness_slider = QSlider(Qt.Horizontal, self)
        self.sharpness_slider.setMinimum(SLIDER_MIN_VAL)
        self.sharpness_slider.setMaximum(SLIDER_MAX_VAL)
        self.sharpness_slider.sliderReleased.connect(self.on_sharpness_slider_released)
        self.sharpness_slider.setToolTip(str(SLIDER_MAX_VAL))

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(contrast_lbl)
        main_layout.addWidget(self.contrast_slider)

        main_layout.addWidget(brightness_lbl)
        main_layout.addWidget(self.brightness_slider)

        main_layout.addWidget(sharpness_lbl)
        main_layout.addWidget(self.sharpness_slider)

        self.reset_sliders()
        self.setLayout(main_layout)

    def reset_sliders(self):
        self.brightness_slider.setValue(SLIDER_DEF_VAL)
        self.sharpness_slider.setValue(SLIDER_DEF_VAL)
        self.contrast_slider.setValue(SLIDER_DEF_VAL)

    def apply_adjusting(self):
        """
        apply adjusting filters all together without changing initial img
        """

        b = OPERATIONS.ADJUSTING.BRIGHTNESS
        c = OPERATIONS.ADJUSTING.CONTRAST
        s = OPERATIONS.ADJUSTING.SHARPNESS

        logger.debug(f"apply adjusting b:{b}, c:{c}, s:{s}")

        img = img_original
        if b != 0:
            img = img_helper.brightness(img, b)

        if c != 0:
            img = img_helper.contrast(img, c)

        if s != 0:
            img = img_helper.sharpness(img, s)

        self.parent.parent.place_preview_img(img)

    def on_brightness_slider_released(self):
        logger.debug(f"brightness selected value: {self.brightness_slider.value()}")
        self.brightness_slider.setToolTip(str(self.brightness_slider.value()))

        factor = _get_converted_point(SLIDER_MIN_VAL, SLIDER_MAX_VAL, img_helper.BRIGHTNESS_FACTOR_MIN, img_helper.BRIGHTNESS_FACTOR_MAX, self.brightness_slider.value())
        logger.debug(f"brightness factor: {factor}")

        OPERATIONS.ADJUSTING.BRIGHTNESS = factor

        self.apply_adjusting()

    def on_sharpness_slider_released(self):
        logger.debug(self.sharpness_slider.value())
        self.sharpness_slider.setToolTip(str(self.sharpness_slider.value()))

        factor = _get_converted_point(SLIDER_MIN_VAL, SLIDER_MAX_VAL, img_helper.SHARPNESS_FACTOR_MIN,
                                      img_helper.SHARPNESS_FACTOR_MAX, self.sharpness_slider.value())
        logger.debug(f"sharpness factor: {factor}")

        OPERATIONS.ADJUSTING.SHARPNESS = factor

        self.apply_adjusting()

    def on_contrast_slider_released(self):
        logger.debug(self.contrast_slider.value())
        self.contrast_slider.setToolTip(str(self.contrast_slider.value()))

        factor = _get_converted_point(SLIDER_MIN_VAL, SLIDER_MAX_VAL, img_helper.CONTRAST_FACTOR_MIN,
                                      img_helper.CONTRAST_FACTOR_MAX, self.contrast_slider.value())
        logger.debug(f"contrast factor: {factor}")

        OPERATIONS.ADJUSTING.CONTRAST = factor

        self.apply_adjusting()


class FiltersTab(QWidget):
    """Color filters widget"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.add_filter_thumb("none")
        for key, val in color_filter.ColorFilters.filters.items():
            self.add_filter_thumb(key, val)

        self.setLayout(self.main_layout)

    def add_filter_thumb(self, name, title=""):
        logger.debug(f"create lbl thumb for: {name}")

        thumb_lbl = QLabel()
        thumb_lbl.name = name
        thumb_lbl.setStyleSheet("border:2px solid #ccc;")

        if name != "none":
            thumb_lbl.setToolTip(f"Apply <b>{title}</b> filter")
        else:
            thumb_lbl.setToolTip('No filter')

        thumb_lbl.setCursor(Qt.PointingHandCursor)
        thumb_lbl.setFixedSize(THUMB_SIZE, THUMB_SIZE)
        thumb_lbl.mousePressEvent = partial(self.on_filter_select, name)

        self.main_layout.addWidget(thumb_lbl)

    def on_filter_select(self, filter_name, e):
        logger.debug(f"apply color filter: {filter_name}")

        # self.parent.parent.parent.loading()
        if filter_name != "none":
            new_img = img_helper.color_filter(img_original, filter_name)
        else:
            new_img = img_original

        OPERATIONS.COLOR_FILTER = filter_name
        self.toggle_thumbs()

        global img_output
        img_output = new_img
        self.parent.parent.place_preview_img(new_img)
        # self.parent.parent.parent.loading(False)

    def toggle_thumbs(self):
        for thumb in self.findChildren(QLabel):
            color = THUMB_BORDER_COLOR_ACTIVE if thumb.name == OPERATIONS.COLOR_FILTER else THUMB_BORDER_COLOR
            thumb.setStyleSheet(f"border:2px solid {color};")


class MainLayout(QVBoxLayout):
    """Main layout"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.img_lbl = QLabel("Press <b>'Upload'</b> to to start<br>"
                              "<div style='margin: 30px 0'><img src='logo.png' /></div>"
                              "<b>made with</b> <span style='color:red'>&#10084;</span>")
        self.img_lbl.setAlignment(Qt.AlignCenter)

        self.file_name = None

        self.img_size_lbl = None
        self.img_size_lbl = QLabel()
        self.img_size_lbl.setAlignment(Qt.AlignCenter)

        upload_btn = QPushButton("Upload")
        upload_btn.setMinimumWidth(BTN_MIN_WIDTH)
        upload_btn.clicked.connect(self.on_upload)
        upload_btn.setStyleSheet("font-weight:bold;")

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setMinimumWidth(BTN_MIN_WIDTH)
        self.reset_btn.clicked.connect(self.on_reset)
        self.reset_btn.setEnabled(False)
        self.reset_btn.setStyleSheet("font-weight:bold;")

        self.save_btn = QPushButton("Save")
        self.save_btn.setMinimumWidth(BTN_MIN_WIDTH)
        self.save_btn.clicked.connect(self.on_save)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("font-weight:bold;")

        self.addWidget(self.img_lbl)
        self.addWidget(self.img_size_lbl)
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
        new_img_path, _ = QFileDialog.getSaveFileName(self.parent, "QFileDialog.getSaveFileName()",
                                                      f"ez_pz_{self.file_name}",
                                                      "Images (*.png *.jpg)")

        if new_img_path:
            logger.debug(f"save output image to {new_img_path}")
            img_output.save(new_img_path)

    def on_upload(self):
        logger.debug("upload")
        img_path, _ = QFileDialog.getOpenFileName(self.parent, "Open image",
                                                  "/Users",
                                                  "Images (*.png *jpg)")

        if img_path:
            logger.debug(f"open file {img_path}")

            self.file_name = ntpath.basename(img_path)

            pix = QPixmap(img_path)
            self.img_lbl.setPixmap(pix)
            self.img_lbl.setScaledContents(True)
            self.action_tabs.setVisible(True)
            self.action_tabs.adjustment_tab.reset_sliders()

            global img_original
            img_original = ImageQt.fromqpixmap(pix)

            self.update_img_size_lbl()

            global img_output
            img_output = img_original.copy()

            if img_original.width < img_original.height:
                w = THUMB_SIZE
                h = _get_ratio_height(img_original.width, img_original.height, w)
            else:
                h = THUMB_SIZE
                w = _get_ratio_width(img_original.width, img_original.height, h)

            img_filter_thumb = img_helper.resize(img_original, w, h)

            for thumb in self.action_tabs.filters_tab.findChildren(QLabel):
                if thumb.name != "none":
                    img_filter_preview = img_helper.color_filter(img_filter_thumb, thumb.name)
                else:
                    img_filter_preview = img_filter_thumb

                preview_pix = ImageQt.toqpixmap(img_filter_preview)
                thumb.setPixmap(preview_pix)

            self.reset_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            self.action_tabs.modification_tab.set_boxes()

    def update_img_size_lbl(self):
        self.img_size_lbl.setText(f"<span style='font-size:11px'>"
                                  f"image size {img_original.width} × {img_original.height}"
                                  f"</span>")

    def on_reset(self):
        logger.debug("reset all")

        global img_output
        img_output = img_original.copy()

        OPERATIONS.reset()
        self.place_preview_img(img_original)
        self.action_tabs.adjustment_tab.reset_sliders()
        self.action_tabs.modification_tab.set_boxes()


class EasyPzUI(QWidget):
    """Main widget"""

    def __init__(self):
        super().__init__()

        self.main_layout = MainLayout(self)
        self.setLayout(self.main_layout)

        self.setMinimumSize(300, 300)
        self.setMaximumSize(900, 900)
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Easy Peasy - Lemon Squeezy')
        self.center()
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.hide()
        self.show()

    def loading(self, status=True):
        if status:
            self.loading_overlay.resize(self.size())

        self.loading_overlay.setVisible(status)

    def center(self):
        """align window center"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        logger.debug("close")

        if OPERATIONS.has_changes():
            reply = QMessageBox.question(self, "",
                                         "You have unsaved changes<br>Are you sure?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def resizeEvent(self, e):
        if self.loading_overlay.isVisible():
            self.loading_overlay.resize(e.size())


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super(LoadingOverlay, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)

        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.drawLine(self.width() / 8, self.height() / 8, 7 * self.width() / 8, 7 * self.height() / 8)
        painter.drawLine(self.width() / 8, 7 * self.height() / 8, 7 * self.width() / 8, self.height() / 8)
        painter.setPen(QPen(Qt.NoPen))

if __name__ == '__main__':
    fileConfig('logging_config.ini')

    app = QApplication(sys.argv)
    win = EasyPzUI()
    sys.exit(app.exec_())

