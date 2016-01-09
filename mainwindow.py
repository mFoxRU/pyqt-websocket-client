# encoding: utf-8
__author__ = 'mFoxRU'

import os.path
from base64 import standard_b64encode as encode

from PyQt4 import QtCore, QtGui, uic
from autobahn.twisted.websocket import connectWS
from twisted.internet import ssl

from protocol import Factory


class App(QtGui.QMainWindow):
    def __init__(self, reactor, url='', user='', passw=''):
        super(App, self).__init__()
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__), 'main.ui'), self)

        self.reactor = reactor
        self.factory = Factory(callback=self.log_line)

        # Connect section
        self.ui.button_connect.clicked.connect(self.ws_connect)
        self.ui.button_disconnect.clicked.connect(self.factory.disconnect)
        self.ui.checkbox_auth.stateChanged.connect(
                self.ui.input_login.setEnabled)
        self.ui.checkbox_auth.stateChanged.connect(
                self.ui.input_password.setEnabled)
        self.ui.input_msg.returnPressed.connect(
                self.ui.button_send.click)
        self.ui.button_send.clicked.connect(self.send_msg)
        self.ui.output_log.customContextMenuRequested.connect(
                self.log_context_menu)

        # Mix
        self.ui.input_url.setText(url)
        self.ui.input_login.setText(user)
        self.ui.input_password.setText(passw)
        if user:
            self.ui.checkbox_auth.setChecked(True)
        if user and not passw:
            self.ui.input_password.setFocus()
        else:
            self.ui.button_connect.setFocus()

    @QtCore.pyqtSlot()
    def ws_connect(self):
        self.factory.disconnect()

        headers = {}
        if self.ui.checkbox_auth.isChecked():
            username = str(self.ui.input_login.text())
            password = str(self.ui.input_password.text())
            auth = ' '.join(['Basic',
                             encode(':'.join([username, password]))])
            headers['Authorization'] = auth

        address = str(self.ui.input_url.text())
        context = None
        if address.startswith('wss://'):
            context = ssl.ClientContextFactory()

        try:
            self.factory.setSessionParameters(url=address, headers=headers)
            self.log_line('Connecting...')
            connectWS(self.factory, context, timeout=5)
        except Exception as e:
            self.log_line(e.message)

    @QtCore.pyqtSlot()
    def send_msg(self):
        msg = str(self.ui.input_msg.text())
        self.factory.send_msg(msg)
        self.ui.input_msg.clear()

    @QtCore.pyqtSlot(QtCore.QPoint)
    def log_context_menu(self, point):
        menu = self.ui.output_log.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction('Clear All', self.ui.output_log.clear)
        menu.exec_(self.ui.output_log.mapToGlobal(point))
        del menu

    def log_line(self, msg):
        self.ui.output_log.insertPlainText(str(msg))
        self.ui.output_log.insertPlainText('\n')

    def closeEvent(self, *args, **kwargs):
        if self.reactor.threadpool is not None:
            self.reactor.threadpool.stop()
        self.reactor.stop()
