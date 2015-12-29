# encoding: utf-8
__author__ = 'mFoxRU'

import sys

from PyQt4.QtGui import QApplication

from mainwindow import App


if __name__ == '__main__':
    app = QApplication(sys.argv)
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    user = sys.argv[2] if len(sys.argv) > 2 else ''
    passw = sys.argv[3] if len(sys.argv) > 3 else ''

    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor

    gui = App(reactor, url, user, passw)
    gui.show()
    reactor.run()

    # Temporary fix
    import os
    os._exit(0)
