# This Python file uses the following encoding: utf-8
import sys
import math
import cv2
import numpy as np
from os.path import expanduser
import time
from time import localtime, strftime

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Slot, QFileInfo, QTimer, Signal, QThread
from PySide6.QtNetwork import QTcpSocket
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from GUI import ui_form_client
from GUI import ui_form_launcher

DEBUG = 1
VIDEOSOURCE = ""

def HMStoDeg(h,m,s):
    return h*360/24+m*6/24+s/240

def DegtoHMS(deg):
    h = math.trunc(deg/(360/24))
    m = math.trunc((deg-360/24*h)/(6/24))
    s = math.trunc((deg-h*360.0/24-m*6/24)/(1/240)*100)/100
    return (h,m,s)

def DMStoDeg(d,m,s):
    return d+m/60+s/3600

def DegtoDMS(deg):
    d = math.trunc(deg)
    m = math.trunc((deg-d)*60)
    s = math.trunc((deg-d-m/60)*3600*100)/100
    return (d,m,s)

class Launcher(QWidget):
    connectAttempt = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = ui_form_launcher.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_Status.setText("")

        self.ui.pushButton_Connect.clicked.connect(self.ConnectClicked)
    def ConnectClicked(self):
        print("Trying to connect...")

        self.connectAttempt.emit()

    def updateStatus(self, msg):
        """Changes status displayed"""
        if type(msg) != str:
            raise TypeError(
                "Error : can only display strings in launcher's status")
        self.ui.label_Status.setText(msg)


class MainClient(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent
        self.SRTconnected = False

        self.ui = ui_form_client.Ui_Widget()
        self.ui.setupUi(self)
        self.hide()

        self.Launcher = Launcher()
        self.Launcher.show()
        self.Launcher.raise_()
        self.Launcher.connectAttempt.connect(self.connectServ)

        self.client_socket = QTcpSocket(self)
        self.client_socket.readyRead.connect(self.receiveMessage)
        self.client_socket.errorOccurred.connect(self.connexionError)
        self.client_socket.disconnected.connect(self.onDisconnected)

        if DEBUG: self.initGUI()
    @Slot()
    def connectServ(self):
        address = self.Launcher.ui.lineEdit_ipAddress.text()
        port = self.Launcher.ui.spinBox_port.value()
        self.Launcher.ui.label_Status.setText("Trying to connect...")
        self.Launcher.ui.pushButton_Connect.setEnabled(0)
        print(f"Attempting to connect to {address} on port {port}")
        self.client_socket.connectToHost(address, port)

    @Slot()
    def connexionError(self):
        self.Launcher.updateStatus("Connexion failed")
        self.Launcher.ui.pushButton_Connect.setEnabled(1)

    # @Slot()
    # def onConnected(self):

    # @Slot()
    def initGUI(self):

        self.Launcher.hide()

        self.CalibFilePath = ''
        self.MeasureFilePath = ''
        self.WorkingDirectoryCalib = ''
        self.WorkingDirectoryMeasure = ''

        self.tracking = 0

        self.measureDuration = 0
        self.timerProgressBar = QTimer()
        self.timerProgressBar.timeout.connect(self.MeasureProgressBarUpdater)
        self.timerIterations = 0

        self.measuring = 0

        self.ui.pushButton_goHome.clicked.connect(self.GoHomeClicked)
        self.ui.pushButton_LaunchMeasurement.clicked.connect(
            self.LaunchMeasurementClicked)
        self.ui.pushButton_Plot.clicked.connect(self.PlotClicked)
        self.ui.pushButton_GoTo.clicked.connect(self.GoToClicked)
        self.ui.pushButton_StopTracking.clicked.connect(
            self.StopTrackingClicked)
        self.ui.pushButton_Connect.clicked.connect(self.ConnectClicked)
        self.ui.pushButton_Disconnect.clicked.connect(self.DisconnectClicked)
        self.ui.pushButton_Untangle.clicked.connect(self.untangleClicked)
        self.ui.pushButton_Standby.clicked.connect(self.standbyClicked)

        self.ui.pushButton_browseCalib.clicked.connect(self.BrowseCalibClicked)
        self.ui.pushButton_browseMeasureFile.clicked.connect(
            self.BrowseMeasureClicked)

        self.ui.pushButton_Plot.clicked.connect(self.PlotClicked)

        self.ui.comboBoxTracking.currentIndexChanged.connect(
            self.TrackingComboBoxChanged)
        self.ui.doubleSpinBox_TrackFirstCoordDecimal.valueChanged.connect(self.TrackFirstCoordDegreeChanged)
        self.ui.doubleSpinBox_TrackFirstCoord_h.valueChanged.connect(self.TrackFirstCoordHMSChanged)
        self.ui.doubleSpinBox_TrackFirstCoord_m.valueChanged.connect(self.TrackFirstCoordHMSChanged)
        self.ui.doubleSpinBox_TrackFirstCoord_s.valueChanged.connect(self.TrackFirstCoordHMSChanged)
        self.ui.doubleSpinBox_TrackSecondCoordDecimal.valueChanged.connect(self.TrackSecondCoordDegreeChanged)
        self.ui.doubleSpinBox_TrackSecondCoord_Deg.valueChanged.connect(self.TrackSecondCoordHMSChanged)
        self.ui.doubleSpinBox_TrackSecondCoord_m.valueChanged.connect(self.TrackSecondCoordHMSChanged)
        self.ui.doubleSpinBox_TrackSecondCoord_s.valueChanged.connect(self.TrackSecondCoordHMSChanged)
        self.ui.tabWidget.setCurrentIndex(0)

        self.ui.pushButton_openCamera.clicked.connect(self.openCameraClicked)
        self.cameraThread = QCameraThread()
        self.cameraThread.closeSignalCameraThread.connect(self.cameraThreadFinished)


        self.show()

    def onDisconnected(self):
        self.addToLog("Disconnected from the server.")
        self.Launcher.updateStatus("Disconnected from the server.")
        self.hide()
        self.Launcher.show()
        self.Launcher.ui.pushButton_Connect.setEnabled(1)
        # TODO self.client_socket disconnect?

    def sendServ(self, message):
        if DEBUG: print(message)
        if (not self.SRTconnected) and message != "connect":
            self.addToLog("No antenna connected. Aborting...")
            return

        if message:
            message = '&' + message  # Adds a "begin" character
            self.client_socket.write(message.encode())

    def receiveMessage(self, verbose=False):

        msg = self.client_socket.readAll().data().decode()
        self.processMsg(msg, verbose)

    def processMsg(self, msg, verbose):

        # Sort messages, sometimes several
        if '&' in msg:
            messages = msg.split('&')[1:]
            if len(messages) > 1:
                print(f"Received concatenated messages : {messages}")
                for message in messages:

                    print(f"processing msg {message}")
                    self.processMsg('&' + message, verbose)

                return

            else:
                msg = messages[0]

        else:
            self.addToLog(
                f"Warning : incorrectly formated message received : {msg}")
            return      # Ignores incorrectly formatted messages

        print(msg)

        if msg == "CONNECTED":
            self.initGUI()
        elif msg == "BUSY":
            self.client_socket.disconnectFromHost()
            self.Launcher.ui.label_Status.setText(
                "Another client is already connected to the server. Try again later...")
        elif msg.startswith('PRINT'):
            msg = msg[6:]  # Gets rid of the "PRINT " statement
            self.addToLog(msg)

        elif '|' in msg:

            status, answer = msg.split('|')
            print(answer)
            if status in ('WARNING', 'ERROR'):
                self.addToLog(status + ' ' + answer)

            if answer == 'connected':
                self.ui.pushButton_Disconnect.setEnabled(1)
                self.SRTconnected = True

            if answer == 'disconnected':
                self.ui.pushButton_Connect.setEnabled(1)
                self.SRTconnected = False

            if answer == 'IDLE':
                self.MovementFinished()

            if "COORDS" in answer:
                print(answer)
                az, alt, ra, dec, long, lat = answer.split(' ')[1:]
                self.setCurrentCoords(ra, dec, long, lat, az, alt)

    def GoHomeClicked(self):
        self.MovementStarted()
        self.sendServ("goHome")

    def LaunchMeasurementClicked(self):
        if self.measuring:
            return
        self.measuring = 1
        self.ui.pushButton_LaunchMeasurement.setEnabled(0)
        self.ui.doubleSpinBox_gain.value()
        self.ui.doubleSpinBox_tsample.value()
        self.ui.doubleSpinBox_Bandwidth.value()
        self.measureDuration = self.ui.doubleSpinBox_duration.value()
        self.ui.doubleSpinBox_centerFreq.value()
        self.ui.spinBox_channels.value()

        self.ui.progressBar_measurement.setValue(0)  # from 0 to 100
        self.timerIterations = 0
        # Launch timer to update progress bar
        self.timerProgressBar.start(1000)

        self.ui.label_MeasureStatus.setText('')  # measuring, saving, etc...
        print("Launch Measurement")
        self.addToLog(f"Started measurement | Center Freq.: {self.ui.doubleSpinBox_centerFreq.value()} MHz, "
                      f"Duration: {self.measureDuration} s, Gain: {self.ui.doubleSpinBox_gain.value()} dB.")
        self.sendServ(f"measure {self.ui.doubleSpinBox_centerFreq.value()} {self.ui.doubleSpinBox_Bandwidth.value()}"
                      f" {self.ui.doubleSpinBox_tsample.value()} {self.ui.doubleSpinBox_duration.value()}"
                      f" {self.ui.doubleSpinBox_gain.value()} {self.ui.spinBox_channels.value()}")

    def MeasurementDone(self):  # link to end of measurement thread!!
        self.measuring = 0
        self.ui.pushButton_LaunchMeasurement.setEnabled(1)
        self.ui.progressBar_measurement.setValue(0)
        self.ui.label_MeasureStatus.setText("Done.")

    def PlotClicked(self):
        print("Plot Measurement")

    def addToLog(self, strInput):
        self.ui.textBrowser_log.append(
            f"{strftime('%Y-%m-%d %H:%M:%S', localtime())}: " + strInput)

    def GoToClicked(self):
        # valeurs:
        self.MovementStarted()

        if self.ui.checkBox_Tracking.isChecked():
            self.tracking = 1
            self.ui.pushButton_StopTracking.setEnabled(1)
            self.ui.doubleSpinBox_TrackFirstCoordDecimal.setEnabled(0)
            self.ui.doubleSpinBox_TrackFirstCoord_h.setEnabled(0)
            self.ui.doubleSpinBox_TrackFirstCoord_m.setEnabled(0)
            self.ui.doubleSpinBox_TrackFirstCoord_s.setEnabled(0)
            self.ui.doubleSpinBox_TrackSecondCoordDecimal.setEnabled(0)
            self.ui.doubleSpinBox_TrackSecondCoord_Deg.setEnabled(0)
            self.ui.doubleSpinBox_TrackSecondCoord_m.setEnabled(0)
            self.ui.doubleSpinBox_TrackSecondCoord_s.setEnabled(0)
            self.ui.comboBoxTracking.setEnabled(0)
            self.ui.checkBox_Tracking.setEnabled(0)

            # valeurs
        else:
            self.tracking = 0
            self.ui.pushButton_StopTracking.setEnabled(0)
            #self.ui.doubleSpinBox_TrackFirstCoordDecimal.setEnabled(0)
            #self.ui.doubleSpinBox_TrackSecondCoordDecimal.setEnabled(0)

            # Do movement

            #self.ui.doubleSpinBox_TrackFirstCoord.setEnabled(1)
            #self.ui.doubleSpinBox_TrackSecondCoord.setEnabled(1)
        message = ''
        if self.ui.comboBoxTracking.currentIndex() == 2 and self.ui.checkBox_Tracking.isChecked():  # should not happen
            message = 'point'
        else:
            if self.ui.checkBox_Tracking.isChecked():
                message = 'track'
            else:
                message = 'point'

            if self.ui.comboBoxTracking.currentIndex() == 0:  # Ra Dec
                message += 'RA'

            if self.ui.comboBoxTracking.currentIndex() == 1:  # Galactic
                message += 'Gal'

            if self.ui.comboBoxTracking.currentIndex() == 2:  # Az Alt
                message += "AzAlt"

            message += f" {self.ui.doubleSpinBox_TrackFirstCoordDecimal.value()} {self.ui.doubleSpinBox_TrackSecondCoordDecimal.value()}"

        self.sendServ(message)

    def StopTrackingClicked(self):
        self.tracking = 0
        self.ui.pushButton_StopTracking.setEnabled(0)
        self.ui.doubleSpinBox_TrackFirstCoordDecimal.setEnabled(1)
        self.ui.doubleSpinBox_TrackFirstCoord_h.setEnabled(1)
        self.ui.doubleSpinBox_TrackFirstCoord_m.setEnabled(1)
        self.ui.doubleSpinBox_TrackFirstCoord_s.setEnabled(1)
        self.ui.doubleSpinBox_TrackSecondCoordDecimal.setEnabled(1)
        self.ui.doubleSpinBox_TrackSecondCoord_Deg.setEnabled(1)
        self.ui.doubleSpinBox_TrackSecondCoord_m.setEnabled(1)
        self.ui.doubleSpinBox_TrackSecondCoord_s.setEnabled(1)
        self.ui.comboBoxTracking.setEnabled(1)
        self.ui.checkBox_Tracking.setEnabled(1)

        self.ui.pushButton_GoTo.setEnabled(1)
        self.ui.checkBox_Tracking.setEnabled(1)
        print("Stop Tracking")

    def MovementFinished(self):
        self.ui.pushButton_Standby.setEnabled(1)
        self.ui.pushButton_Untangle.setEnabled(1)
        self.ui.pushButton_goHome.setEnabled(1)
        self.ui.pushButton_GoTo.setEnabled(1)
        self.ui.checkBox_Tracking.setEnabled(1)

    def MovementStarted(self):
        self.ui.pushButton_Standby.setEnabled(0)
        self.ui.pushButton_Untangle.setEnabled(0)
        self.ui.pushButton_goHome.setEnabled(0)
        self.ui.pushButton_GoTo.setEnabled(0)
        self.ui.checkBox_Tracking.setEnabled(0)
        pass

    def ConnectClicked(self):
        self.sendServ("connect")
        self.ui.pushButton_Connect.setEnabled(0)
        self.ui.pushButton_Disconnect.setEnabled(1)

    def DisconnectClicked(self):
        self.ui.pushButton_Connect.setEnabled(1)
        self.ui.pushButton_Disconnect.setEnabled(0)
        self.sendServ("disconnect")
        print("Disconnect")

    def TrackFirstCoordDegreeChanged(self,val):
        (h,m,s) = DegtoHMS(val)
        self.ui.doubleSpinBox_TrackFirstCoord_h.blockSignals(1)
        self.ui.doubleSpinBox_TrackFirstCoord_m.blockSignals(1)
        self.ui.doubleSpinBox_TrackFirstCoord_s.blockSignals(1)

        self.ui.doubleSpinBox_TrackFirstCoord_h.setValue(h)
        self.ui.doubleSpinBox_TrackFirstCoord_m.setValue(m)
        self.ui.doubleSpinBox_TrackFirstCoord_s.setValue(s)

        self.ui.doubleSpinBox_TrackFirstCoord_h.blockSignals(0)
        self.ui.doubleSpinBox_TrackFirstCoord_m.blockSignals(0)
        self.ui.doubleSpinBox_TrackFirstCoord_s.blockSignals(0)
    def TrackFirstCoordHMSChanged(self, val):
        self.ui.doubleSpinBox_TrackFirstCoordDecimal.blockSignals(1)
        self.ui.doubleSpinBox_TrackFirstCoordDecimal.setValue(HMStoDeg(self.ui.doubleSpinBox_TrackFirstCoord_h.value(),
                                                                       self.ui.doubleSpinBox_TrackFirstCoord_m.value(),
                                                                       self.ui.doubleSpinBox_TrackFirstCoord_s.value()))
        self.ui.doubleSpinBox_TrackFirstCoordDecimal.blockSignals(0)

    def TrackSecondCoordDegreeChanged(self,val):
        (h,m,s) = DegtoDMS(val)
        self.ui.doubleSpinBox_TrackSecondCoord_Deg.blockSignals(1)
        self.ui.doubleSpinBox_TrackSecondCoord_m.blockSignals(1)
        self.ui.doubleSpinBox_TrackSecondCoord_s.blockSignals(1)

        self.ui.doubleSpinBox_TrackSecondCoord_Deg.setValue(h)
        self.ui.doubleSpinBox_TrackSecondCoord_m.setValue(m)
        self.ui.doubleSpinBox_TrackSecondCoord_s.setValue(s)

        self.ui.doubleSpinBox_TrackSecondCoord_Deg.blockSignals(0)
        self.ui.doubleSpinBox_TrackSecondCoord_m.blockSignals(0)
        self.ui.doubleSpinBox_TrackSecondCoord_s.blockSignals(0)
    def TrackSecondCoordHMSChanged(self, val):
        self.ui.doubleSpinBox_TrackSecondCoordDecimal.blockSignals(1)
        self.ui.doubleSpinBox_TrackSecondCoordDecimal.setValue(DMStoDeg(self.ui.doubleSpinBox_TrackSecondCoord_Deg.value(),
                                                                       self.ui.doubleSpinBox_TrackSecondCoord_m.value(),
                                                                       self.ui.doubleSpinBox_TrackSecondCoord_s.value()))
        self.ui.doubleSpinBox_TrackSecondCoordDecimal.blockSignals(0)
    def TrackingComboBoxChanged(self, index):
        if index == 0:
            self.ui.LabelTrackingFirstCoord.setText("Ra")
            self.ui.LabelTrackingSecondCoord.setText("Dec")
            self.ui.checkBox_Tracking.setEnabled(1)
        if index == 1:
            self.ui.LabelTrackingFirstCoord.setText("l")
            self.ui.LabelTrackingSecondCoord.setText("b")
            self.ui.checkBox_Tracking.setEnabled(1)
        if index == 2:
            self.ui.LabelTrackingFirstCoord.setText("Az")
            self.ui.LabelTrackingSecondCoord.setText("Alt")
            self.ui.checkBox_Tracking.setChecked(0)
            self.ui.checkBox_Tracking.setEnabled(0)

    def BrowseCalibClicked(self):
        if self.WorkingDirectoryCalib:
            fileName = QFileDialog.getOpenFileName(self,
                                                   "Open Data file", self.WorkingDirectoryCalib, "Data Files (*.dat)")[
                0]
        else:
            fileName = QFileDialog.getOpenFileName(self,
                                                   "Open Data file", expanduser("~"), "Data Files (*.dat)")[0]
        print(fileName)
        print(QFileInfo(fileName).absoluteDir().absolutePath())
        self.WorkingDirectoryCalib = QFileInfo(
            fileName).absoluteDir().absolutePath()
        if fileName:
            self.CalibFilePath = fileName
            self.ui.lineEdit_CalibFile.setText(self.CalibFilePath)

    def BrowseMeasureClicked(self):
        if self.WorkingDirectoryMeasure:
            fileName = QFileDialog.getOpenFileName(self,
                                                   "Open Data file", self.WorkingDirectoryMeasure,
                                                   "Data Files (*.dat)")[
                0]
        else:
            fileName = QFileDialog.getOpenFileName(self,
                                                   "Open Data file", expanduser("~"), "Data Files (*.dat)")[0]
        print(fileName)
        print(QFileInfo(fileName).absoluteDir().absolutePath())
        self.WorkingDirectoryMeasure = QFileInfo(
            fileName).absoluteDir().absolutePath()
        if fileName:
            self.MeasureFilePath = fileName
            self.ui.lineEdit_MeasureFile.setText(self.MeasureFilePath)

    def MeasureProgressBarUpdater(self):  # ProgressBar updater
        self.timerIterations += 1
        value = self.timerIterations / self.measureDuration * 100
        if 100 >= value >= 0:
            self.ui.progressBar_measurement.setValue(int(value))
            self.ui.label_MeasureStatus.setText("Measuring...")

        if value >= 100:
            self.timerProgressBar.stop()
            self.ui.progressBar_measurement.setValue(100)
            self.timerIterations = 0

            self.MeasurementDone()  # %TODO Temporary! link to thread end

    def untangleClicked(self):
        pass

    def standbyClicked(self):
        pass

    def setCurrentCoords(self, *args):

        args = [float(elt) for elt in args]

        Ra, Dec, GalL, GalB, Az, Alt = args

        self.ui.RaLabel.setText(f"{Ra:.2f}")
        self.ui.DecLabel.setText(f"{Dec:.2f}")
        self.ui.label_GalL.setText(f"{GalL:.2f}")
        self.ui.label_GalB.setText(f"{GalB:.2f}")
        self.ui.AltLabel.setText(f"{Alt:.2f}")
        self.ui.AzLabel.setText(f"{Az:.2f}")

    def openCameraClicked(self):
        print(self.cameraThread.on)
        if not self.cameraThread.on:
            self.cameraThread = QCameraThread()
            self.cameraThread.closeSignalCameraThread.connect(self.cameraThreadFinished)
            self.cameraThread.turnOn()
            self.cameraThread.start()
            self.ui.pushButton_openCamera.setText("Close Camera")
        else:
            self.cameraThread.turnOff()
            while self.cameraThread.isRunning():
                pass
            #self.cameraThread.exit()
            self.cameraThread = QCameraThread()
            self.ui.pushButton_openCamera.setText("Open Camera")

    def cameraThreadFinished(self):
        print("triggered")
        self.ui.pushButton_openCamera.setText("Open Camera")
        self.cameraThread = QCameraThread()

class QCameraThread(QThread):

    closeSignalCameraThread = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.on = False

        self.display_image_widget = DisplayImageWidget()
        self.display_image_widget.closeSignal.connect(self.CustomClose)

    def turnOff(self):
        self.on = False
        if VIDEOSOURCE == '':
            return
        cv2.destroyWindow("Camera")

    def turnOn(self):
        self.on = True
        self.display_image_widget.show()

    def CustomClose(self):
        print("customclosed")
        self.closeSignalCameraThread.emit()
        self.exit()

    def run(self):
        if VIDEOSOURCE == '':
            return

        self.cap = cv2.VideoCapture(VIDEOSOURCE)
        self.FRAME_WIDTH = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.FRAME_HEIGHT = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('Frame Size: ', self.FRAME_WIDTH, 'x', self.FRAME_HEIGHT)

        self.ret = False
        self.frame = None
        if self.cap.isOpened():
            self.ret, self.frame = self.cap.read()

        while self.ret and self.on:
            #print("loading")
            self.ret, self.frame = self.cap.read()
            if self.frame is not None: self.display_image_widget.show_image(self.frame)
            time.sleep(0.05)
            #cv2.imshow('Camera', self.frame)


class DisplayImageWidget(QWidget):

    closeSignal = Signal()
    def __init__(self, parent=None):
        super(DisplayImageWidget, self).__init__(parent)

        self.image_frame = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

    def closeEvent(self, event):
        print("closed")
        self.closeSignal.emit()

    @Slot()
    def show_image(self, cap):
        scale_percent = 60  # percent of original size
        width = int(cap.shape[1] * scale_percent / 100)
        height = int(cap.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(cap, dim, interpolation=cv2.INTER_AREA)

        self.image_frame.setPixmap(QPixmap.fromImage(QImage(resized.data, resized.shape[1],
                                                            resized.shape[0], QImage.Format_RGB888).rgbSwapped()))

if __name__ == "__main__":
    sys.argv[0] = 'Astro Antenna'
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Astro Antenna")

    widgetMainClient = MainClient()
    # widgetMainClient.show()
    sys.exit(app.exec())
