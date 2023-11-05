from GS_interface.lib.library_GS import *
import sys
from os.path import expanduser
from time import time, localtime, strftime
import io
from GUI.ui_form_server import Ui_MainWindow
import socket
from PySide6.QtNetwork import QTcpServer, QTcpSocket, QHostAddress, QNetworkInterface, QAbstractSocket
from PySide6.QtCore import Slot, QFileInfo, QTimer, Signal, QThread, QObject
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow
import os
import time

sys.path.append("../")

"""
THIS SCRIPT RUNS THE SERVER IN CHARGE OF COMMUNICATING WITH THE APM

Format of exchanged messages : 
    Client -> Server : &{cmd} {*args, separated by spaces}
    Server -> Client : &{Status}|{feedback}
    
    with Status in (PRINT, OK, WARNING, ERROR)     
    
    Notice hence forbidden characters & and | in the body of exchanged messages
"""

POS_LOGGING_RATE = 1


class sigEmettor(QObject):
    """QObject that handles sending a signal from a non-Q thread.
    Used by StdoutRedirector to pass the Server a print statement
    to send to the client"""

    printMsg = Signal(str, bool)  # Signal emitted when sth is printed

    def __init__(self, parent=None):
        super().__init__(parent)


class StdoutRedirector(io.StringIO):
    """Handles the redirection of print statements to both the server-side
    console and to the client via messages with PRINT status"""

    def __init__(self, target, parent=None):
        super().__init__()
        self.target = target
        self.emettor = sigEmettor()

    def write(self, message):
        self.target.write(message)
        self.target.flush()
        if message == '\n':
            return

        message = "PRINT|" + str(message)
        self.emettor.printMsg.emit(message, False)  # Set verbose to False


class SRTThread(QThread):
    """Thread that handles communication with SRT object, including tracking"""

    endMotion = Signal(str, str)

    send2socket = Signal(str)

    def __init__(self, msg: str = '', parent=None):
        super().__init__(parent)

        self.measuring = 0
        self.on = True
        self.posLoggingOn = True
        self.pending = False
        self.timeLastPosCheck = time.time()

        self.SRT = Srt("/dev/ttyUSB0", 115200, 1)
        self.msg = msg

    def tracking(self):
        return self.SRT.tracking

    def sendClient(self, msgSend):

        self.send2socket.emit(msgSend)

    def sendOK(self, msg):

        msg = "OK|" + msg
        self.sendClient(msg)

    def sendWarning(self, msg):

        msg = "WARNING|" + msg
        self.sendClient(msg)

    def sendError(self, msg):

        msg = "ERROR|" + msg
        self.sendClient(msg)

    def receiveCommand(self, msg):
        self.msg = str

    def pausePositionLogging(self):
        self.posLoggingOn = False

    def unpausePositionLogging(self):
        self.posLoggingOn = True

    def sendPos(self):
        az, alt = self.SRT.getAzAlt()
        ra, dec = self.SRT.getPos()
        long, lat = self.SRT.getGal()

        if (az == -1) or (alt == -1):
            self.sendError(
                "Error while trying to get current coordinates. Hardware may be damaged. Please report this"
                " event to the person in charge ASAP")

        msgReturn = f"COORDS {az} {alt} {ra} {dec} {long} {lat}"
        self.sendOK(msgReturn)

    def run(self):

        while self.on:
            self.pending = False
            feedback = ''
            if time.time() > self.timeLastPosCheck + POS_LOGGING_RATE:
                self.timeLastPosCheck = time.time()
                self.sendPos()

            if self.msg != '':

                self.pending = True
                print("SRT Thread handling: " + self.msg)
                args = self.msg.split(" ")
                cmd = args[0]

                # Processing of command
                if cmd in ("pointRA", "pointGal", "pointAzAlt", "trackRA", "trackGal"):

                    if len(args) == 3:  # Parses arguments (point/track)
                        a, b = float(args[1]), float(args[2])
                        if self.msg == "pointRA":
                            a, b = RaDec2AzAlt(a, b)
                        if self.msg == "pointGal":
                            a, b = Gal2AzAlt(a, b)
                        if "point" in self.msg:
                            feedback = self.SRT.pointAzAlt(a, b)
                        elif self.msg == "trackRA":
                            feedback = self.SRT.trackRaDec(a, b)
                        elif self.msg == "trackGal":
                            feedback = self.SRT.trackGal(a, b)
                    else:
                        raise ValueError("ERROR : invalid command passed to server")

                if cmd in ("connect", "goHome", "untangle",
                           "standby", "disconnect"):

                    if len(args) == 1:
                        if self.msg == "goHome":
                            feedback = self.SRT.go_home()
                        elif self.msg == "connect":
                            feedback = self.SRT.connect()  # False for debug
                        elif self.msg == "disconnect":
                            feedback = self.SRT.disconnect()
                        elif self.msg == "untangle":
                            feedback = self.SRT.untangle()
                        elif self.msg == "standby":
                            feedback = self.SRT.standby()
                        elif self.msg == "wait":
                            feedback = ""

                    else:
                        raise ValueError(
                            "ERROR : invalid command passed to server")

                if cmd == "measure":
                    if len(args) == 7:  # Parses arguments (measurement)
                        centerFreq, bandwidth, sampleTime, duration, gain, channels = (
                            float(args[1]), float(args[2]), float(args[3]),
                            float(args[4]), float(args[5]), float(args[6]))

                        if self.measuring == 0:
                            self.measuring = 1
                            # TODO connect measurement, (remember to set self.measuring to 0). parameters are above.
                        else:
                            self.sendError("Already measuring!")
                    else:
                        raise ValueError(
                            "ERROR : invalid command passed to server")

                feedback = str(feedback)

                print("SRT Thread handled: " + self.msg + " with feedback: " + feedback)
                self.endMotion.emit(self.msg, feedback)
                self.msg = ''


class ServerGUI(QMainWindow):
    """Class that operates the server by handshaking clients, receiving and
    sending messages and modifying the GUI display in consequence.

    Owner of all threads operating the APM"""
    sendToSRTSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addToLog("Launched server.")

        # Updates the port on which the sever listens
        self.ui.spinBox_port.valueChanged.connect(self.portChanged)

        # Obtains the IP address of host on the network
        ipaddress = get_ipv4_address()
        self.setIPAddress(ipaddress)
        self.IPAddress = QHostAddress(ipaddress)
        self.port = self.ui.spinBox_port.value()

        # Initializes server
        self.server = QTcpServer(self)
        self.server.listen(self.IPAddress, self.port)
        self.client_socket = None
        self.original_stdout = sys.stdout  # Backup of stdout

        self.server.newConnection.connect(self.handleConnection)

        self.SRTThread = SRTThread()
        self.SRTThread.send2socket.connect(self.sendClient)
        self.SRTThread.endMotion.connect(self.sendEndMotion)
        self.sendToSRTSignal.connect(self.SRTThread.receiveCommand)
        # When in motion, stop asking for position. Tracking not affected

        self.measuring = 0

    def handleConnection(self):
        """Method triggered when a new client connects the server
        If a client is already connected, rejects the connection
        Otherwise, executes the handshake (sends CONNECTED to client)"""
        if self.client_socket is None:
            self.client_socket = self.server.nextPendingConnection()
            self.client_socket.readyRead.connect(self.receiveMessage)
            self.client_socket.disconnected.connect(self.disconnectClient)
            self.addToLog("Client connected.")
            self.sendClient("CONNECTED", True)
            # Redirect sys.stdout to send print statements to the client
            self.redirect_stdout()
        else:
            other_client = self.server.nextPendingConnection()
            other_client.write("BUSY".encode())
            self.addToLog(
                "New connection rejected for a client is already connected")
            other_client.disconnectFromHost()
            other_client.deleteLater()

    def disconnectClient(self):
        """Method triggered when the client disconnects from the server
        A safety SRT disconnect is called in order to set the antenna to
        standby mode"""
        if self.client_socket:
            self.addToLog("Client disconnected.")
            self.client_socket = None

            self.restore_stdout()  # Restore sys.stdout to its original state

            self.sendToSRTSignal.emit("disconnect")  # Disconnect SRT

    def redirect_stdout(self):
        """Operates the redirection of stdout to both the server console and
        to the client via a msg with PRINT status"""
        redirector = StdoutRedirector(sys.stdout)
        redirector.emettor.printMsg.connect(self.sendClient)
        sys.stdout = redirector

    def restore_stdout(self):
        """Method triggered when the client disconnects. Print statements are 
        no longer redirected to a client"""

        sys.stdout = self.original_stdout

    # ======= Send / Receive methods =======

    def sendClient(self, msg, verbose=True):
        """Send message to client"""

        if self.client_socket:
            unpausePosLoggingLater = False
            # Pauses the thread spamming the position getter
            if self.SRTThread.posLoggingOn:
                unpausePosLoggingLater = True
                self.SRTThread.pausePositionLogging()

            # Waits for the previous request to have returned to avoid multiple
            # messages sent to client
            time1 = time.time_ns()
            while self.SRTThread.pending:
                pass
            time2 = time.time_ns()
            print(f"DEBUG: waited {round((time2 - time1) / 1e6)} ms for SRTThread to stop pending (in fn sendClient)")

            msg = '&' + msg  # Adds a "begin" character
            # Sends the message
            self.client_socket.write(msg.encode())
            if verbose:
                self.addToLog(f"Message sent : {msg}")

            # If tracking, the position spamming thread should be turned back on
            if unpausePosLoggingLater:
                self.SRTThread.unpausePositionLogging()

        else:
            self.addToLog(f"No connected client to send msg : {msg}")

    def sendOK(self, msg):
        msg = "OK|" + msg
        self.sendClient(msg)

    def sendWarning(self, msg):
        msg = "WARNING|" + msg
        self.sendClient(msg)

    def sendError(self, msg):
        msg = "ERROR|" + msg
        self.sendClient(msg)

    def receiveMessage(self, verbose=True):
        """Method that handles receiving a message from the client"""
        if self.client_socket:
            msg = self.client_socket.readAll().data().decode()

            self.processMsg(msg, verbose)

    def processMsg(self, msg, verbose):
        """Method that processes the command sent from client.
        Note that several messages might be received simultaneously, hence
        the recursive approach taking advantage of the format of messages :
            &{command} {*args}
        """

        # Sort messages, sometimes several
        if '&' in msg:
            messages = msg.split('&')[1:]

            # If several messages
            if len(messages) > 1:
                print(f"Received concatenated messages : {messages}")
                for message in messages:
                    print(f"processing msg {message}")

                    # Re-add the start character
                    self.processMsg('&' + message, verbose)

                return

            # If only one message
            else:
                msg = messages[0]

        else:
            self.addToLog(
                f"Warning : incorrectly formatted message received : {msg}")
            return  # Ignores incorrectly formatted messages

        self.addToLog("Received: " + msg)

        if not self.SRTThread.pending:
            self.sendToSRTSignal.emit(msg)
        else:
            self.sendWarning("MOVING")

    def sendEndMotion(self, cmd, feedback):
        """Sends message to client when motion is ended

        This is a slot connected to signal self.motionThread.endMotion"""
        print(f"DEBUG : sendEndMotion with cmd = {cmd}, fb = {feedback}")
        self.sendClient("PRINT|" + feedback)

        if cmd == "connect":
            self.sendOK("connected")
        elif cmd == "disconnect":
            self.sendOK("disconnected")
        else:
            self.sendOK("IDLE")

    # ======== GUI methods ========

    def closeEvent(self, event):
        """Triggered when the server GUI is closed manually"""
        if self.client_socket:
            self.client_socket.disconnectFromHost()
        self.server.close()
        event.accept()

    def addToLog(self, strInput):
        """Adds statement to the GUI log console """
        self.ui.textBrowser_log.append(
            f"{strftime('%Y-%m-%d %H:%M:%S', localtime())}: " + strInput)

    def setIPAddress(self, stringIn):
        """Sets the IP address displayed in the GUI """
        self.ui.lineEdit_IP.setText(stringIn)

    def portChanged(self):
        """Handles manual port changing"""

        print("Port changed.")
        self.port = self.ui.spinBox_port.value()
        self.server.close()
        self.server.listen(self.IPAddress, self.port)


def get_ipv4_address():
    """Method that gets the ipv4 address of host to initialize the server """

    try:
        # Get a list of all network interfaces
        interfaces = QNetworkInterface.allInterfaces()
        for interface in interfaces:
            # Check if the interface is not loopback and is running
            if not interface.flags() & QNetworkInterface.InterfaceFlag.IsLoopBack and \
                    interface.flags() & QNetworkInterface.InterfaceFlag.IsRunning:
                addresses = interface.addressEntries()
                for address in addresses:
                    if address.ip().protocol() == QAbstractSocket.NetworkLayerProtocol.IPv4Protocol:
                        return address.ip().toString()
        return "Not Found"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    sys.argv[0] = 'Astro Antenna'
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Astro Antenna")

    widgetServer = ServerGUI()
    widgetServer.show()
    sys.exit(app.exec())
