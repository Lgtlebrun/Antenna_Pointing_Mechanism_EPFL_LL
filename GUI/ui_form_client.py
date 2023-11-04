# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formMainClient.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGraphicsView, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(802, 840)
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_home = QWidget()
        self.tab_home.setObjectName(u"tab_home")
        self.verticalLayout_3 = QVBoxLayout(self.tab_home)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_CurrentPosition_3 = QLabel(self.tab_home)
        self.label_CurrentPosition_3.setObjectName(u"label_CurrentPosition_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_CurrentPosition_3.sizePolicy().hasHeightForWidth())
        self.label_CurrentPosition_3.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.label_CurrentPosition_3, 0, Qt.AlignHCenter)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.pushButton_openCamera = QPushButton(self.tab_home)
        self.pushButton_openCamera.setObjectName(u"pushButton_openCamera")

        self.horizontalLayout_5.addWidget(self.pushButton_openCamera)

        self.pushButton_goHome = QPushButton(self.tab_home)
        self.pushButton_goHome.setObjectName(u"pushButton_goHome")

        self.horizontalLayout_5.addWidget(self.pushButton_goHome)

        self.pushButton_Untangle = QPushButton(self.tab_home)
        self.pushButton_Untangle.setObjectName(u"pushButton_Untangle")

        self.horizontalLayout_5.addWidget(self.pushButton_Untangle)

        self.pushButton_Standby = QPushButton(self.tab_home)
        self.pushButton_Standby.setObjectName(u"pushButton_Standby")

        self.horizontalLayout_5.addWidget(self.pushButton_Standby)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.line_8 = QFrame(self.tab_home)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_8)

        self.label_CurrentPosition = QLabel(self.tab_home)
        self.label_CurrentPosition.setObjectName(u"label_CurrentPosition")
        sizePolicy.setHeightForWidth(self.label_CurrentPosition.sizePolicy().hasHeightForWidth())
        self.label_CurrentPosition.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.label_CurrentPosition, 0, Qt.AlignHCenter)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.DecLabel = QLabel(self.tab_home)
        self.DecLabel.setObjectName(u"DecLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.DecLabel.sizePolicy().hasHeightForWidth())
        self.DecLabel.setSizePolicy(sizePolicy1)
        self.DecLabel.setMinimumSize(QSize(40, 0))
        self.DecLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.DecLabel, 1, 2, 1, 1)

        self.AzLabel = QLabel(self.tab_home)
        self.AzLabel.setObjectName(u"AzLabel")
        sizePolicy1.setHeightForWidth(self.AzLabel.sizePolicy().hasHeightForWidth())
        self.AzLabel.setSizePolicy(sizePolicy1)
        self.AzLabel.setMinimumSize(QSize(40, 0))
        self.AzLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.AzLabel, 0, 2, 1, 1)

        self.label_GalB = QLabel(self.tab_home)
        self.label_GalB.setObjectName(u"label_GalB")
        sizePolicy1.setHeightForWidth(self.label_GalB.sizePolicy().hasHeightForWidth())
        self.label_GalB.setSizePolicy(sizePolicy1)
        self.label_GalB.setMinimumSize(QSize(40, 0))
        self.label_GalB.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_GalB, 2, 2, 1, 1)

        self.label_2 = QLabel(self.tab_home)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.RaLabel = QLabel(self.tab_home)
        self.RaLabel.setObjectName(u"RaLabel")
        sizePolicy1.setHeightForWidth(self.RaLabel.sizePolicy().hasHeightForWidth())
        self.RaLabel.setSizePolicy(sizePolicy1)
        self.RaLabel.setMinimumSize(QSize(40, 0))
        self.RaLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.RaLabel, 1, 1, 1, 1)

        self.label_4 = QLabel(self.tab_home)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_GalL = QLabel(self.tab_home)
        self.label_GalL.setObjectName(u"label_GalL")
        sizePolicy1.setHeightForWidth(self.label_GalL.sizePolicy().hasHeightForWidth())
        self.label_GalL.setSizePolicy(sizePolicy1)
        self.label_GalL.setMinimumSize(QSize(40, 0))
        self.label_GalL.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_GalL, 2, 1, 1, 1)

        self.AltLabel = QLabel(self.tab_home)
        self.AltLabel.setObjectName(u"AltLabel")
        sizePolicy1.setHeightForWidth(self.AltLabel.sizePolicy().hasHeightForWidth())
        self.AltLabel.setSizePolicy(sizePolicy1)
        self.AltLabel.setMinimumSize(QSize(40, 0))
        self.AltLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.AltLabel, 0, 1, 1, 1)

        self.label_6 = QLabel(self.tab_home)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.line_3 = QFrame(self.tab_home)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.label_CurrentPosition_2 = QLabel(self.tab_home)
        self.label_CurrentPosition_2.setObjectName(u"label_CurrentPosition_2")
        sizePolicy.setHeightForWidth(self.label_CurrentPosition_2.sizePolicy().hasHeightForWidth())
        self.label_CurrentPosition_2.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.label_CurrentPosition_2, 0, Qt.AlignHCenter)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, -1, -1)
        self.comboBoxTracking = QComboBox(self.tab_home)
        self.comboBoxTracking.addItem("")
        self.comboBoxTracking.addItem("")
        self.comboBoxTracking.addItem("")
        self.comboBoxTracking.setObjectName(u"comboBoxTracking")

        self.horizontalLayout_11.addWidget(self.comboBoxTracking)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.LabelTrackingFirstCoord = QLabel(self.tab_home)
        self.LabelTrackingFirstCoord.setObjectName(u"LabelTrackingFirstCoord")
        sizePolicy1.setHeightForWidth(self.LabelTrackingFirstCoord.sizePolicy().hasHeightForWidth())
        self.LabelTrackingFirstCoord.setSizePolicy(sizePolicy1)
        self.LabelTrackingFirstCoord.setMinimumSize(QSize(30, 10))

        self.horizontalLayout_6.addWidget(self.LabelTrackingFirstCoord)

        self.doubleSpinBox_TrackFirstCoordDecimal = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackFirstCoordDecimal.setObjectName(u"doubleSpinBox_TrackFirstCoordDecimal")
        self.doubleSpinBox_TrackFirstCoordDecimal.setMinimumSize(QSize(30, 0))
        self.doubleSpinBox_TrackFirstCoordDecimal.setDecimals(3)
        self.doubleSpinBox_TrackFirstCoordDecimal.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_TrackFirstCoordDecimal.setMaximum(1000.000000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_TrackFirstCoordDecimal)

        self.LabelTrackingFirstCoord_2 = QLabel(self.tab_home)
        self.LabelTrackingFirstCoord_2.setObjectName(u"LabelTrackingFirstCoord_2")
        sizePolicy1.setHeightForWidth(self.LabelTrackingFirstCoord_2.sizePolicy().hasHeightForWidth())
        self.LabelTrackingFirstCoord_2.setSizePolicy(sizePolicy1)
        self.LabelTrackingFirstCoord_2.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_6.addWidget(self.LabelTrackingFirstCoord_2)

        self.line_5 = QFrame(self.tab_home)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line_5)

        self.doubleSpinBox_TrackFirstCoord_h = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackFirstCoord_h.setObjectName(u"doubleSpinBox_TrackFirstCoord_h")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_TrackFirstCoord_h.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_TrackFirstCoord_h.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_TrackFirstCoord_h.setMinimumSize(QSize(30, 0))
        self.doubleSpinBox_TrackFirstCoord_h.setDecimals(0)
        self.doubleSpinBox_TrackFirstCoord_h.setMinimum(0.000000000000000)
        self.doubleSpinBox_TrackFirstCoord_h.setMaximum(23.000000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_TrackFirstCoord_h)

        self.LabelTrackingFirstCoord_3 = QLabel(self.tab_home)
        self.LabelTrackingFirstCoord_3.setObjectName(u"LabelTrackingFirstCoord_3")
        sizePolicy1.setHeightForWidth(self.LabelTrackingFirstCoord_3.sizePolicy().hasHeightForWidth())
        self.LabelTrackingFirstCoord_3.setSizePolicy(sizePolicy1)
        self.LabelTrackingFirstCoord_3.setMinimumSize(QSize(29, 10))

        self.horizontalLayout_6.addWidget(self.LabelTrackingFirstCoord_3)

        self.doubleSpinBox_TrackFirstCoord_m = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackFirstCoord_m.setObjectName(u"doubleSpinBox_TrackFirstCoord_m")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_TrackFirstCoord_m.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_TrackFirstCoord_m.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_TrackFirstCoord_m.setMinimumSize(QSize(20, 0))
        self.doubleSpinBox_TrackFirstCoord_m.setBaseSize(QSize(0, 0))
        self.doubleSpinBox_TrackFirstCoord_m.setDecimals(0)
        self.doubleSpinBox_TrackFirstCoord_m.setMinimum(0.000000000000000)
        self.doubleSpinBox_TrackFirstCoord_m.setMaximum(59.000000000000000)
        self.doubleSpinBox_TrackFirstCoord_m.setValue(0.000000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_TrackFirstCoord_m)

        self.LabelTrackingFirstCoord_4 = QLabel(self.tab_home)
        self.LabelTrackingFirstCoord_4.setObjectName(u"LabelTrackingFirstCoord_4")
        sizePolicy1.setHeightForWidth(self.LabelTrackingFirstCoord_4.sizePolicy().hasHeightForWidth())
        self.LabelTrackingFirstCoord_4.setSizePolicy(sizePolicy1)
        self.LabelTrackingFirstCoord_4.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_6.addWidget(self.LabelTrackingFirstCoord_4)

        self.doubleSpinBox_TrackFirstCoord_s = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackFirstCoord_s.setObjectName(u"doubleSpinBox_TrackFirstCoord_s")
        self.doubleSpinBox_TrackFirstCoord_s.setDecimals(1)
        self.doubleSpinBox_TrackFirstCoord_s.setMinimum(0.000000000000000)
        self.doubleSpinBox_TrackFirstCoord_s.setMaximum(59.899999999999999)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_TrackFirstCoord_s)

        self.LabelTrackingFirstCoord_5 = QLabel(self.tab_home)
        self.LabelTrackingFirstCoord_5.setObjectName(u"LabelTrackingFirstCoord_5")
        sizePolicy1.setHeightForWidth(self.LabelTrackingFirstCoord_5.sizePolicy().hasHeightForWidth())
        self.LabelTrackingFirstCoord_5.setSizePolicy(sizePolicy1)
        self.LabelTrackingFirstCoord_5.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_6.addWidget(self.LabelTrackingFirstCoord_5)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_12)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.LabelTrackingSecondCoord = QLabel(self.tab_home)
        self.LabelTrackingSecondCoord.setObjectName(u"LabelTrackingSecondCoord")
        sizePolicy1.setHeightForWidth(self.LabelTrackingSecondCoord.sizePolicy().hasHeightForWidth())
        self.LabelTrackingSecondCoord.setSizePolicy(sizePolicy1)
        self.LabelTrackingSecondCoord.setMinimumSize(QSize(30, 10))

        self.horizontalLayout_12.addWidget(self.LabelTrackingSecondCoord)

        self.doubleSpinBox_TrackSecondCoordDecimal = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackSecondCoordDecimal.setObjectName(u"doubleSpinBox_TrackSecondCoordDecimal")
        self.doubleSpinBox_TrackSecondCoordDecimal.setMinimumSize(QSize(30, 0))
        self.doubleSpinBox_TrackSecondCoordDecimal.setDecimals(3)
        self.doubleSpinBox_TrackSecondCoordDecimal.setMinimum(-1000.000000000000000)
        self.doubleSpinBox_TrackSecondCoordDecimal.setMaximum(1000.000000000000000)

        self.horizontalLayout_12.addWidget(self.doubleSpinBox_TrackSecondCoordDecimal)

        self.LabelTrackingSecondCoord_2 = QLabel(self.tab_home)
        self.LabelTrackingSecondCoord_2.setObjectName(u"LabelTrackingSecondCoord_2")
        sizePolicy1.setHeightForWidth(self.LabelTrackingSecondCoord_2.sizePolicy().hasHeightForWidth())
        self.LabelTrackingSecondCoord_2.setSizePolicy(sizePolicy1)
        self.LabelTrackingSecondCoord_2.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_12.addWidget(self.LabelTrackingSecondCoord_2)

        self.line_7 = QFrame(self.tab_home)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_12.addWidget(self.line_7)

        self.doubleSpinBox_TrackSecondCoord_Deg = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackSecondCoord_Deg.setObjectName(u"doubleSpinBox_TrackSecondCoord_Deg")
        self.doubleSpinBox_TrackSecondCoord_Deg.setMinimumSize(QSize(30, 0))
        self.doubleSpinBox_TrackSecondCoord_Deg.setDecimals(0)
        self.doubleSpinBox_TrackSecondCoord_Deg.setMinimum(-90.000000000000000)
        self.doubleSpinBox_TrackSecondCoord_Deg.setMaximum(360.000000000000000)

        self.horizontalLayout_12.addWidget(self.doubleSpinBox_TrackSecondCoord_Deg)

        self.LabelTrackingSecondCoord_3 = QLabel(self.tab_home)
        self.LabelTrackingSecondCoord_3.setObjectName(u"LabelTrackingSecondCoord_3")
        sizePolicy1.setHeightForWidth(self.LabelTrackingSecondCoord_3.sizePolicy().hasHeightForWidth())
        self.LabelTrackingSecondCoord_3.setSizePolicy(sizePolicy1)
        self.LabelTrackingSecondCoord_3.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_12.addWidget(self.LabelTrackingSecondCoord_3)

        self.doubleSpinBox_TrackSecondCoord_m = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackSecondCoord_m.setObjectName(u"doubleSpinBox_TrackSecondCoord_m")
        self.doubleSpinBox_TrackSecondCoord_m.setMinimumSize(QSize(20, 0))
        self.doubleSpinBox_TrackSecondCoord_m.setDecimals(0)
        self.doubleSpinBox_TrackSecondCoord_m.setMinimum(0.000000000000000)
        self.doubleSpinBox_TrackSecondCoord_m.setMaximum(59.000000000000000)

        self.horizontalLayout_12.addWidget(self.doubleSpinBox_TrackSecondCoord_m)

        self.LabelTrackingSecondCoord_4 = QLabel(self.tab_home)
        self.LabelTrackingSecondCoord_4.setObjectName(u"LabelTrackingSecondCoord_4")
        sizePolicy1.setHeightForWidth(self.LabelTrackingSecondCoord_4.sizePolicy().hasHeightForWidth())
        self.LabelTrackingSecondCoord_4.setSizePolicy(sizePolicy1)
        self.LabelTrackingSecondCoord_4.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_12.addWidget(self.LabelTrackingSecondCoord_4)

        self.doubleSpinBox_TrackSecondCoord_s = QDoubleSpinBox(self.tab_home)
        self.doubleSpinBox_TrackSecondCoord_s.setObjectName(u"doubleSpinBox_TrackSecondCoord_s")
        self.doubleSpinBox_TrackSecondCoord_s.setDecimals(1)
        self.doubleSpinBox_TrackSecondCoord_s.setMinimum(0.000000000000000)
        self.doubleSpinBox_TrackSecondCoord_s.setMaximum(59.899999999999999)

        self.horizontalLayout_12.addWidget(self.doubleSpinBox_TrackSecondCoord_s)

        self.LabelTrackingSecondCoord_5 = QLabel(self.tab_home)
        self.LabelTrackingSecondCoord_5.setObjectName(u"LabelTrackingSecondCoord_5")
        sizePolicy1.setHeightForWidth(self.LabelTrackingSecondCoord_5.sizePolicy().hasHeightForWidth())
        self.LabelTrackingSecondCoord_5.setSizePolicy(sizePolicy1)
        self.LabelTrackingSecondCoord_5.setMinimumSize(QSize(20, 10))

        self.horizontalLayout_12.addWidget(self.LabelTrackingSecondCoord_5)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_13)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.line_2 = QFrame(self.tab_home)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_10)

        self.pushButton_GoTo = QPushButton(self.tab_home)
        self.pushButton_GoTo.setObjectName(u"pushButton_GoTo")
        sizePolicy.setHeightForWidth(self.pushButton_GoTo.sizePolicy().hasHeightForWidth())
        self.pushButton_GoTo.setSizePolicy(sizePolicy)
        self.pushButton_GoTo.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_10.addWidget(self.pushButton_GoTo)

        self.pushButton_StopTracking = QPushButton(self.tab_home)
        self.pushButton_StopTracking.setObjectName(u"pushButton_StopTracking")
        self.pushButton_StopTracking.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButton_StopTracking.sizePolicy().hasHeightForWidth())
        self.pushButton_StopTracking.setSizePolicy(sizePolicy)
        self.pushButton_StopTracking.setCheckable(False)
        self.pushButton_StopTracking.setFlat(False)

        self.horizontalLayout_10.addWidget(self.pushButton_StopTracking)

        self.checkBox_Tracking = QCheckBox(self.tab_home)
        self.checkBox_Tracking.setObjectName(u"checkBox_Tracking")

        self.horizontalLayout_10.addWidget(self.checkBox_Tracking)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_11)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)


        self.verticalLayout_3.addLayout(self.verticalLayout_6)

        self.line = QFrame(self.tab_home)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_Connect = QPushButton(self.tab_home)
        self.pushButton_Connect.setObjectName(u"pushButton_Connect")
        sizePolicy.setHeightForWidth(self.pushButton_Connect.sizePolicy().hasHeightForWidth())
        self.pushButton_Connect.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_Connect)

        self.pushButton_Disconnect = QPushButton(self.tab_home)
        self.pushButton_Disconnect.setObjectName(u"pushButton_Disconnect")
        sizePolicy.setHeightForWidth(self.pushButton_Disconnect.sizePolicy().hasHeightForWidth())
        self.pushButton_Disconnect.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_Disconnect)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.ConnectedLabel = QLabel(self.tab_home)
        self.ConnectedLabel.setObjectName(u"ConnectedLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ConnectedLabel.sizePolicy().hasHeightForWidth())
        self.ConnectedLabel.setSizePolicy(sizePolicy3)

        self.horizontalLayout_4.addWidget(self.ConnectedLabel)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.tab_home, "")
        self.tab_measure = QWidget()
        self.tab_measure.setObjectName(u"tab_measure")
        self.verticalLayout_4 = QVBoxLayout(self.tab_measure)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.label_3 = QLabel(self.tab_measure)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 21))
        self.label_3.setMaximumSize(QSize(100000, 16777215))

        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_5 = QLabel(self.tab_measure)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 21))
        self.label_5.setMaximumSize(QSize(10000, 16777215))

        self.gridLayout_2.addWidget(self.label_5, 0, 3, 1, 1)

        self.label_8 = QLabel(self.tab_measure)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(10000, 16777215))

        self.gridLayout_2.addWidget(self.label_8, 1, 3, 1, 1)

        self.doubleSpinBox_duration = QDoubleSpinBox(self.tab_measure)
        self.doubleSpinBox_duration.setObjectName(u"doubleSpinBox_duration")
        self.doubleSpinBox_duration.setMaximumSize(QSize(70, 16777215))
        self.doubleSpinBox_duration.setMaximum(3600.000000000000000)
        self.doubleSpinBox_duration.setValue(60.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_duration, 1, 4, 1, 1)

        self.doubleSpinBox_tsample = QDoubleSpinBox(self.tab_measure)
        self.doubleSpinBox_tsample.setObjectName(u"doubleSpinBox_tsample")
        self.doubleSpinBox_tsample.setMaximumSize(QSize(70, 16777215))
        self.doubleSpinBox_tsample.setMaximum(3600.000000000000000)
        self.doubleSpinBox_tsample.setValue(1.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_tsample, 1, 2, 1, 1)

        self.doubleSpinBox_Bandwidth = QDoubleSpinBox(self.tab_measure)
        self.doubleSpinBox_Bandwidth.setObjectName(u"doubleSpinBox_Bandwidth")
        self.doubleSpinBox_Bandwidth.setMinimumSize(QSize(0, 21))
        self.doubleSpinBox_Bandwidth.setMaximumSize(QSize(70, 16777215))
        self.doubleSpinBox_Bandwidth.setDecimals(2)
        self.doubleSpinBox_Bandwidth.setValue(2.460000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_Bandwidth, 0, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 0, 5, 1, 1)

        self.label_7 = QLabel(self.tab_measure)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(10000, 16777215))

        self.gridLayout_2.addWidget(self.label_7, 1, 1, 1, 1)

        self.label_10 = QLabel(self.tab_measure)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(10000, 16777215))

        self.gridLayout_2.addWidget(self.label_10, 2, 3, 1, 1)

        self.label_9 = QLabel(self.tab_measure)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(10000, 16777215))

        self.gridLayout_2.addWidget(self.label_9, 2, 1, 1, 1)

        self.doubleSpinBox_gain = QDoubleSpinBox(self.tab_measure)
        self.doubleSpinBox_gain.setObjectName(u"doubleSpinBox_gain")
        self.doubleSpinBox_gain.setMaximumSize(QSize(70, 16777215))
        self.doubleSpinBox_gain.setDecimals(1)
        self.doubleSpinBox_gain.setValue(48.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_gain, 2, 2, 1, 1)

        self.spinBox_channels = QSpinBox(self.tab_measure)
        self.spinBox_channels.setObjectName(u"spinBox_channels")
        self.spinBox_channels.setMaximumSize(QSize(70, 16777215))
        self.spinBox_channels.setMaximum(4096)
        self.spinBox_channels.setSingleStep(16)
        self.spinBox_channels.setValue(2048)

        self.gridLayout_2.addWidget(self.spinBox_channels, 2, 4, 1, 1)

        self.doubleSpinBox_centerFreq = QDoubleSpinBox(self.tab_measure)
        self.doubleSpinBox_centerFreq.setObjectName(u"doubleSpinBox_centerFreq")
        self.doubleSpinBox_centerFreq.setMinimumSize(QSize(0, 21))
        self.doubleSpinBox_centerFreq.setMaximumSize(QSize(70, 16777215))
        self.doubleSpinBox_centerFreq.setDecimals(1)
        self.doubleSpinBox_centerFreq.setMaximum(2000.000000000000000)
        self.doubleSpinBox_centerFreq.setValue(1420.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_centerFreq, 0, 2, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_8)

        self.pushButton_LaunchMeasurement = QPushButton(self.tab_measure)
        self.pushButton_LaunchMeasurement.setObjectName(u"pushButton_LaunchMeasurement")

        self.horizontalLayout_9.addWidget(self.pushButton_LaunchMeasurement)

        self.pushButton_StopMeasurement = QPushButton(self.tab_measure)
        self.pushButton_StopMeasurement.setObjectName(u"pushButton_StopMeasurement")

        self.horizontalLayout_9.addWidget(self.pushButton_StopMeasurement)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.label_17 = QLabel(self.tab_measure)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_4.addWidget(self.label_17, 0, Qt.AlignHCenter)

        self.progressBar_measurement = QProgressBar(self.tab_measure)
        self.progressBar_measurement.setObjectName(u"progressBar_measurement")
        self.progressBar_measurement.setValue(0)

        self.verticalLayout_4.addWidget(self.progressBar_measurement)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.label_18 = QLabel(self.tab_measure)
        self.label_18.setObjectName(u"label_18")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy4)

        self.horizontalLayout_8.addWidget(self.label_18)

        self.label_MeasureStatus = QLabel(self.tab_measure)
        self.label_MeasureStatus.setObjectName(u"label_MeasureStatus")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_MeasureStatus.sizePolicy().hasHeightForWidth())
        self.label_MeasureStatus.setSizePolicy(sizePolicy5)

        self.horizontalLayout_8.addWidget(self.label_MeasureStatus)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_measure, "")
        self.tab_plot = QWidget()
        self.tab_plot.setObjectName(u"tab_plot")
        self.verticalLayout_5 = QVBoxLayout(self.tab_plot)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_11 = QLabel(self.tab_plot)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_3.addWidget(self.label_11)

        self.lineEdit_CalibFile = QLineEdit(self.tab_plot)
        self.lineEdit_CalibFile.setObjectName(u"lineEdit_CalibFile")
        self.lineEdit_CalibFile.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_CalibFile)

        self.pushButton_browseCalib = QPushButton(self.tab_plot)
        self.pushButton_browseCalib.setObjectName(u"pushButton_browseCalib")

        self.horizontalLayout_3.addWidget(self.pushButton_browseCalib)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_16 = QLabel(self.tab_plot)
        self.label_16.setObjectName(u"label_16")
        sizePolicy1.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy1)
        self.label_16.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_7.addWidget(self.label_16)

        self.lineEdit_MeasureFile = QLineEdit(self.tab_plot)
        self.lineEdit_MeasureFile.setObjectName(u"lineEdit_MeasureFile")
        self.lineEdit_MeasureFile.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.lineEdit_MeasureFile)

        self.pushButton_browseMeasureFile = QPushButton(self.tab_plot)
        self.pushButton_browseMeasureFile.setObjectName(u"pushButton_browseMeasureFile")

        self.horizontalLayout_7.addWidget(self.pushButton_browseMeasureFile)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.line_6 = QFrame(self.tab_plot)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_6)

        self.pushButton_Plot = QPushButton(self.tab_plot)
        self.pushButton_Plot.setObjectName(u"pushButton_Plot")

        self.verticalLayout_5.addWidget(self.pushButton_Plot, 0, Qt.AlignHCenter)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.graphicsView_4 = QGraphicsView(self.tab_plot)
        self.graphicsView_4.setObjectName(u"graphicsView_4")

        self.gridLayout_3.addWidget(self.graphicsView_4, 3, 0, 1, 1)

        self.graphicsView_3 = QGraphicsView(self.tab_plot)
        self.graphicsView_3.setObjectName(u"graphicsView_3")

        self.gridLayout_3.addWidget(self.graphicsView_3, 1, 1, 1, 1)

        self.graphicsView_2 = QGraphicsView(self.tab_plot)
        self.graphicsView_2.setObjectName(u"graphicsView_2")

        self.gridLayout_3.addWidget(self.graphicsView_2, 1, 0, 1, 1)

        self.label_12 = QLabel(self.tab_plot)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1, Qt.AlignHCenter)

        self.graphicsView_5 = QGraphicsView(self.tab_plot)
        self.graphicsView_5.setObjectName(u"graphicsView_5")

        self.gridLayout_3.addWidget(self.graphicsView_5, 3, 1, 1, 1)

        self.label_13 = QLabel(self.tab_plot)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_3.addWidget(self.label_13, 0, 1, 1, 1, Qt.AlignHCenter)

        self.label_14 = QLabel(self.tab_plot)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1, Qt.AlignHCenter)

        self.label_15 = QLabel(self.tab_plot)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_3.addWidget(self.label_15, 2, 1, 1, 1, Qt.AlignHCenter)


        self.verticalLayout_5.addLayout(self.gridLayout_3)

        self.tabWidget.addTab(self.tab_plot, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.line_4 = QFrame(Widget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.textBrowser_log = QTextBrowser(Widget)
        self.textBrowser_log.setObjectName(u"textBrowser_log")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.textBrowser_log.sizePolicy().hasHeightForWidth())
        self.textBrowser_log.setSizePolicy(sizePolicy6)
        self.textBrowser_log.setMinimumSize(QSize(0, 200))

        self.verticalLayout.addWidget(self.textBrowser_log)


        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Radio Antenna Connection Software ", None))
        self.label_CurrentPosition_3.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p><span style=\" font-size:16pt;\">Basic commands</span></p></body></html>", None))
        self.pushButton_openCamera.setText(QCoreApplication.translate("Widget", u"Open Camera", None))
        self.pushButton_goHome.setText(QCoreApplication.translate("Widget", u"Go Home", None))
        self.pushButton_Untangle.setText(QCoreApplication.translate("Widget", u"Untangle", None))
        self.pushButton_Standby.setText(QCoreApplication.translate("Widget", u"Standby", None))
        self.label_CurrentPosition.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p><span style=\" font-size:16pt;\">Current position</span></p></body></html>", None))
        self.DecLabel.setText(QCoreApplication.translate("Widget", u"-", None))
        self.AzLabel.setText(QCoreApplication.translate("Widget", u"-", None))
        self.label_GalB.setText(QCoreApplication.translate("Widget", u"-", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Alt/Az", None))
        self.RaLabel.setText(QCoreApplication.translate("Widget", u"-", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Ra/Dec", None))
        self.label_GalL.setText(QCoreApplication.translate("Widget", u"-", None))
        self.AltLabel.setText(QCoreApplication.translate("Widget", u"-", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Gal. Coords", None))
        self.label_CurrentPosition_2.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p><span style=\" font-size:16pt;\">Go To</span></p></body></html>", None))
        self.comboBoxTracking.setItemText(0, QCoreApplication.translate("Widget", u"Ra/Dec", None))
        self.comboBoxTracking.setItemText(1, QCoreApplication.translate("Widget", u"Galactic", None))
        self.comboBoxTracking.setItemText(2, QCoreApplication.translate("Widget", u"Az/Alt", None))

        self.LabelTrackingFirstCoord.setText(QCoreApplication.translate("Widget", u"Ra", None))
        self.LabelTrackingFirstCoord_2.setText(QCoreApplication.translate("Widget", u"\u00b0", None))
        self.LabelTrackingFirstCoord_3.setText(QCoreApplication.translate("Widget", u"h", None))
        self.LabelTrackingFirstCoord_4.setText(QCoreApplication.translate("Widget", u"m", None))
        self.LabelTrackingFirstCoord_5.setText(QCoreApplication.translate("Widget", u"s", None))
        self.LabelTrackingSecondCoord.setText(QCoreApplication.translate("Widget", u"Dec", None))
        self.LabelTrackingSecondCoord_2.setText(QCoreApplication.translate("Widget", u"\u00b0", None))
        self.LabelTrackingSecondCoord_3.setText(QCoreApplication.translate("Widget", u"\u00b0", None))
        self.LabelTrackingSecondCoord_4.setText(QCoreApplication.translate("Widget", u"m", None))
        self.LabelTrackingSecondCoord_5.setText(QCoreApplication.translate("Widget", u"s", None))
        self.pushButton_GoTo.setText(QCoreApplication.translate("Widget", u"Go To", None))
        self.pushButton_StopTracking.setText(QCoreApplication.translate("Widget", u"Stop Tracking", None))
        self.checkBox_Tracking.setText(QCoreApplication.translate("Widget", u"Tracking", None))
        self.pushButton_Connect.setText(QCoreApplication.translate("Widget", u"Connect", None))
        self.pushButton_Disconnect.setText(QCoreApplication.translate("Widget", u"Disconnect", None))
        self.ConnectedLabel.setText(QCoreApplication.translate("Widget", u"Connected to []", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_home), QCoreApplication.translate("Widget", u"Home", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Center Frequency (MHz)", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Bandwidth (MHz)", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"Duration", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"Sample Time", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Channels", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Gain", None))
        self.pushButton_LaunchMeasurement.setText(QCoreApplication.translate("Widget", u"Launch Measurement", None))
        self.pushButton_StopMeasurement.setText(QCoreApplication.translate("Widget", u"Stop measurement", None))
        self.label_17.setText(QCoreApplication.translate("Widget", u"Progress", None))
        self.label_18.setText(QCoreApplication.translate("Widget", u"Status:", None))
        self.label_MeasureStatus.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_measure), QCoreApplication.translate("Widget", u"Measurement", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"Calibration File", None))
        self.pushButton_browseCalib.setText(QCoreApplication.translate("Widget", u"Browse...", None))
        self.label_16.setText(QCoreApplication.translate("Widget", u"Measurement File", None))
        self.pushButton_browseMeasureFile.setText(QCoreApplication.translate("Widget", u"Browse...", None))
        self.pushButton_Plot.setText(QCoreApplication.translate("Widget", u"Plot", None))
        self.label_12.setText(QCoreApplication.translate("Widget", u"Average Spectrum", None))
        self.label_13.setText(QCoreApplication.translate("Widget", u"Calibrated Average Spectrum", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"Dynamic Spectrum (Waterfall)", None))
        self.label_15.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plot), QCoreApplication.translate("Widget", u"Plot", None))
    # retranslateUi

