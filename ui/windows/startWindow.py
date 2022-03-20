import os

import cv2 as cv
import sys
import os.path as path
# import matplotlib.pyplot as plt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QLineEdit
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt

from threading import Thread
from core.roi.roi import ROI
from core.contour.contour import Contour


class MainWindow:
    imagePath = ""
    pictureName = "test"
    savePath = "..\\resource\\image"
    defaultPic = ""

    def __init__(self):
        qfile = QFile("..\\resource\\mainWindow.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)
        self.ui.uploadButton.clicked.connect(self.showSelectFileDialog)
        self.ui.startButton.clicked.connect(self.startScan)
        self.ui.exitButton.clicked.connect(self.exit)
        self.ui.showButton.clicked.connect(self.showResult)
        self.ui.displayLabel.setStyleSheet('''background: rgba(177, 177, 177, 0.8);
            font-family: YouYuan;
            font-size: 12pt;
            color: white;
        ''')
        self.ui.displayLabel.setAlignment(Qt.AlignCenter)
        self.ui.displayLabel.setText("No picture")
        global pictureName
        self.ui.pnLineEdit.setText("test")
        global savePath
        self.ui.spLineEdit.setText("E:\\Code\\thesis_design\\PalmScan\\ui\\resource\\image")
        #for test
        global imagePath
        imagePath = 'E:\\Code\\thesis_design\\PalmScan\\image\\wxf.jpg'
        pixmap = QPixmap(imagePath).scaled(self.ui.size(), aspectMode=Qt.KeepAspectRatio)

        self.ui.displayLabel.setPixmap(pixmap)
        self.ui.displayLabel.repaint()

    def startScan(self):
        userName = self.ui.pnLineEdit.text()
        if not userName:
            userName = "test"
        toSavePath = self.ui.spLineEdit.text()
        if not toSavePath:
            toSavePath = "E:\\Code\\thesis_design\\PalmScan\\ui\\resource\\image"
        global imagePath

        try:
            c = Contour(userName, imagePath, toSavePath)
            ct, skin, contour, contour_skin = c.drawContour()
            r = ROI(contour, skin, contour_skin)
            r.roi(ct, userName, toSavePath, contour_skin)
            r.roi_main(ct)
            r.roi_thenar()
            r.roi_small_thenar()
            r.roi_5()
            r.roi_7()

        except:
            QMessageBox().warning(self.ui, "warnning", "No image selected!")

    def showResult(self):
        toSavePath = self.ui.spLineEdit.text()
        if not toSavePath:
            global savePath
            toSavePath = savePath
        imgs = os.listdir(toSavePath)
        imgsCount = len(imgs)

        for imName in imgs:
            self.showPic(toSavePath + "//" + imName)
            # thread = Thread(target=self.showPic, args=toSavePath + imName)
            # thread.start()

    def exit(self):
        sys.exit(self)

    def showSelectFileDialog(self):
        fileName = QFileDialog.getOpenFileName(None, "Input File", "//",
                                               "JPG, PNG (*.jpg *.png);;All files (*.*)")
        if fileName[0]:
            try:
                global imagePath
                imagePath = fileName[0]
                global pictureName
                pictureName = path.basename(imagePath).split('.')[0]
                self.ui.pnLineEdit.setText(pictureName)
                pixmap = QPixmap(fileName[0]).scaled(self.ui.displayLabel.size(), aspectMode=Qt.KeepAspectRatio)
                self.ui.displayLabel.setPixmap(pixmap)
                # self.ui.displayLabel.repaint()

            except:
                QMessageBox.warning("open file failed, please check the file type!")

    def showPic(self, path):
        # global imagePath
        # path = imagePath
        image = cv.imread(path)
        h, w = image.shape[:2]
        image = cv.resize(image, (0, 0), fx=0.5, fy=0.5)
        # plt.imshow(image)
        # plt.show()
        # cv.imwrite('D:\\Pictures\\images_gray.jpg', image)
        self.cv_show("result", image)

    def cv_show(self, name, img):
        cv.imshow(name, img)

        cv.waitKey(0)

        cv.destroyAllWindows()


app = QApplication([])
mainWindow = MainWindow()
mainWindow.ui.show()
app.exec_()
