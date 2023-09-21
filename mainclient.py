# This Python file uses the following encoding: utf-8
import sys
from os.path import expanduser
from time import time, localtime, strftime

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import Slot, QFileInfo, QTimer, Signal, QThread
from PySide6.QtNetwork import QTcpSocket
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from GUI import ui_form_client
from GUI import ui_form_launcher


def say_hello():
    print("Button clicked, Hello!")


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
        """Cahnges status displayed"""
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

        self.ui.tabWidget.setCurrentIndex(0)

        self.show()

    def onDisconnected(self):
        self.addToLog("Disconnected from the server.")
        self.Launcher.updateStatus("Disconnected from the server.")
        self.hide()
        self.Launcher.show()
        self.Launcher.ui.pushButton_Connect.setEnabled(1)
        # TODO self.client_socket disconnect?

    def sendServ(self, message):

        if (not self.SRTconnected) and message != "connect":
            self.addToLog("No antenna connected. Aborting...")
            return

        if message:
            self.client_socket.write(message.encode())

    def receiveMessage(self, verbose=False):

        msg = self.client_socket.readAll().data().decode()
        self.processMsg(msg, verbose)

    def processMsg(self, msg, verbose):

        # Sort messages, sometimes several
        if '&' in msg:
            messages = msg.split('&')[1:]
            if len(messages) > 1:
                for message in messages:
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
            self.ui.doubleSpinBox_TrackFirstCoord.setEnabled(0)
            self.ui.doubleSpinBox_TrackSecondCoord.setEnabled(0)
            self.ui.checkBox_Tracking.setEnabled(0)

            # valeurs
        else:
            self.tracking = 0
            self.ui.pushButton_StopTracking.setEnabled(0)
            self.ui.doubleSpinBox_TrackFirstCoord.setEnabled(0)
            self.ui.doubleSpinBox_TrackSecondCoord.setEnabled(0)

            # Do movement

            self.ui.doubleSpinBox_TrackFirstCoord.setEnabled(1)
            self.ui.doubleSpinBox_TrackSecondCoord.setEnabled(1)
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
                pass

            message += f" {self.ui.doubleSpinBox_TrackFirstCoord.value()} {self.ui.doubleSpinBox_TrackSecondCoord.value()}"

        self.sendServ(message)

    def StopTrackingClicked(self):
        self.tracking = 0
        self.ui.pushButton_StopTracking.setEnabled(0)
        self.ui.doubleSpinBox_TrackFirstCoord.setEnabled(1)
        self.ui.doubleSpinBox_TrackSecondCoord.setEnabled(1)

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

    def TrackingComboBoxChanged(self, index):
        if index == 0:
            self.ui.LabelTrackingFirstCoord.setText("Ra")
            self.ui.LabelTrackingSecondCoord.setText("Dec")
        if index == 1:
            self.ui.LabelTrackingFirstCoord.setText("l")
            self.ui.LabelTrackingSecondCoord.setText("b")
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


if __name__ == "__main__":
    sys.argv[0] = 'Astro Antenna'
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Astro Antenna")

    widgetMainClient = MainClient()
    # widgetMainClient.show()
    sys.exit(app.exec())
