#!/usr/bin/python3.6
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GUI.ui_NewMosaic import Ui_Dialog


class NewMosaicDialog(QDialog):
    image_size = None
    file_dialog = None
    _pixmap = None

    # signal
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        # setup ui
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # config
        self.setModal(True)
        self.setWindowTitle(self.tr("New Mosaic"))
        self._pixmap = QPixmap()
        self.ui.lb_Image.installEventFilter(self)
        # self.ui.scrollArea.setMinimumWidth(self.ui.verticalLayout_2.totalMinimumSize().width())
        # connection
        self.ui.pb_ok.clicked.connect(self.on_ok_button_clicked)
        self.ui.pb_cancel.clicked.connect(self.on_cancel_button_clicked)
        self.ui.sb_im_h.editingFinished.connect(self.on_number_of_image_h_changed)
        self.ui.sb_im_v.editingFinished.connect(self.on_number_of_image_v_changed)
        self.ui.pb_browse.clicked.connect(self.on_browse_button_clicked)
        self.ui.le_im_path.textChanged.connect(self.on_text_field_path_set)
        self.ui.sb_tile_height.editingFinished.connect(self.on_height_of_tile_changed)
        self.ui.sb_tile_width.editingFinished.connect(self.on_width_of_tile_changed)
        self.ui.cb_grayscale.clicked.connect(self.on_gray_scale_cb_clicked)
        self.ui.le_im_path.textChanged.connect(self.on_number_of_image_v_changed)

    # event filter for pixmap preview
    def eventFilter(self, widget, event):
        if event.type() == QEvent.Resize and widget is self.ui.lb_Image and self._pixmap.isNull() is False:
            self.ui.lb_Image.setPixmap(self._pixmap.scaled(
                self.ui.lb_Image.width(), self.ui.lb_Image.height(),
                Qt.KeepAspectRatio))
            return True
        return QDialog.eventFilter(self, widget, event)

    def on_ok_button_clicked(self):
        self.finished.emit()

    def on_cancel_button_clicked(self):
        self.close()

    def on_browse_button_clicked(self):
        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        type_filters = list()
        type_filters.append("Image files (*.png *.gif *.jpg *.jpeg *.JPG *.JPEG *.PNG)")
        self.file_dialog.setNameFilters(type_filters)
        self.file_dialog.fileSelected[str].connect(self.ui.le_im_path.setText)
        self.file_dialog.setModal(True)
        self.file_dialog.show()

    def on_text_field_path_set(self):
        image_path = self.ui.le_im_path.text()
        pixmap = QPixmap(image_path)
        if pixmap.isNull() is False:
            self.ui.groupBox_Tiles.setEnabled(True)
            self.image_size = pixmap.size()
            self.ui.pb_ok.setEnabled(True)
            self._pixmap = pixmap
            # if the image is wanted in gray scale then adapt the preview
            if self.ui.cb_grayscale.isChecked():
                image = self._pixmap.toImage()
                image = image.convertToFormat(QImage.Format_Grayscale8)
                self._pixmap = QPixmap(image)
            self.ui.lb_Image.setPixmap(self._pixmap.scaled(
                self.ui.lb_Image.width(), self.ui.lb_Image.height(),
                Qt.KeepAspectRatio))
        else:
            self.ui.groupBox_Tiles.setEnabled(False)
            self.ui.pb_ok.setEnabled(False)
            self.ui.lb_Image.setPixmap(pixmap)

    def on_number_of_image_h_changed(self):
        if self.ui.cb_keep_aspect_ratio.isChecked() is True:
            num_im_v = int(self.ui.sb_im_h.value() / int(self.image_size.width() / 3) * int(self.image_size.height() / 2))
            # if we go above the limit of the spinbox
            if num_im_v > self.ui.sb_im_v.maximum():
                self.ui.sb_im_v.setValue(self.ui.sb_im_v.maximum())
            # if we go under the limit of the spinbox
            elif num_im_v <= self.ui.sb_im_v.minimum():
                self.ui.sb_im_v.setValue(self.ui.sb_im_v.minimum())
            # else just ensure size synchronisation
            elif abs(num_im_v - self.ui.sb_im_v.value()) > 1:
                self.ui.cb_keep_aspect_ratio.setChecked(False)
                self.ui.sb_im_v.setValue(num_im_v)
                self.ui.cb_keep_aspect_ratio.setChecked(True)

    def on_number_of_image_v_changed(self):
        if self.ui.cb_keep_aspect_ratio.isChecked() is True:
            num_im_h = int(self.ui.sb_im_v.value() / int(self.image_size.height() / 2) * int(self.image_size.width() / 3))
            # if we go above the limit of the spinbox
            if num_im_h > self.ui.sb_im_h.maximum():
                self.ui.sb_im_h.setValue(self.ui.sb_im_h.maximum())
            # if we go under the limit of the spinbox
            elif num_im_h <= self.ui.sb_im_h.minimum():
                self.ui.sb_im_h.setValue(self.ui.sb_im_h.minimum())
            # else just ensure size synchronisation
            elif abs(num_im_h - self.ui.sb_im_h.value()) > 1:
                self.ui.cb_keep_aspect_ratio.setChecked(False)
                self.ui.sb_im_h.setValue(num_im_h)
                self.ui.cb_keep_aspect_ratio.setChecked(True)

    def on_height_of_tile_changed(self):
        tile_height = (self.ui.sb_tile_height.value() // 2) * 2
        tile_width = tile_height / 2 * 3
        self.ui.sb_tile_height.setValue(tile_height)
        self.ui.sb_tile_width.setValue(tile_width)

    def on_width_of_tile_changed(self):
        tile_width = (self.ui.sb_tile_width.value() // 3) * 3
        tile_height = tile_width / 3 * 2
        self.ui.sb_tile_height.setValue(tile_height)
        self.ui.sb_tile_width.setValue(tile_width)

    def on_gray_scale_cb_clicked(self):
        if self.ui.cb_grayscale.isChecked():
            image = self._pixmap.toImage()
            image = image.convertToFormat(QImage.Format_Grayscale8)
            self._pixmap = QPixmap(image)
        else:
            image_path = self.ui.le_im_path.text()
            self._pixmap = QPixmap(image_path)
        self.ui.lb_Image.setPixmap(self._pixmap.scaled(
            self.ui.lb_Image.width(), self.ui.lb_Image.height(),
            Qt.KeepAspectRatio))
