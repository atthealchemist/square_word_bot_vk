import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QThreadPool

from bot import Bot
from worker import Worker


class WordBotWindow(QMainWindow):

    def __ui_stubs(self):
        self.Form_BotWindow = QWidget()
        self.layoutWidget = QWidget()
        self.splitter_Login = QSplitter()
        self.label_Login = QLabel()
        self.lineEdit_Login = QLineEdit()
        self.splitter_Password = QSplitter()
        self.label_Password = QLabel()
        self.lineEdit_Password = QLineEdit()
        self.splitter_ChatNumber = QSplitter()
        self.label_ChatNumber = QLabel()
        self.spinBox_ChatNumber = QSpinBox()
        self.checkBox_IsUser = QCheckBox()
        self.layoutWidget = QWidget()
        self.pushButton_Exit = QPushButton()
        self.label_Status = QLabel()
        self.pushButton_Toggle = QPushButton()
        raise AssertionError("This should never be called")

    # region Slots

    def setStatus(self, text):
        self.label_Status.setStyleSheet('color: green')
        self.label_Status.setText(text)

    def error(self):
        self.label_Status.setStyleSheet('color: red')
        self.label_Status.setText("Error! Bot can't be started!")

    def stop(self):
        self.label_Status.setText("Bot is stopped!")

    def __StartBot(self):
        self.bot.setCredentials(self.lineEdit_Login.text(), self.label_Password.text())
        self.bot.start()
        self.bot.setVkId(self.spinBox_ChatNumber.value(), self.checkBox_IsUser.isChecked())

    def onBotStart(self, checked):
        botWorker = Worker(self.__StartBot)

        botWorker.signals.start.connect(self.setStatus)
        botWorker.signals.error.connect(self.error)
        botWorker.signals.stop.connect(self.stop)

        if checked:
            self.pushButton_Toggle.setText("Stop")
            self.threadPool.start(botWorker)
        else:
            self.pushButton_Toggle.setText("Start")


    # endregion

    # region Initialization

    def __setConnections(self):
        self.pushButton_Exit.clicked.connect(self.Form_BotWindow.close)
        self.pushButton_Toggle.toggled[bool].connect(self.onBotStart)

    def __setComponents(self):
        self.Form_BotWindow.setWindowTitle("Word Bot for VK (now with UI!)")
        self.pushButton_Toggle.setCheckable(True)

    # endregion

    def __init__(self, parent=None):
        super(WordBotWindow, self).__init__(parent)
        loadUi("./ui/word_bot_window.ui", self)

        self.threadPool = QThreadPool()
        self.bot = Bot()

        self.__setComponents()
        self.__setConnections()
