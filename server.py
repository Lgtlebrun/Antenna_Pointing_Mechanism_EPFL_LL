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

SRT = Srt("/dev/ttyUSB0", 115200, 1)


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


class MotionThread(QThread):

    """Thread that parallelizes the execution of long-duration motion tasks"""

    endMotion = Signal(str, str)

    def __init__(self,  cmd: str, a=None, b=None, parent=None):
        super().__init__(parent)

        self.cmd = cmd
        self.a = a
        self.b = b

    def run(self):

        feedback = ''
        print(self.cmd)

        if self.cmd == "pointRA":
            self.a, self.b = RaDec2AzAlt(self.a, self.b)

        if self.cmd == "pointGal":
            self.a, self.b = Gal2AzAlt(self.a, self.b)

        if "point" in self.cmd:
            feedback = SRT.pointAzAlt(self.a, self.b)

        elif self.cmd == "goHome":
            feedback = SRT.go_home()

        elif self.cmd == "trackRA":
            feedback = SRT.trackRaDec(self.a, self.b)

        elif self.cmd == "trackGal":
            feedback = SRT.trackGal(self.a, self.b)

        elif self.cmd == "connect":
            feedback = SRT.connect()  # False for debug

        elif self.cmd == "disconnect":
            feedback = SRT.disconnect()

        elif self.cmd == "untangle":
            feedback = SRT.untangle()

        elif self.cmd == "standby":
            feedback = SRT.standby()

        elif self.cmd == "wait":
            feedback = ""
            pass

        feedback = str(feedback)
        self.endMotion.emit(self.cmd, feedback)


# class BckgrndServTask(BckgrndTask):

#     """ Background thread able to send messages to the client.

#     self.wait : Flag that indicates the message should be delayed until new order.
#     Avoids spamming SRT with multiple commands. Flag risen and lowered by the
#     main server thread only"""

#     def __init__(self, parent=None):

#         BckgrndTask.__init__(self)


class PositionThread(QThread):

    """Thread that updates continuously the current coordinates of the antenna """

    # Signal emitted to pass the Serevr the msg to send to the client
    send2socket = Signal(str)

    def __init__(self, parent=None):
        """No need to indicate a particular serial port for the thread will use 
        the global variable SRT which handles waiting for tracker/ping"""

        super().__init__(parent)
        self.on = False         # May pause the thread but does not kill it
        self.stop = False       # kills the thread
        self.pending = False    # flag on while waiting for answer from ser

        self.daemon = True

    def stop(self):             # Allows to kill the thread
        self.stop = True

    def pause(self):
        self.on = False

    def unpause(self):
        self.on = True

    def run(self):
        while not self.stop:

            if self.on:
                self.pending = True         # Indicates waiting for an answer
                self.sendPos()
                self.pending = False        # Answer received

                # delay next
                timeNow = time.time()
                while time.time() < timeNow + TRACKING_RATE:
                    pass

    def sendClient(self, msg):

        self.send2socket.emit(msg)

    def sendOK(self, msg):

        msg = "OK|" + msg
        self.sendClient(msg)

    def sendWarning(self, msg):

        msg = "WARNING|" + msg
        self.sendClient(msg)

    def sendError(self, msg):

        msg = "ERROR|"+msg
        self.sendClient(msg)

    def sendPos(self):
        """Sends position in all coordinates to client"""

        az, alt = SRT.getAzAlt()
        ra, dec = SRT.getPos()
        long, lat = SRT.getGal()

        if (az == -1) or (alt == -1):
            self.sendError(
                "Error while trying to get current coordinates. Hardware may be damaged. Please report this event to the person in charge ASAP")

        msg = f"COORDS {az} {alt} {ra} {dec} {long} {lat}"
        self.sendOK(msg)


class ServerGUI(QMainWindow):
    """Class that operates the server by handshaking clients, receiving and
    sending messages and modifying the GUI display in consequence.

    Owner of all threads operating the APM"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addToLog("Launched server.")

        # Updates the port on which the sever listens
        self.ui.spinBox_port.valueChanged.connect(self.portChanged)

        # Obtains the IP address of host on the network
        ipaddress = self.get_ipv4_address()
        self.setIPAddress(ipaddress)
        self.IPAddress = QHostAddress(ipaddress)
        self.port = self.ui.spinBox_port.value()

        # Initializes server
        self.server = QTcpServer(self)
        self.server.listen(self.IPAddress, self.port)
        self.client_socket = None
        self.original_stdout = sys.stdout  # Backup of stdout

        self.server.newConnection.connect(self.handleConnection)

        self.motionThread = MotionThread("wait")

        # When in motion, stop asking for position. Tracking not affected

        self.posThread = PositionThread()
        self.posThread.send2socket.connect(self.sendClient)
        self.posThread.start()  # Start in pause mode

        self.measuring = 0

    def get_ipv4_address(self):
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
                f"New connection rejected for a client is already connected")
            other_client.disconnectFromHost()
            other_client.deleteLater()

    def disconnectClient(self):
        """Method triggered when the client disconnects from the server
        A safety SRT.disconnect() is called in order to set the antenna to
        standby mode"""

        if self.client_socket:
            self.addToLog("Client disconnected.")
            self.client_socket = None
            # Restore sys.stdout to its original state
            self.restore_stdout()
            self.motionThread = MotionThread("disconnect")
            self.motionThread.start()

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

            # Pauses the thread spamming the position getter
            if self.posThread.on:
                self.posThread.pause()

            # Waits for the previous request to have returned to avoid multiple
            # messages sent to client
            while self.posThread.pending:
                pass

            msg = '&' + msg  # Adds a "begin" character
            # Sends the message
            self.client_socket.write(msg.encode())
            if verbose:
                self.addToLog(f"Message sent : {msg}")

            # If tracking, the position spamming thread should be turned back on
            if SRT.tracking:
                self.posThread.unpause()

        else:
            self.addToLog(f"No connected client to send msg : {msg}")

    def sendOK(self, msg):

        msg = "OK|" + msg
        self.sendClient(msg)

    def sendWarning(self, msg):

        msg = "WARNING|" + msg
        self.sendClient(msg)

    def sendError(self, msg):

        msg = "ERROR|"+msg
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
                f"Warning : incorrectly formated message received : {msg}")
            return      # Ignores incorrectly formatted messages

        self.addToLog("Received: " + msg)
        args = msg.split(" ")
        cmd = args[0]

        # Processing of command
        if cmd in ("connect", "pointRA", "pointGal ", "pointAzAlt", "trackRA", "trackGal", "goHome", "untangle", "standby", "disconnect"):

            if not self.motionThread.isRunning():
                # Pauses thread spamming position
                self.pausePosThread()
                while self.posThread.pending:   # Waits for posThread return
                    continue

                if len(args) > 1:   # Parses arguments
                    a, b = float(args[1]), float(args[2])
                    self.motionThread = MotionThread(cmd, a, b)

                elif len(args) == 1:
                    self.motionThread = MotionThread(cmd)

                else:
                    raise ValueError(
                        "ERROR : invalid command passed to server")

                self.motionThread.endMotion.connect(self.sendEndMotion)

                self.motionThread.start()

            else:
                self.sendWarning("MOVING")
        elif cmd == 'measure':
            centerFreq, bandwidth, sampleTime, duration, gain, channels = (float(args[1]), float(args[2]), float(args[3]),
                                                                           float(args[4]), float(args[5]),float(args[6]))
            if(self.measuring == 0):
                self.measuring = 1
                #TODO connect actual measurement, remember to set self.measuring to 0. Nec. parameters are above.
            else:
                self.sendError("Already measuring!")


    def sendEndMotion(self, cmd, feedback):
        """Sends message to client when motion is ended

        This is a slot connected to signal self.motionThread.endMotion"""
        print(f"DEBUG : sendEndMotion with cmd = {cmd}, fb = {feedback}")
        self.sendClient("PRINT|" + feedback)

        if cmd == "connect":
            self.sendOK("connected")
            self.posThread.unpause()
        elif cmd == "disconnect":
            self.sendOK("disconnected")
        else:
            self.sendOK("IDLE")
            self.posThread.unpause()

    def pausePosThread(self):
        """Blocks the posThread from sending messages to the client. Called
        at beginning of motion to avoid spamming SRT with multiple commands"""

        self.posThread.pause()  # Blocks the Pos Thread

    def sendPos(self):
        """Sends current position in all coordinates to client """

        self.posThread.sendPos()

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


if __name__ == "__main__":
    sys.argv[0] = 'Astro Antenna'
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Astro Antenna")

    widgetServer = ServerGUI()
    widgetServer.show()
    sys.exit(app.exec())
