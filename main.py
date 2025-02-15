import sys
import os
import json
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QMessageBox
from upload_worker import UploadWorker
from app.customwidgets.switch import Switch

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1105, 833)
        fontDB = QFontDatabase()
        bold_id = fontDB.addApplicationFont(resource_path("app/static/fonts/ggl-venuri-medium-72504837416.ttf"))
        normal_id = fontDB.addApplicationFont(resource_path("app/static/fonts/bpg_nino_mtavruli_normal-50137711009.otf"))
        if bold_id != -1:
            bold_family = QFontDatabase.applicationFontFamilies(bold_id)[0]
        else:
            bold_family = "Arial"
        if normal_id != -1:
            normal_family = QFontDatabase.applicationFontFamilies(normal_id)[0]
        else:
            normal_family = "Arial"
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.singleuploadPage = QtWidgets.QWidget()
        self.singleuploadPage.setStyleSheet("background-color: rgb(245,245,245)")
        self.singleuploadPage.setObjectName("singleuploadPage")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.singleuploadPage)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frm_top = QtWidgets.QFrame(self.singleuploadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.frm_top.setSizePolicy(sizePolicy)
        self.frm_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_top.setObjectName("frm_top")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frm_top)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.wdg_estage = QtWidgets.QWidget(self.frm_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.wdg_estage.setSizePolicy(sizePolicy)
        self.wdg_estage.setObjectName("wdg_estage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.wdg_estage)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_logo = QtWidgets.QLabel(self.wdg_estage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.lbl_logo.setSizePolicy(sizePolicy)
        self.lbl_logo.setFixedSize(QtCore.QSize(30, 30))
        self.lbl_logo.setStyleSheet("QLabel {\n"
                                    "    border-radius: 25px;\n"
                                    "    background-position: center;\n"
                                    "    background-repeat: no-repeat;\n"
                                    "    background-origin: content;\n"
                                    "}")
        self.lbl_logo.setText("")
        self.lbl_logo.setPixmap(QtGui.QPixmap(resource_path("app/static/images/logo.ico")))
        self.lbl_logo.setScaledContents(True)
        self.lbl_logo.setObjectName("lbl_logo")
        self.horizontalLayout_4.addWidget(self.lbl_logo)
        self.widget_6 = QtWidgets.QWidget(self.wdg_estage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_estage_geo = QtWidgets.QLabel(self.widget_6)
        self.lbl_estage_geo.setStyleSheet(f"QLabel {{\n"
                                          f"    font-family: \"{bold_family}\";\n"
                                          "    font-size: 18px;\n"
                                          "    color: #333333;\n"
                                          "}}")
        self.lbl_estage_geo.setScaledContents(True)
        self.lbl_estage_geo.setObjectName("lbl_estage_geo")
        self.verticalLayout_3.addWidget(self.lbl_estage_geo)
        self.lbl_estage_eng = QtWidgets.QLabel(self.widget_6)
        self.lbl_estage_eng.setStyleSheet("QLabel {\n"
                                          "    font-family: \"Arial\", sans-serif;\n"
                                          "    font-size: 18px;\n"
                                          "    font-weight: bold;\n"
                                          "    color: #333333;\n"
                                          "}")
        self.lbl_estage_eng.setScaledContents(True)
        self.lbl_estage_eng.setObjectName("lbl_estage_eng")
        self.verticalLayout_3.addWidget(self.lbl_estage_eng)
        self.horizontalLayout_4.addWidget(self.widget_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_17.addWidget(self.wdg_estage)
        self.horizontalLayout_17.setStretch(0, 1)
        self.wdg_accounts = QtWidgets.QWidget(self.frm_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.wdg_accounts.setSizePolicy(sizePolicy)
        self.wdg_accounts.setObjectName("wdg_accounts")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.wdg_accounts)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_8 = QtWidgets.QWidget(self.wdg_accounts)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setStyleSheet("background-color: rgb(254,254,254);")
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_18 = QtWidgets.QWidget(self.widget_8)
        self.widget_18.setObjectName("widget_18")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_18)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lbl_ss_user = QtWidgets.QLabel(self.widget_18)
        self.lbl_ss_user.setStyleSheet("QLabel {\n"
                                       "    font-family: \"Arial\", sans-serif;\n"
                                       "    font-size: 12px;\n"
                                       "    font-weight: bold;\n"
                                       "    color: black;\n"
                                       "    text-align: center;\n"
                                       "    margin: 0;\n"
                                       "}")
        self.lbl_ss_user.setScaledContents(False)
        self.lbl_ss_user.setObjectName("lbl_ss_user")
        self.verticalLayout_9.addWidget(self.lbl_ss_user)
        self.lbl_ss_email = QtWidgets.QLabel(self.widget_18)
        self.lbl_ss_email.setStyleSheet("QLabel {\n"
                                        "    font-family: \"Arial\", sans-serif;\n"
                                        "    font-size: 10px;\n"
                                        "    color: black;\n"
                                        "    text-align: center;\n"
                                        "    margin: 0;\n"
                                        "}")
        self.lbl_ss_email.setObjectName("lbl_ss_email")
        self.verticalLayout_9.addWidget(self.lbl_ss_email)
        self.horizontalLayout_5.addWidget(self.widget_18)
        self.horizontalLayout_5.addStretch()
        self.btn_change_ss_profile = QtWidgets.QPushButton(self.widget_8)
        self.btn_change_ss_profile.setStyleSheet(f"QPushButton {{\n"
                                                 f"    background-color: #0066FF;\n"
                                                 f"    color: white;\n"
                                                 f"    border: none;\n"
                                                 f"    border-radius: 5px;\n"
                                                 f"    padding: 5px 15px;\n"
                                                 f"    font-family: \"{bold_family}\";\n"
                                                 f"    font-size: 14px;\n"
                                                 f"    font-weight: bold;\n"
                                                 f"    text-align: center;\n"
                                                 f"}}\n"
                                                 f"QPushButton:hover {{\n"
                                                 f"    background-color: #0056E0;\n"
                                                 f"}}\n"
                                                 f"QPushButton:pressed {{\n"
                                                 f"    background-color: #0040B0;\n"
                                                 f"}}")
        self.btn_change_ss_profile.setObjectName("btn_change_ss_profile")
        self.horizontalLayout_5.addWidget(self.btn_change_ss_profile)
        self.horizontalLayout_6.addWidget(self.widget_8)
        self.widget_19 = QtWidgets.QWidget(self.wdg_accounts)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.widget_19.setSizePolicy(sizePolicy)
        self.widget_19.setStyleSheet("background-color: rgb(254,254,254);")
        self.widget_19.setObjectName("widget_19")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widget_19)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.widget_20 = QtWidgets.QWidget(self.widget_19)
        self.widget_20.setObjectName("widget_20")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_20)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.lbl_myhome_user = QtWidgets.QLabel(self.widget_20)
        self.lbl_myhome_user.setStyleSheet("QLabel {\n"
                                           "    font-family: \"Arial\", sans-serif;\n"
                                           "    font-size: 12px;\n"
                                           "    font-weight: bold;\n"
                                           "    color: black;\n"
                                           "    text-align: center;\n"
                                           "    margin: 0;\n"
                                           "}")
        self.lbl_myhome_user.setScaledContents(False)
        self.lbl_myhome_user.setObjectName("lbl_myhome_user")
        self.verticalLayout_10.addWidget(self.lbl_myhome_user)
        self.lbl_myhome_email = QtWidgets.QLabel(self.widget_20)
        self.lbl_myhome_email.setStyleSheet("QLabel {\n"
                                            "    font-family: \"Arial\", sans-serif;\n"
                                            "    font-size: 10px;\n"
                                            "    color: black;\n"
                                            "    text-align: center;\n"
                                            "    margin: 0;\n"
                                            "}")
        self.lbl_myhome_email.setObjectName("lbl_myhome_email")
        self.verticalLayout_10.addWidget(self.lbl_myhome_email)
        self.gridLayout_10.addWidget(self.widget_20, 0, 0, 1, 1)
        self.btn_change_myhome_profile = QtWidgets.QPushButton(self.widget_19)
        self.btn_change_myhome_profile.setStyleSheet(f"QPushButton {{\n"
                                                     f"    background-color: #28A745;\n"
                                                     f"    color: white;\n"
                                                     f"    border: none;\n"
                                                     f"    border-radius: 5px;\n"
                                                     f"    padding: 5px 15px;\n"
                                                     f"    font-family: \"{bold_family}\";\n"
                                                     f"    font-size: 14px;\n"
                                                     f"    font-weight: bold;\n"
                                                     f"    text-align: center;\n"
                                                     f"}}\n"
                                                     f"QPushButton:hover {{\n"
                                                     f"    background-color: #218838;\n"
                                                     f"}}\n"
                                                     f"QPushButton:pressed {{\n"
                                                     f"    background-color: #1E7E34;\n"
                                                     f"}}")
        self.btn_change_myhome_profile.setObjectName("btn_change_myhome_profile")
        self.gridLayout_10.addWidget(self.btn_change_myhome_profile, 0, 1, 1, 1)
        self.horizontalLayout_6.addWidget(self.widget_19)
        self.horizontalLayout_17.addWidget(self.wdg_accounts)
        self.horizontalLayout_17.setStretch(1, 10)
        spacerItem1 = QtWidgets.QSpacerItem(304, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem1)
        self.horizontalLayout_17.setStretch(2, 1)
        self.gridLayout_7.addWidget(self.frm_top, 0, 0, 1, 1)
        self.frm_mid = QtWidgets.QFrame(self.singleuploadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.frm_mid.setSizePolicy(sizePolicy)
        self.frm_mid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_mid.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_mid.setObjectName("frm_mid")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frm_mid)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.frm_mid_left = QtWidgets.QFrame(self.frm_mid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.frm_mid_left.setSizePolicy(sizePolicy)
        self.frm_mid_left.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_mid_left.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frm_mid_left.setObjectName("frm_mid_left")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frm_mid_left)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        self.horizontalLayout_16.addWidget(self.frm_mid_left)
        self.horizontalLayout_16.setStretch(0, 1)
        self.frm_mid_mid = QtWidgets.QFrame(self.frm_mid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.frm_mid_mid.setSizePolicy(sizePolicy)
        self.frm_mid_mid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_mid_mid.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_mid_mid.setObjectName("frm_mid_mid")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frm_mid_mid)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.singleScrapeMainWidget = QtWidgets.QWidget(self.frm_mid_mid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.singleScrapeMainWidget.setSizePolicy(sizePolicy)
        self.singleScrapeMainWidget.setObjectName("singleScrapeMainWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.singleScrapeMainWidget)
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_4.setHorizontalSpacing(20)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.widget_10 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lbl_currency = QtWidgets.QLabel(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.lbl_currency.setSizePolicy(sizePolicy)
        self.lbl_currency.setStyleSheet(f"QLabel {{\n"
                                        f"    font-family: \"{bold_family}\";\n"
                                        "    font-size: 12px;\n"
                                        "    color: black;\n"
                                        "    text-align: center;\n"
                                        "    margin: 0;\n"
                                        "}}")
        self.lbl_currency.setObjectName("lbl_currency")
        self.horizontalLayout_9.addWidget(self.lbl_currency)
        self.label_9 = QtWidgets.QLabel(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setStyleSheet("QLabel {\n"
                                   "    font-family: \"Arial\", sans-serif;\n"
                                   "    font-size: 12px;\n"
                                   "    color: gray;\n"
                                   "    text-align: center;\n"
                                   "    margin: 0;\n"
                                   "}")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_10.setSpacing(30)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.btn_usd = QtWidgets.QRadioButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.btn_usd.setSizePolicy(sizePolicy)
        self.btn_usd.setStyleSheet("QLabel {\n"
                                   "    font-family: \"Arial\", sans-serif;\n"
                                   "    font-size: 12px;\n"
                                   "    color: black;\n"
                                   "    text-align: center;\n"
                                   "    margin: 0;\n"
                                   "}")
        self.btn_usd.setObjectName("btn_usd")
        self.horizontalLayout_10.addWidget(self.btn_usd)
        self.btn_gel = QtWidgets.QRadioButton(self.widget_10)
        self.btn_gel.setStyleSheet("QLabel {\n"
                                   "    font-family: \"Arial\", sans-serif;\n"
                                   "    font-size: 12px;\n"
                                   "    color: black;\n"
                                   "    text-align: center;\n"
                                   "    margin: 0;\n"
                                   "}")
        self.btn_gel.setObjectName("btn_gel")
        self.horizontalLayout_10.addWidget(self.btn_gel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.gridLayout_4.addWidget(self.widget_10, 2, 0, 1, 1)
        self.widget_11 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        self.widget_11.setObjectName("widget_11")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_11)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(10, 5, 10, 5)
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lbl_desc_off = QtWidgets.QLabel(self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.lbl_desc_off.setSizePolicy(sizePolicy)
        self.lbl_desc_off.setStyleSheet(f"QLabel {{\n"
                                        f"    font-family: \"{normal_family}\";\n"
                                        "    font-size: 12px;\n"
                                        "    color: black;\n"
                                        "    text-align: center;\n"
                                        "    margin: 0;\n"
                                        "}}")
        self.lbl_desc_off.setObjectName("lbl_desc_off")
        self.horizontalLayout_11.addWidget(self.lbl_desc_off)
        self.wdg_switch = Switch(self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.wdg_switch.setSizePolicy(sizePolicy)
        self.wdg_switch.setObjectName("wdg_switch")
        self.horizontalLayout_11.addWidget(self.wdg_switch)
        self.lbl_desc_on = QtWidgets.QLabel(self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.lbl_desc_on.setSizePolicy(sizePolicy)
        self.lbl_desc_on.setStyleSheet(f"QLabel {{\n"
                                       f"    font-family: \"{normal_family}\";\n"
                                       "    font-size: 12px;\n"
                                       "    color: black;\n"
                                       "    text-align: center;\n"
                                       "    margin: 0;\n"
                                       "}}")
        self.lbl_desc_on.setObjectName("lbl_desc_on")
        self.horizontalLayout_11.addWidget(self.lbl_desc_on)
        self.gridLayout_5.addLayout(self.horizontalLayout_11, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 1, 1, 1, 1)
        self.lbl_desc = QtWidgets.QLabel(self.widget_11)
        self.lbl_desc.setStyleSheet(f"QLabel {{\n"
                                    f"    font-family: \"{bold_family}\";\n"
                                    "    font-size: 12px;\n"
                                    "    color: black;\n"
                                    "    text-align: center;\n"
                                    "    margin: 0;\n"
                                    "}}")
        self.lbl_desc.setObjectName("lbl_desc")
        self.gridLayout_5.addWidget(self.lbl_desc, 0, 0, 1, 2)
        self.gridLayout_4.addWidget(self.widget_11, 5, 0, 1, 1)
        self.widget_13 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_10 = QtWidgets.QLabel(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setStyleSheet(f"QLabel {{\n"
                                    f"    font-family: \"{bold_family}\";\n"
                                    "    font-size: 12px;\n"
                                    "    color: black;\n"
                                    "    text-align: center;\n"
                                    "    margin: 0;\n"
                                    "}}")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_12.addWidget(self.label_10)
        self.lbl_comment = QtWidgets.QLabel(self.widget_13)
        self.lbl_comment.setStyleSheet("QLabel {\n"
                                       "    font-family: \"Arial\", sans-serif;\n"
                                       "    font-size: 12px;\n"
                                       "    color: gray;\n"
                                       "    text-align: center;\n"
                                       "    margin: 0;\n"
                                       "}")
        self.lbl_comment.setText("")
        self.lbl_comment.setObjectName("lbl_comment")
        self.horizontalLayout_12.addWidget(self.lbl_comment)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.ted_comment = QtWidgets.QTextEdit(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ted_comment.setSizePolicy(sizePolicy)
        self.ted_comment.setMaximumSize(QtCore.QSize(16777215, 60))
        self.ted_comment.setStyleSheet(f"QTextEdit {{\n"
                                       f"    background-color: #F5F5F5;\n"
                                       f"    border: 1px solid #E0E0E0;\n"
                                       f"    border-radius: 8px;\n"
                                       f"    padding: 8px;\n"
                                       f"    font-family: \"Arial\", sans-serif;\n"
                                       f"    font-size: 12px;\n"
                                       f"    color: #333333;\n"
                                       f"}}\n"
                                       f"QTextEdit:focus {{\n"
                                       f"    border: 1px solid #BDBDBD;\n"
                                       f"    outline: none;\n"
                                       f"}}\n"
                                       f"QScrollBar:vertical {{\n"
                                       f"    background: transparent;\n"
                                       f"    width: 8px;\n"
                                       f"    margin: 2px;\n"
                                       f"    border: none;\n"
                                       f"}}\n"
                                       f"QScrollBar::handle:vertical {{\n"
                                       f"    background: #C0C0C0;\n"
                                       f"    min-height: 20px;\n"
                                       f"    border-radius: 4px;\n"
                                       f"}}\n"
                                       f"QScrollBar::handle:vertical:hover {{\n"
                                       f"    background: #A0A0A0;\n"
                                       f"}}\n"
                                       f"QScrollBar::sub-line:vertical,\n"
                                       f"QScrollBar::add-line:vertical {{\n"
                                       f"    background: none;\n"
                                       f"    height: 0px;\n"
                                       f"}}\n"
                                       f"QScrollBar::add-page:vertical,\n"
                                       f"QScrollBar::sub-page:vertical {{\n"
                                       f"    background: none;\n"
                                       f"}}")
        self.ted_comment.setObjectName("ted_comment")
        self.verticalLayout_5.addWidget(self.ted_comment)
        self.gridLayout_4.addWidget(self.widget_13, 4, 0, 1, 1)
        self.logoWidget_2 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        self.logoWidget_2.setObjectName("logoWidget_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.logoWidget_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lbl_single_upload = QtWidgets.QLabel(self.logoWidget_2)
        self.lbl_single_upload.setStyleSheet(f"QLabel {{\n"
                                             f"    font-family: \"{bold_family}\";\n"
                                             "    font-size: 20px;\n"
                                             "    color: black;\n"
                                             "    text-align: center;\n"
                                             "    margin: 0;\n"
                                             "}}")
        self.lbl_single_upload.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_single_upload.setObjectName("lbl_single_upload")
        self.verticalLayout_6.addWidget(self.lbl_single_upload)
        self.gridLayout_4.addWidget(self.logoWidget_2, 0, 0, 1, 1)
        self.widget_14 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_14)
        self.horizontalLayout_13.setContentsMargins(-1, -1, 20, -1)
        self.horizontalLayout_13.setSpacing(40)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem4 = QtWidgets.QSpacerItem(577, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem4)
        self.btn_upload = QtWidgets.QPushButton(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.btn_upload.setSizePolicy(sizePolicy)
        self.btn_upload.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.btn_upload.setStyleSheet(f"QPushButton {{\n"
                                      f"    background-color: #00594D;\n"
                                      f"    color: white;\n"
                                      f"    font-family: \"{bold_family}\";\n"
                                      f"    font-size: 12px;\n"
                                      f"    border: none;\n"
                                      f"    border-radius: 10px;\n"
                                      f"    padding: 8px 40px;\n"
                                      f"}}\n"
                                      f"QPushButton:hover {{\n"
                                      f"    background-color: #007367;\n"
                                      f"}}\n"
                                      f"QPushButton:pressed {{\n"
                                      f"    background-color: #004A41;\n"
                                      f"}}")
        self.btn_upload.setDefault(False)
        self.btn_upload.setFlat(False)
        self.btn_upload.setObjectName("btn_upload")
        self.horizontalLayout_13.addWidget(self.btn_upload, 0, QtCore.Qt.AlignRight)
        self.gridLayout_4.addWidget(self.widget_14, 6, 0, 1, 1)
        self.widget_15 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setStyleSheet(f"QLabel {{\n"
                                    f"    font-family: \"{bold_family}\";\n"
                                    "    font-size: 12px;\n"
                                    "    color: black;\n"
                                    "    text-align: center;\n"
                                    "    margin: 0;\n"
                                    "}}")
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_14.addWidget(self.label_14)
        self.lbl_price = QtWidgets.QLabel(self.widget_15)
        self.lbl_price.setStyleSheet("QLabel {\n"
                                     "    font-family: \"Arial\", sans-serif;\n"
                                     "    font-size: 12px;\n"
                                     "    color: gray;\n"
                                     "    text-align: center;\n"
                                     "    margin: 0;\n"
                                     "}")
        self.lbl_price.setText("")
        self.lbl_price.setObjectName("lbl_price")
        self.horizontalLayout_14.addWidget(self.lbl_price)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.led_price = QtWidgets.QLineEdit(self.widget_15)
        self.led_price.setStyleSheet("QLineEdit {\n"
                                     "    background-color: #F5F5F5;\n"
                                     "    border: 1px solid #E0E0E0;\n"
                                     "    border-radius: 8px;\n"
                                     "    padding: 5px 10px;\n"
                                     "    font-family: \"Arial\", sans-serif;\n"
                                     "    font-size: 12px;\n"
                                     "    color: #333333;\n"
                                     "}\n"
                                     "QLineEdit:focus {\n"
                                     "    border: 1px solid #BDBDBD;\n"
                                     "    outline: none;\n"
                                     "}")
        self.led_price.setObjectName("led_price")
        self.verticalLayout_7.addWidget(self.led_price)
        self.gridLayout_4.addWidget(self.widget_15, 3, 0, 1, 1)
        self.widget_16 = QtWidgets.QWidget(self.singleScrapeMainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.widget_16.setSizePolicy(sizePolicy)
        self.widget_16.setObjectName("widget_16")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_16)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.lbl_url = QtWidgets.QLabel(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.lbl_url.setSizePolicy(sizePolicy)
        self.lbl_url.setStyleSheet(f"QLabel {{\n"
                                   f"    font-family: \"{bold_family}\";\n"
                                   "    font-size: 12px;\n"
                                   "    color: black;\n"
                                   "    text-align: center;\n"
                                   "    margin: 0;\n"
                                   "}}")
        self.lbl_url.setObjectName("lbl_url")
        self.horizontalLayout_15.addWidget(self.lbl_url)
        self.label_17 = QtWidgets.QLabel(self.widget_16)
        self.label_17.setStyleSheet("QLabel {\n"
                                    "    font-family: \"Arial\", sans-serif;\n"
                                    "    font-size: 12px;\n"
                                    "    color: gray;\n"
                                    "    text-align: center;\n"
                                    "    margin: 0;\n"
                                    "}")
        self.label_17.setText("")
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_15.addWidget(self.label_17)
        self.verticalLayout_8.addLayout(self.horizontalLayout_15)
        self.led_url = QtWidgets.QLineEdit(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.led_url.setSizePolicy(sizePolicy)
        self.led_url.setStyleSheet("QLineEdit {\n"
                                   "    background-color: #F5F5F5;\n"
                                   "    border: 1px solid #E0E0E0;\n"
                                   "    border-radius: 8px;\n"
                                   "    padding: 5px 10px;\n"
                                   "    font-family: \"Arial\", sans-serif;\n"
                                   "    font-size: 12px;\n"
                                   "    color: #333333;\n"
                                   "}\n"
                                   "QLineEdit:focus {\n"
                                   "    border: 1px solid #BDBDBD;\n"
                                   "    outline: none;\n"
                                   "}")
        self.led_url.setText("")
        self.led_url.setObjectName("led_url")
        self.verticalLayout_8.addWidget(self.led_url)
        self.gridLayout_4.addWidget(self.widget_16, 1, 0, 1, 1)
        self.gridLayout_6.addWidget(self.singleScrapeMainWidget, 0, 0, 1, 1)
        self.horizontalLayout_16.addWidget(self.frm_mid_mid)
        self.horizontalLayout_16.setStretch(1, 10)
        self.frm_mid_right = QtWidgets.QFrame(self.frm_mid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.frm_mid_right.setSizePolicy(sizePolicy)
        self.frm_mid_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_mid_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_mid_right.setObjectName("frm_mid_right")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frm_mid_right)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(20, 221, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.widget_3 = QtWidgets.QWidget(self.frm_mid_right)
        self.widget_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setStyleSheet("background-color: rgb(254,254,254);")
        self.widget.setObjectName("widget")
        self.widget.setFixedSize(200, 40)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_ss_app = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.lbl_ss_app.setSizePolicy(sizePolicy)
        self.lbl_ss_app.setStyleSheet("QLabel {\n"
                                      "    font-family: \"Arial\", sans-serif;\n"
                                      "    font-size: 12px;\n"
                                      "    font-weight: bold;\n"
                                      "    color: black;\n"
                                      "    text-align: center;\n"
                                      "    margin: 0;\n"
                                      "}")
        self.lbl_ss_app.setScaledContents(False)
        self.lbl_ss_app.setObjectName("lbl_ss_app")
        self.horizontalLayout.addWidget(self.lbl_ss_app)
        self.btn_use_ss_app = QtWidgets.QPushButton(self.widget)
        self.btn_use_ss_app.setStyleSheet("QPushButton {\n"
                                          "    background-color: #0066FF;\n"
                                          "    color: white;\n"
                                          "    border: none;\n"
                                          "    border-radius: 5px;\n"
                                          "    padding: 5px 5px;\n"
                                          "    font-family: \"Arial\", sans-serif;\n"
                                          "    font-size: 14px;\n"
                                          "    font-weight: bold;\n"
                                          "    text-align: center;\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: #0056E0;\n"
                                          "}\n"
                                          "QPushButton:pressed {\n"
                                          "    background-color: #0040B0;\n"
                                          "}")
        self.btn_use_ss_app.setObjectName("btn_use_ss_app")
        self.btn_use_ss_app.setFixedSize(85, 27)
        self.horizontalLayout.addWidget(self.btn_use_ss_app, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.widget_3)
        self.widget_2.setStyleSheet("background-color: rgb(254,254,254);")
        self.widget_2.setObjectName("widget_2")
        self.widget_2.setFixedSize(200, 40)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_myhome_app = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.lbl_myhome_app.setSizePolicy(sizePolicy)
        self.lbl_myhome_app.setStyleSheet("QLabel {\n"
                                          "    font-family: \"Arial\", sans-serif;\n"
                                          "    font-size: 12px;\n"
                                          "    font-weight: bold;\n"
                                          "    color: black;\n"
                                          "    text-align: center;\n"
                                          "    margin: 0;\n"
                                          "}")
        self.lbl_myhome_app.setObjectName("lbl_myhome_app")
        self.horizontalLayout_2.addWidget(self.lbl_myhome_app)
        self.horizontalLayout_2.addStretch()
        self.btn_use_myhome_app = QtWidgets.QPushButton(self.widget_2)
        self.btn_use_myhome_app.setStyleSheet("QPushButton {\n"
                                              "    background-color: #28A745;\n"
                                              "    color: white;\n"
                                              "    border: none;\n"
                                              "    border-radius: 5px;\n"
                                              "    padding: 5px 5px;\n"
                                              "    font-family: \"Arial\", sans-serif;\n"
                                              "    font-size: 14px;\n"
                                              "    font-weight: bold;\n"
                                              "    text-align: center;\n"
                                              "}\n"
                                              "QPushButton:hover {\n"
                                              "    background-color: #218838;\n"
                                              "}\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: #1E7E34;\n"
                                              "}")
        self.btn_use_myhome_app.setObjectName("btn_use_myhome_app")
        self.btn_use_myhome_app.setFixedSize(85, 27)
        self.horizontalLayout_2.addWidget(self.btn_use_myhome_app)
        self.verticalLayout.addWidget(self.widget_2)
        self.verticalLayout_2.addWidget(self.widget_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 222, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_16.addWidget(self.frm_mid_right)
        self.horizontalLayout_16.setStretch(2, 1)
        self.gridLayout_7.addWidget(self.frm_mid, 1, 0, 1, 1)
        self.frm_bot = QtWidgets.QFrame(self.singleuploadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.frm_bot.setSizePolicy(sizePolicy)
        self.frm_bot.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_bot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_bot.setObjectName("frm_bot")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frm_bot)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.wdt_xlx_btn_container = QtWidgets.QWidget(self.frm_bot)
        self.wdt_xlx_btn_container.setObjectName("wdt_xlx_btn_container")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.wdt_xlx_btn_container)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_open_excel = QtWidgets.QPushButton(self.wdt_xlx_btn_container)
        self.btn_open_excel.setStyleSheet("QPushButton {\n"
                                          "    background-color: #e6f5e6;\n"
                                          "    border: 2px solid #a2d4a2;\n"
                                          "    border-radius: 15px;\n"
                                          "    padding: 5px 10px;\n"
                                          "    font-size: 14px;\n"
                                          "    font-family: Arial, sans-serif;\n"
                                          "    color: #333333;\n"
                                          "    text-align: left;\n"
                                          "}\n"
                                          "QPushButton::icon {\n"
                                          "    padding-left: 10px;\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: #d9f2d9;\n"
                                          "    border-color: #8cc98c;\n"
                                          "}\n"
                                          "QPushButton:pressed {\n"
                                          "    background-color: #c4e3c4;\n"
                                          "    border-color: #6fbf6f;\n"
                                          "}")
        self.btn_open_excel.setObjectName("btn_open_excel")
        self.gridLayout_3.addWidget(self.btn_open_excel, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.wdt_xlx_btn_container)
        spacerItem7 = QtWidgets.QSpacerItem(908, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.lbl_status_icon = QtWidgets.QLabel(self.frm_bot)
        self.lbl_status_icon.setFixedSize(QtCore.QSize(24, 24))
        self.lbl_status_icon.setScaledContents(True)
        self.horizontalLayout_3.addWidget(self.lbl_status_icon)
        self.progressBar = QtWidgets.QProgressBar(self.frm_bot)
        self.progressBar.setFixedSize(QtCore.QSize(120, 15))
        self.progressBar.setRange(0, 0)
        self.progressBar.setVisible(False)
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.lbl_status = QtWidgets.QLabel(self.frm_bot)
        self.lbl_status.setObjectName("lbl_status")
        self.lbl_status.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.horizontalLayout_3.addWidget(self.lbl_status)
        self.gridLayout_7.addWidget(self.frm_bot, 2, 0, 1, 1)
        self.stackedWidget.addWidget(self.singleuploadPage)
        self.myhomeprofilePage = QtWidgets.QWidget()
        self.myhomeprofilePage.setObjectName("myhomeprofilePage")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.myhomeprofilePage)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.widget_9 = QtWidgets.QWidget(self.myhomeprofilePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget_9.setSizePolicy(sizePolicy)
        self.widget_9.setStyleSheet("background-color: #f5f5f5;")
        self.widget_9.setObjectName("widget_9")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.widget_9)
        self.gridLayout_11.setObjectName("gridLayout_11")
        spacerItem8 = QtWidgets.QSpacerItem(20, 151, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem8, 0, 2, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(320, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem9, 1, 0, 1, 1)
        self.myhome_container = QtWidgets.QGridLayout()
        self.myhome_container.setContentsMargins(50, 50, 50, 50)
        self.myhome_container.setSpacing(20)
        self.myhome_container.setObjectName("myhome_container")
        self.lbl_myhome_logo = QtWidgets.QLabel(self.widget_9)
        self.lbl_myhome_logo.setStyleSheet("QLabel {\n"
                                           "    font-family: \"Arial\", sans-serif;\n"
                                           "    font-size: 20px;\n"
                                           "    font-weight: bold;\n"
                                           "    color: black;\n"
                                           "    text-align: center;\n"
                                           "    margin: 0;\n"
                                           "}")
        self.lbl_myhome_logo.setText("")
        self.lbl_myhome_logo.setPixmap(QtGui.QPixmap(resource_path("app/static/images/myhome_transparent.png")))
        self.lbl_myhome_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_myhome_logo.setObjectName("lbl_myhome_logo")
        self.myhome_container.addWidget(self.lbl_myhome_logo, 0, 0, 1, 2)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.myhome_container.addItem(spacerItem10, 5, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.myhome_container.addItem(spacerItem11, 2, 1, 1, 1)
        self.led_myhome_password = QtWidgets.QLineEdit(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.led_myhome_password.setSizePolicy(sizePolicy)
        self.led_myhome_password.setStyleSheet("QLineEdit {\n"
                                               "    background-color: #F5F5F5;\n"
                                               "    border: 1px solid #E0E0E0;\n"
                                               "    border-radius: 8px;\n"
                                               "    padding: 5px 10px;\n"
                                               "    font-family: \"Arial\", sans-serif;\n"
                                               "    font-size: 12px;\n"
                                               "    color: #333333;\n"
                                               "}\n"
                                               "QLineEdit:focus {\n"
                                               "    border: 1px solid #BDBDBD;\n"
                                               "    outline: none;\n"
                                               "}")
        self.led_myhome_password.setObjectName("led_myhome_password")
        self.led_myhome_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.myhome_container.addWidget(self.led_myhome_password, 7, 0, 1, 2)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.myhome_container.addItem(spacerItem12, 10, 0, 1, 1)
        self.lbl_myhome_password = QtWidgets.QLabel(self.widget_9)
        self.lbl_myhome_password.setStyleSheet(f"QLabel {{\n"
                                               f"    font-family: \"{bold_family}\";\n"
                                               "    font-size: 12px;\n"
                                               "    color: black;\n"
                                               "    text-align: center;\n"
                                               "    margin: 0;\n"
                                               "}}")
        self.lbl_myhome_password.setObjectName("lbl_myhome_password")
        self.myhome_container.addWidget(self.lbl_myhome_password, 5, 0, 1, 1)
        self.lbl_myhome_user_2 = QtWidgets.QLabel(self.widget_9)
        self.lbl_myhome_user_2.setStyleSheet(f"QLabel {{\n"
                                             f"    font-family: \"{bold_family}\";\n"
                                             "    font-size: 12px;\n"
                                             "    color: black;\n"
                                             "    text-align: center;\n"
                                             "    margin: 0;\n"
                                             "}}")
        self.lbl_myhome_user_2.setObjectName("lbl_myhome_user_2")
        self.myhome_container.addWidget(self.lbl_myhome_user_2, 2, 0, 1, 1)
        self.led_myhome_user = QtWidgets.QLineEdit(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.led_myhome_user.setSizePolicy(sizePolicy)
        self.led_myhome_user.setStyleSheet("QLineEdit {\n"
                                           "    background-color: #F5F5F5;\n"
                                           "    border: 1px solid #E0E0E0;\n"
                                           "    border-radius: 8px;\n"
                                           "    padding: 5px 10px;\n"
                                           "    font-family: \"Arial\", sans-serif;\n"
                                           "    font-size: 12px;\n"
                                           "    color: #333333;\n"
                                           "}\n"
                                           "QLineEdit:focus {\n"
                                           "    border: 1px solid #BDBDBD;\n"
                                           "    outline: none;\n"
                                           "}")
        self.led_myhome_user.setObjectName("led_myhome_user")
        self.myhome_container.addWidget(self.led_myhome_user, 3, 0, 1, 2)
        self.btn_cancel_myhome_profile = QtWidgets.QPushButton(self.widget_9)
        self.btn_cancel_myhome_profile.setFixedSize(QtCore.QSize(100, 27))
        self.btn_cancel_myhome_profile.setStyleSheet("QPushButton {\n"
                                                     "    background-color: grey;\n"
                                                     "    color: white;\n"
                                                     "    border: none;\n"
                                                     "    border-radius: 5px;\n"
                                                     "    padding: 5px 15px;\n"
                                                     "    font-family: \"{bold_family}\";\n"
                                                     "    font-size: 11px;\n"
                                                     "    font-weight: bold;\n"
                                                     "    text-align: center;\n"
                                                     "}\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #5f5f5f;\n"
                                                     "}\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #404040;\n"
                                                     "}")
        self.btn_cancel_myhome_profile.setObjectName("btn_cancel_myhome_profile")
        self.myhome_container.addWidget(self.btn_cancel_myhome_profile, 10, 0, 1, 1)
        self.btn_save_myhome_profile = QtWidgets.QPushButton(self.widget_9)
        self.btn_save_myhome_profile.setStyleSheet("QPushButton {\n"
                                                   "    background-color: #28A745;\n"
                                                   "    color: white;\n"
                                                   "    border: none;\n"
                                                   "    border-radius: 5px;\n"
                                                   "    padding: 5px 15px;\n"
                                                   "    font-family: \"{bold_family}\";\n"
                                                   "    font-size: 14px;\n"
                                                   "    font-weight: bold;\n"
                                                   "    text-align: center;\n"
                                                   "}\n"
                                                   "QPushButton:hover {\n"
                                                   "    background-color: #218838;\n"
                                                   "}\n"
                                                   "QPushButton:pressed {\n"
                                                   "    background-color: #1E7E34;\n"
                                                   "}")
        self.btn_save_myhome_profile.setObjectName("btn_save_myhome_profile")
        self.myhome_container.addWidget(self.btn_save_myhome_profile, 10, 1, 1, 1)
        self.lbl_myhome_name = QtWidgets.QLabel(self.widget_9)
        self.lbl_myhome_name.setStyleSheet(f"QLabel {{\n"
                                           f"    font-family: \"{bold_family}\";\n"
                                           "    font-size: 12px;\n"
                                           "    color: black;\n"
                                           "    text-align: center;\n"
                                           "    margin: 0;\n"
                                           "}}")
        self.lbl_myhome_name.setObjectName("lbl_myhome_name")
        self.myhome_container.addWidget(self.lbl_myhome_name, 8, 0, 1, 1)
        self.led_myhome_name = QtWidgets.QLineEdit(self.widget_9)
        self.led_myhome_name.setStyleSheet("QLineEdit {\n"
                                           "    background-color: #F5F5F5;\n"
                                           "    border: 1px solid #E0E0E0;\n"
                                           "    border-radius: 8px;\n"
                                           "    padding: 5px 10px;\n"
                                           "    font-family: \"Arial\", sans-serif;\n"
                                           "    font-size: 12px;\n"
                                           "    color: #333333;\n"
                                           "}\n"
                                           "QLineEdit:focus {\n"
                                           "    border: 1px solid #BDBDBD;\n"
                                           "    outline: none;\n"
                                           "}")
        self.led_myhome_name.setObjectName("led_myhome_name")
        self.myhome_container.addWidget(self.led_myhome_name, 9, 0, 1, 2)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.myhome_container.addItem(spacerItem13, 8, 1, 1, 1)
        self.gridLayout_11.addLayout(self.myhome_container, 1, 1, 2, 2)
        spacerItem14 = QtWidgets.QSpacerItem(319, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem14, 2, 3, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(20, 151, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem15, 3, 1, 1, 1)
        self.gridLayout_9.addWidget(self.widget_9, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.myhomeprofilePage)
        self.ssgeprofilePage = QtWidgets.QWidget()
        self.ssgeprofilePage.setObjectName("ssgeprofilePage")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.ssgeprofilePage)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.widget_12 = QtWidgets.QWidget(self.ssgeprofilePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget_12.setSizePolicy(sizePolicy)
        self.widget_12.setStyleSheet("background-color: #f5f5f5;")
        self.widget_12.setObjectName("widget_12")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.widget_12)
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem16 = QtWidgets.QSpacerItem(20, 196, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem16, 0, 2, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(320, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem17, 1, 0, 1, 1)
        self.ssge_container = QtWidgets.QGridLayout()
        self.ssge_container.setContentsMargins(50, 50, 50, 50)
        self.ssge_container.setSpacing(20)
        self.ssge_container.setObjectName("ssge_container")
        self.btn_cancel_ssge_profile = QtWidgets.QPushButton(self.widget_12)
        self.btn_cancel_ssge_profile.setFixedSize(QtCore.QSize(100, 27))
        self.btn_cancel_ssge_profile.setStyleSheet("QPushButton {\n"
                                                   "    background-color: grey;\n"
                                                   "    color: white;\n"
                                                   "    border: none;\n"
                                                   "    border-radius: 5px;\n"
                                                   "    padding: 5px 15px;\n"
                                                   "    font-family: \"Arial\", sans-serif;\n"
                                                   "    font-size: 11px;\n"
                                                   "    font-weight: bold;\n"
                                                   "    text-align: center;\n"
                                                   "}\n"
                                                   "QPushButton:hover {\n"
                                                   "    background-color: #5f5f5f;\n"
                                                   "}\n"
                                                   "QPushButton:pressed {\n"
                                                   "    background-color: #404040;\n"
                                                   "}")
        self.btn_cancel_ssge_profile.setObjectName("btn_cancel_ssge_profile")
        self.ssge_container.addWidget(self.btn_cancel_ssge_profile, 10, 0, 1, 1)
        self.btn_save_ssge_profile = QtWidgets.QPushButton(self.widget_12)
        self.btn_save_ssge_profile.setStyleSheet("QPushButton {\n"
                                                 "    background-color: #28A745;\n"
                                                 "    color: white;\n"
                                                 "    border: none;\n"
                                                 "    border-radius: 5px;\n"
                                                 "    padding: 5px 15px;\n"
                                                 "    font-family: \"Arial\", sans-serif;\n"
                                                 "    font-size: 14px;\n"
                                                 "    font-weight: bold;\n"
                                                 "    text-align: center;\n"
                                                 "}\n"
                                                 "QPushButton:hover {\n"
                                                 "    background-color: #218838;\n"
                                                 "}\n"
                                                 "QPushButton:pressed {\n"
                                                 "    background-color: #1E7E34;\n"
                                                 "}")
        self.btn_save_ssge_profile.setObjectName("btn_save_ssge_profile")
        self.ssge_container.addWidget(self.btn_save_ssge_profile, 10, 1, 1, 1)
        self.led_ssge_password = QtWidgets.QLineEdit(self.widget_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.led_ssge_password.setSizePolicy(sizePolicy)
        self.led_ssge_password.setStyleSheet("QLineEdit {\n"
                                             "    background-color: #F5F5F5;\n"
                                             "    border: 1px solid #E0E0E0;\n"
                                             "    border-radius: 8px;\n"
                                             "    padding: 5px 10px;\n"
                                             "    font-family: \"Arial\", sans-serif;\n"
                                             "    font-size: 12px;\n"
                                             "    color: #333333;\n"
                                             "}\n"
                                             "QLineEdit:focus {\n"
                                             "    border: 1px solid #BDBDBD;\n"
                                             "    outline: none;\n"
                                             "}")
        self.led_ssge_password.setObjectName("led_ssge_password")
        self.led_ssge_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ssge_container.addWidget(self.led_ssge_password, 7, 0, 1, 2)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ssge_container.addItem(spacerItem18, 8, 1, 1, 1)
        self.lbl_ssge_password = QtWidgets.QLabel(self.widget_12)
        self.lbl_ssge_password.setStyleSheet(f"QLabel {{\n"
                                             f"    font-family: \"{bold_family}\";\n"
                                             "    font-size: 12px;\n"
                                             "    color: black;\n"
                                             "    text-align: center;\n"
                                             "    margin: 0;\n"
                                             "}}")
        self.lbl_ssge_password.setObjectName("lbl_ssge_password")
        self.ssge_container.addWidget(self.lbl_ssge_password, 5, 0, 1, 1)
        self.led_ssge_user = QtWidgets.QLineEdit(self.widget_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.led_ssge_user.setSizePolicy(sizePolicy)
        self.led_ssge_user.setStyleSheet("QLineEdit {\n"
                                         "    background-color: #F5F5F5;\n"
                                         "    border: 1px solid #E0E0E0;\n"
                                         "    border-radius: 8px;\n"
                                         "    padding: 5px 10px;\n"
                                         "    font-family: \"Arial\", sans-serif;\n"
                                         "    font-size: 12px;\n"
                                         "    color: #333333;\n"
                                         "}\n"
                                         "QLineEdit:focus {\n"
                                         "    border: 1px solid #BDBDBD;\n"
                                         "    outline: none;\n"
                                         "}")
        self.led_ssge_user.setObjectName("led_ssge_user")
        self.ssge_container.addWidget(self.led_ssge_user, 3, 0, 1, 2)
        self.lbl_ssge_logo = QtWidgets.QLabel(self.widget_12)
        self.lbl_ssge_logo.setStyleSheet("QLabel {\n"
                                         "    font-family: \"Arial\", sans-serif;\n"
                                         "    font-size: 20px;\n"
                                         "    font-weight: bold;\n"
                                         "    color: black;\n"
                                         "    text-align: center;\n"
                                         "    margin: 0;\n"
                                         "}")
        self.lbl_ssge_logo.setText("")
        self.lbl_ssge_logo.setPixmap(QtGui.QPixmap(resource_path("app/static/images/ssge_transparent.png")))
        self.lbl_ssge_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_ssge_logo.setObjectName("lbl_ssge_logo")
        self.ssge_container.addWidget(self.lbl_ssge_logo, 0, 0, 1, 2)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ssge_container.addItem(spacerItem19, 5, 1, 1, 1)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ssge_container.addItem(spacerItem20, 10, 0, 1, 1)
        self.lbl_ssge_user = QtWidgets.QLabel(self.widget_12)
        self.lbl_ssge_user.setStyleSheet(f"QLabel {{\n"
                                         f"    font-family: \"{bold_family}\";\n"
                                         "    font-size: 12px;\n"
                                         "    color: black;\n"
                                         "    text-align: center;\n"
                                         "    margin: 0;\n"
                                         "}}")
        self.lbl_ssge_user.setObjectName("lbl_ssge_user")
        self.ssge_container.addWidget(self.lbl_ssge_user, 2, 0, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ssge_container.addItem(spacerItem21, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_12)
        self.label.setStyleSheet(f"QLabel {{\n"
                                 f"    font-family: \"{bold_family}\";\n"
                                 "    font-size: 12px;\n"
                                 "    color: black;\n"
                                 "    text-align: center;\n"
                                 "    margin: 0;\n"
                                 "}}")
        self.label.setObjectName("label")
        self.ssge_container.addWidget(self.label, 8, 0, 1, 1)
        self.led_ssge_name = QtWidgets.QLineEdit(self.widget_12)
        self.led_ssge_name.setStyleSheet("QLineEdit {\n"
                                         "    background-color: #F5F5F5;\n"
                                         "    border: 1px solid #E0E0E0;\n"
                                         "    border-radius: 8px;\n"
                                         "    padding: 5px 10px;\n"
                                         "    font-family: \"Arial\", sans-serif;\n"
                                         "    font-size: 12px;\n"
                                         "    color: #333333;\n"
                                         "}\n"
                                         "QLineEdit:focus {\n"
                                         "    border: 1px solid #BDBDBD;\n"
                                         "    outline: none;\n"
                                         "}")
        self.led_ssge_name.setObjectName("led_ssge_name")
        self.ssge_container.addWidget(self.led_ssge_name, 9, 0, 1, 2)
        self.gridLayout_12.addLayout(self.ssge_container, 1, 1, 2, 2)
        spacerItem22 = QtWidgets.QSpacerItem(319, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem22, 2, 3, 1, 1)
        spacerItem23 = QtWidgets.QSpacerItem(20, 195, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem23, 3, 1, 1, 1)
        self.gridLayout_14.addWidget(self.widget_12, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.ssgeprofilePage)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.use_ss_app = False
        self.use_myhome_app = False
        self.btn_use_ss_app.clicked.connect(self.toggle_ss_app)
        self.btn_use_myhome_app.clicked.connect(self.toggle_myhome_app)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Estage"))
        self.lbl_estage_geo.setText(_translate("Form", "ისთეიჯი"))
        self.lbl_estage_eng.setText(_translate("Form", "ESTAGE"))
        self.lbl_ss_user.setText(_translate("Form", "SS.GE USER"))
        self.lbl_ss_email.setText(_translate("Form", "whateverwhatever@mail.com"))
        self.btn_change_ss_profile.setText(_translate("Form", "შეცვლა"))
        self.lbl_myhome_user.setText(_translate("Form", "MYHOME USER"))
        self.lbl_myhome_email.setText(_translate("Form", "whateverwhatever@mail.com"))
        self.btn_change_myhome_profile.setText(_translate("Form", "შეცვლა"))
        self.lbl_currency.setText(_translate("Form", "აირჩიე ვალუტა"))
        self.btn_usd.setText(_translate("Form", "USD"))
        self.btn_gel.setText(_translate("Form", "GEL"))
        self.lbl_desc_off.setText(_translate("Form", "არა"))
        self.lbl_desc_on.setText(_translate("Form", "კი"))
        self.lbl_desc.setText(_translate("Form", "აიტვირთოს აღწერა?"))
        self.label_10.setText(_translate("Form", "კომენტარი"))
        self.ted_comment.setPlaceholderText(_translate("Form", "type comment here"))
        self.lbl_single_upload.setText(_translate("Form", "ერთეული ატვირთვა"))
        self.btn_upload.setText(_translate("Form", "ატვირთე"))
        self.label_14.setText(_translate("Form", "ფასი"))
        self.led_price.setPlaceholderText(_translate("Form", "type price here"))
        self.lbl_url.setText(_translate("Form", "სახლის ბმული"))
        self.led_url.setPlaceholderText(_translate("Form", "type url here"))
        self.lbl_ss_app.setText(_translate("Form", "SS.GE APP"))
        self.btn_use_ss_app.setText(_translate("Form", "გამოყენება"))
        self.lbl_myhome_app.setText(_translate("Form", "MYHOME APP"))
        self.btn_use_myhome_app.setText(_translate("Form", "გამოყენება"))
        self.btn_open_excel.setText(_translate("Form", "ექსელის ნახვა"))
        self.lbl_status_icon.setText(_translate("Form", ""))
        self.lbl_status.setText(_translate("Form", ""))
        self.lbl_myhome_password.setText(_translate("Form", "შენი MYHOME (PASSWORD)"))
        self.lbl_myhome_user_2.setText(_translate("Form", "შენი MYHOME (USERNAME)"))
        self.btn_cancel_myhome_profile.setText(_translate("Form", "დაბრუნება"))
        self.btn_save_myhome_profile.setText(_translate("Form", "დაადასტურე"))
        self.lbl_myhome_name.setText(_translate("Form", "სახელი"))
        self.btn_cancel_ssge_profile.setText(_translate("Form", "დაბრუნება"))
        self.btn_save_ssge_profile.setText(_translate("Form", "დაადასტურე"))
        self.lbl_ssge_password.setText(_translate("Form", "შენი SS.Gე (PASSWORD)"))
        self.lbl_ssge_user.setText(_translate("Form", "შენი SS.Gე (USERNAME)"))
        self.label.setText(_translate("Form", "სახელი"))
        self.load_config_emails()
        self.btn_save_myhome_profile.clicked.connect(self.save_myhome_profile)
        self.btn_cancel_myhome_profile.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_save_ssge_profile.clicked.connect(self.save_ssge_profile)
        self.btn_cancel_ssge_profile.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_change_ss_profile.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_change_myhome_profile.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_upload.clicked.connect(self.on_upload_clicked)
        self.btn_open_excel.clicked.connect(self.open_excel_file)
        Form.setTabOrder(self.led_myhome_user, self.led_myhome_password)
        Form.setTabOrder(self.led_myhome_password, self.led_myhome_name)
        Form.setTabOrder(self.led_myhome_name, self.btn_save_myhome_profile)
        Form.setTabOrder(self.led_url, self.btn_usd)
        Form.setTabOrder(self.btn_usd, self.btn_gel)
        Form.setTabOrder(self.btn_gel, self.led_price)
        Form.setTabOrder(self.led_price, self.ted_comment)
        Form.setTabOrder(self.ted_comment, self.btn_upload)
        Form.setTabOrder(self.led_ssge_user, self.led_ssge_password)
        Form.setTabOrder(self.led_ssge_password, self.led_ssge_name)
        Form.setTabOrder(self.led_ssge_name, self.btn_save_ssge_profile)

    def load_config_emails(self):
        try:
            config_path = os.path.join(get_base_dir(), "confidential", "config.json")
            if not os.path.exists(config_path):
                return
            with open(config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)
            ss_email = config_data.get("SSGE", {}).get("email") or "No Email Found"
            myhome_email = config_data.get("MyHome", {}).get("email") or "No Email Found"
            self.lbl_ss_email.setText(ss_email)
            self.lbl_myhome_email.setText(myhome_email)
        except Exception:
            pass

    def save_myhome_profile(self):
        try:
            config_path = os.path.join(get_base_dir(), "confidential", "config.json")
            if not os.path.exists(config_path):
                return
            myhome_user = self.led_myhome_user.text().strip()
            myhome_password = self.led_myhome_password.text().strip()
            estage_name = self.led_myhome_name.text().strip()
            if not self.is_valid_email(myhome_user):
                QMessageBox.warning(None, "Invalid Email", "Please enter a valid email address for MyHome.")
                return
            if not estage_name:
                QMessageBox.warning(None, "Invalid Name", "Name field cannot be empty.")
                return
            with open(config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)
            config_data["MyHome"]["email"] = myhome_user
            config_data["MyHome"]["password"] = myhome_password
            config_data["Estage"]["name"] = estage_name
            with open(config_path, "w", encoding="utf-8") as file:
                json.dump(config_data, file, indent=4, ensure_ascii=False)
            self.load_config_emails()
            self.stackedWidget.setCurrentIndex(0)
        except Exception:
            pass

    def save_ssge_profile(self):
        try:
            config_path = os.path.join(get_base_dir(), "confidential", "config.json")
            if not os.path.exists(config_path):
                return
            ssge_user = self.led_ssge_user.text().strip()
            ssge_password = self.led_ssge_password.text().strip()
            estage_name = self.led_ssge_name.text().strip()
            if not self.is_valid_email(ssge_user):
                QMessageBox.warning(None, "Invalid Email", "Please enter a valid email address for SSGE.")
                return
            if not estage_name:
                QMessageBox.warning(None, "Invalid Name", "Name field cannot be empty.")
                return
            with open(config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)
            config_data["SSGE"]["email"] = ssge_user
            config_data["SSGE"]["password"] = ssge_password
            config_data["Estage"]["name"] = estage_name
            with open(config_path, "w", encoding="utf-8") as file:
                json.dump(config_data, file, indent=4, ensure_ascii=False)
            self.load_config_emails()
            self.stackedWidget.setCurrentIndex(0)
        except Exception:
            pass

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    def open_excel_file(self):
        try:
            excel_path = os.path.join(get_base_dir(), "data", "realestate.xlsx")
            os.startfile(excel_path)
        except Exception:
            pass

    def on_upload_clicked(self):
        if hasattr(self, 'worker') and self.worker is not None and self.worker.isRunning():
            return
        self.btn_upload.setEnabled(False)
        self.url = self.led_url.text().strip()
        if self.btn_usd.isChecked():
            self.currency = "$"
        elif self.btn_gel.isChecked():
            self.currency = "₾"
        else:
            self.currency = "$"
        self.agency_price = self.led_price.text().strip()
        self.comment = self.ted_comment.toPlainText().strip()
        self.upload_description = self.wdg_switch.isChecked()
        if not self.url:
            self.lbl_status.setText("მიუთითეთ ბმული")
            self.lbl_status.setStyleSheet("QLabel { font-family: 'Arial'; font-size: 14px; color: red; background-color: #F8D7DA; border-radius: 8px; padding: 4px; }")
            self.lbl_status_icon.setPixmap(QtGui.QPixmap(resource_path("app/static/images/error_icon.png")))
            self.progressBar.setVisible(False)
            self.btn_upload.setEnabled(True)
            return
        if "ss" not in self.url.lower() and "myhome" not in self.url.lower():
            self.lbl_status.setText("მიუთითეთ სწორი ბმული")
            self.lbl_status.setStyleSheet("QLabel { font-family: 'Arial'; font-size: 14px; color: red; background-color: #F8D7DA; border-radius: 8px; padding: 4px; }")
            self.lbl_status_icon.setPixmap(QtGui.QPixmap(resource_path("app/static/images/error_icon.png")))
            self.progressBar.setVisible(False)
            self.btn_upload.setEnabled(True)
            return
        if not self.agency_price:
            QMessageBox.warning(None, "Input Error", "Please enter the agency price.")
            self.btn_upload.setEnabled(True)
            return
        self.lbl_status.setText("დაიწყო ატვირთვის პროცესი")
        self.lbl_status.setStyleSheet("QLabel { font-family: 'Arial'; font-size: 14px; color: black; background-color: #FFF3CD; border-radius: 8px; padding: 4px; }")
        self.lbl_status_icon.setPixmap(QtGui.QPixmap(resource_path("app/static/images/hourglass.png")))
        self.progressBar.setVisible(True)
        self.worker = UploadWorker(
            url=self.url,
            currency=self.currency,
            agency_price=self.agency_price,
            comment=self.comment,
            upload_description=self.upload_description,
            run_myhome=(not self.use_ss_app),
            run_ss=(not self.use_myhome_app)
        )
        self.worker.error_flag = False
        self.worker.errorOccurred.connect(self.on_worker_error_wrapper)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_error_wrapper(self, err):
        self.worker.error_flag = True
        self.on_worker_error(err)

    def on_worker_finished(self):
        if self.worker.error_flag:
            return
        self.lbl_status.setText("წარმატებით აიტვირთა")
        self.lbl_status.setStyleSheet("QLabel { font-family: 'Arial'; font-size: 14px; color: white; background-color: #28a745; border-radius: 8px; padding: 4px; }")
        self.lbl_status_icon.setPixmap(QtGui.QPixmap(resource_path("app/static/images/success_icon.png")))
        self.progressBar.setVisible(False)
        QtCore.QTimer.singleShot(5000, self.clear_snackbar)
        self.btn_upload.setEnabled(True)

    def clear_snackbar(self):
        self.lbl_status.setText("")
        self.lbl_status.setStyleSheet("")
        self.lbl_status_icon.clear()

    def on_worker_error(self, err):
        self.lbl_status.setText("დაფიქსირდა შეცდომა")
        self.lbl_status.setStyleSheet("QLabel { font-family: 'Arial'; font-size: 14px; color: white; background-color: #dc3545; border-radius: 8px; padding: 4px; }")
        self.lbl_status_icon.setPixmap(QtGui.QPixmap(resource_path("app/static/images/error_icon.png")))
        self.progressBar.setVisible(False)
        QtCore.QTimer.singleShot(5000, self.clear_snackbar)
        self.btn_upload.setEnabled(True)

    def toggle_ss_app(self):
        if not self.use_ss_app:
            self.use_ss_app = True
            if self.use_myhome_app:
                self.use_myhome_app = False
                self.lbl_single_upload.setText("ერთეული ატვირთვა")
                self.lbl_myhome_app.setText("MYHOME APP")
                self.lbl_myhome_app.setStyleSheet("QLabel { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; color: black; text-align: center; margin: 0; }")
                self.btn_use_myhome_app.setStyleSheet("QPushButton {\n"
                                                      "    background-color: #28A745;\n"
                                                      "    color: white;\n"
                                                      "    border: none;\n"
                                                      "    border-radius: 5px;\n"
                                                      "    padding: 5px 5px;\n"
                                                      "    font-family: Arial, sans-serif;\n"
                                                      "    font-size: 14px;\n"
                                                      "    font-weight: bold;\n"
                                                      "    text-align: center;\n"
                                                      "}\n"
                                                      "QPushButton:hover {\n"
                                                      "    background-color: #218838;\n"
                                                      "}\n"
                                                      "QPushButton:pressed {\n"
                                                      "    background-color: #1E7E34;\n"
                                                      "}")
            self.lbl_single_upload.setText("ერთეული ატვირთვა (SS.Gე)")
            self.lbl_ss_app.setText("ორივე")
            self.lbl_ss_app.setStyleSheet("QLabel { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: black; text-align: center; margin: 0; }")
            self.btn_use_ss_app.setStyleSheet("QPushButton {\n"
                                              "    background-color: grey;\n"
                                              "    color: white;\n"
                                              "    border: none;\n"
                                              "    border-radius: 5px;\n"
                                              "    padding: 5px 5px;\n"
                                              "    font-family: Arial, sans-serif;\n"
                                              "    font-size: 14px;\n"
                                              "    font-weight: bold;\n"
                                              "    text-align: center;\n"
                                              "}\n"
                                              "QPushButton:hover {\n"
                                              "    background-color: darkgrey;\n"
                                              "}\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: dimgray;\n"
                                              "}")
        else:
            self.use_ss_app = False
            self.lbl_single_upload.setText("ერთეული ატვირთვა")
            self.lbl_ss_app.setText("SS.GE APP")
            self.lbl_ss_app.setStyleSheet("QLabel { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; color: black; text-align: center; margin: 0; }")
            self.btn_use_ss_app.setStyleSheet("QPushButton {\n"
                                              "    background-color: #0066FF;\n"
                                              "    color: white;\n"
                                              "    border: none;\n"
                                              "    border-radius: 5px;\n"
                                              "    padding: 5px 5px;\n"
                                              "    font-family: Arial, sans-serif;\n"
                                              "    font-size: 14px;\n"
                                              "    font-weight: bold;\n"
                                              "    text-align: center;\n"
                                              "}\n"
                                              "QPushButton:hover {\n"
                                              "    background-color: #0056E0;\n"
                                              "}\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: #0040B0;\n"
                                              "}")

    def toggle_myhome_app(self):
        if not self.use_myhome_app:
            self.use_myhome_app = True
            if self.use_ss_app:
                self.use_ss_app = False
                self.lbl_single_upload.setText("ერთეული ატვირთვა")
                self.lbl_ss_app.setText("SS.GE APP")
                self.lbl_ss_app.setStyleSheet("QLabel { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; color: black; text-align: center; margin: 0; }")
                self.btn_use_ss_app.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #0066FF;\n"
                                                  "    color: white;\n"
                                                  "    border: none;\n"
                                                  "    border-radius: 5px;\n"
                                                  "    padding: 5px 5px;\n"
                                                  "    font-family: Arial, sans-serif;\n"
                                                  "    font-size: 14px;\n"
                                                  "    font-weight: bold;\n"
                                                  "    text-align: center;\n"
                                                  "}\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #0056E0;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #0040B0;\n"
                                                  "}")
            self.lbl_single_upload.setText("ერთეული ატვირთვა (MYHOME)")
            self.lbl_myhome_app.setText("ორივე")
            self.lbl_myhome_app.setStyleSheet("QLabel { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: black; text-align: center; margin: 0; }")
            self.btn_use_myhome_app.setStyleSheet("QPushButton {\n"
                                                  "    background-color: grey;\n"
                                                  "    color: white;\n"
                                                  "    border: none;\n"
                                                  "    border-radius: 5px;\n"
                                                  "    padding: 5px 5px;\n"
                                                  "    font-family: Arial, sans-serif;\n"
                                                  "    font-size: 14px;\n"
                                                  "    font-weight: bold;\n"
                                                  "    text-align: center;\n"
                                                  "}\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: darkgrey;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: dimgray;\n"
                                                  "}")
        else:
            self.use_myhome_app = False
            self.lbl_single_upload.setText("ერთეული ატვირთვა")
            self.lbl_myhome_app.setText("MYHOME APP")
            self.lbl_myhome_app.setStyleSheet("QLabel { font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; color: black; text-align: center; margin: 0; }")
            self.btn_use_myhome_app.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #28A745;\n"
                                                  "    color: white;\n"
                                                  "    border: none;\n"
                                                  "    border-radius: 5px;\n"
                                                  "    padding: 5px 5px;\n"
                                                  "    font-family: Arial, sans-serif;\n"
                                                  "    font-size: 14px;\n"
                                                  "    font-weight: bold;\n"
                                                  "    text-align: center;\n"
                                                  "}\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #218838;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #1E7E34;\n"
                                                  "}")

def initialize_app_files():
    base_dir = get_base_dir()
    data_folder = os.path.join(base_dir, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    excel_file = os.path.join(data_folder, "realestate.xlsx")
    if not os.path.exists(excel_file):
        try:
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "RealEstate Data"
            columns = [
                "Uploaded Timestamp",
                "მესაქვს(ID)",
                "ტელეფონის ნომერი",
                "რაიონი",
                "ოთახი",
                "სართული",
                "მისამართი",
                "სააგენტოს ფასი",
                "მესაკუთრის ფასი",
                "Comment",
                "ss.ge",
                "myhome.ge"
            ]
            ws.append(columns)
            wb.save(excel_file)
        except ImportError:
            with open(excel_file, "w", encoding="utf-8") as f:
                f.write("")
    logs_folder = os.path.join(base_dir, "logs")
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    confidential_folder = os.path.join(base_dir, "confidential")
    if not os.path.exists(confidential_folder):
        os.makedirs(confidential_folder)
    config_file = os.path.join(confidential_folder, "config.json")
    if not os.path.exists(config_file):
        default_config = {
            "MyHome": {
                "email": "",
                "password": "",
                "name": ""
            },
            "SSGE": {
                "email": "",
                "password": "",
                "name": ""
            },
            "Estage": {
                "name": ""
            }
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    initialize_app_files()
    app = QtWidgets.QApplication(sys.argv)
    icon_path = resource_path("app/static/images/logo.ico")
    app.setWindowIcon(QtGui.QIcon(icon_path))
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
