"""
A crappy GUI for intelligent scissors/livewire with 
# Left click to set seed
# Right click to finish
# Mid click to export image file
"""

from __future__ import division
import time
import cv2
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from threading import Thread

from PyQt5.QtGui import QPixmap, QPainter

from floodFill import qtpixmap_to_cvimg
from pylivewire_master.livewire import Livewire
from utils import extract_object, bgraImg_to_qtImg


class ImageWin(QtWidgets.QDialog):
    def __init__(self, img: QPixmap):
        super(ImageWin, self).__init__()
        self.setupUi(img)
        self.active = False
        self.seed_enabled = True
        self.seed = None
        self.path_map = {}
        self.path = []
        self.cropped_image = None  # save the cropped image for returning
        
    def setupUi(self, img):
        self.hbox = QtWidgets.QVBoxLayout(self)

        self.image = img
        # self.cv2_image = cv2.imread(str(self.image_path))
        self.cv2_image = qtpixmap_to_cvimg(img)
        self.lw = Livewire(self.cv2_image)
        self.w, self.h = self.image.width(), self.image.height()
        
        self.canvas = QtWidgets.QLabel(self)  #
        self.canvas.setMouseTracking(True)
        self.canvas.setPixmap(self.image)
        
        self.status_bar = QtWidgets.QStatusBar(self)
        self.status_bar.showMessage('Left click to set a seed')

        # add a button to finish the path
        self.finish_button = QtWidgets.QPushButton('Finish', self)
        self.finish_button.clicked.connect(self.finishPathAndExport)

        self.hbox.addWidget(self.canvas)
        self.hbox.addWidget(self.status_bar)
        self.hbox.addWidget(self.finish_button)
        self.setLayout(self.hbox)

    # Export bitmap and close window
    def finishPathAndExport(self):
        if self.path is not None:
            path = [(col, row) for row, col in self.path]  # convert to (x, y) format
            mask = np.zeros(self.cv2_image.shape[:2], np.uint8)
            cv2.fillPoly(mask, np.int32([path]), 255)  # fill the path with white
            # cv2.imshow('mask', mask)
            # cv2.waitKey(0)
            self.cv2_image[mask == 0] = 255  # set background to white

            # Find bounding rectangle of path
            min_x = min(p[1] for p in self.path)
            max_x = max(p[1] for p in self.path)
            min_y = min(p[0] for p in self.path)
            max_y = max(p[0] for p in self.path)

            # extract selected img with transparency and Crop image to bounding rectangle
            extracted_img_bgra = extract_object(self.cv2_image, mask)
            self.cropped_image = QPixmap(bgraImg_to_qtImg(extracted_img_bgra))

            # Save and return cropped image
            # filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save image audio to', '',
            #                                                     '*.jpg\n*.bmp\n*.png')
            self.cropped_image.save('./segmented_output/freeCut_result.jpg', quality=100)
        self.close()
    
    def mousePressEvent(self, event):            
        if self.seed_enabled:
            pos = event.pos()
            x, y = pos.x()-self.canvas.x(), pos.y()-self.canvas.y()
            
            if x < 0:
                x = 0
            if x >= self.w:
                x = self.w - 1
            if y < 0:
                y = 0
            if y >= self.h:
                y = self.h - 1

            # Get the mouse cursor position
            p = y, x
            seed = self.seed
            
            # Export bitmap and close window
            if event.buttons() == QtCore.Qt.MidButton:
                self.finishPathAndExport()
            
            else:
                self.seed = p
                
                if self.path_map:
                    while p != seed:
                        p = self.path_map[p]
                        self.path.append(p)
                
                # Calculate path map
                if event.buttons() == QtCore.Qt.LeftButton:
                    Thread(target=self._cal_path_matrix).start()
                    Thread(target=self._update_path_map_progress).start()
                
                # Finish current task and reset
                elif event.buttons() == QtCore.Qt.RightButton:
                    self.path_map = {}
                    self.status_bar.showMessage('Left click to set a seed')
                    self.active = False
    
    def mouseMoveEvent(self, event):
        if self.active and event.buttons() == QtCore.Qt.NoButton:
            pos = event.pos()
            x, y = pos.x()-self.canvas.x(), pos.y()-self.canvas.y()

            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                pass
            else:
                # Draw livewire
                p = y, x
                path = []
                while p != self.seed:
                    p = self.path_map[p]
                    path.append(p)
                
                image = self.image.copy()
                draw = QPainter()
                draw.begin(image)
                draw.setPen(QtCore.Qt.blue)
                for p in path:
                    draw.drawPoint(p[1], p[0])
                if self.path:
                    draw.setPen(QtCore.Qt.green)
                    for p in self.path:
                        draw.drawPoint(p[1], p[0])
                draw.end()
                self.canvas.setPixmap(image)
    
    def _cal_path_matrix(self):
        self.seed_enabled = False
        self.active = False
        self.status_bar.showMessage('Calculating path map...')
        path_matrix = self.lw.get_path_matrix(self.seed)
        self.status_bar.showMessage(r'Left: new seed / Right: finish')
        self.seed_enabled = True
        self.active = True
        
        self.path_map = path_matrix
    
    def _update_path_map_progress(self):
        while not self.seed_enabled:
            time.sleep(0.1)
            message = 'Calculating path map... {:.1f}%'.format(self.lw.n_processed/self.lw.n_pixs*100.0)
            self.status_bar.showMessage(message)
        self.status_bar.showMessage(r'Left: new seed / Right: finish')
