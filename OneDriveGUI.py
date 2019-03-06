"""
    https://github.com/abraunegg/onedrive
"""

import sys
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread
import threading

class Sync(threading.Thread):
    """
    Realiza la operacion de sincronizado interactivo.
    """

    def __init__(self, widget, process, change_icon=False):
        threading.Thread.__init__(self)
        self.widget = widget
        self.process = process
        self.change_icon = change_icon

    def run(self):
        log_file = open("log.txt", "w")
        subprocess.call(self.process, stdout=log_file)
        if self.change_icon:
            self.widget.setIcon(QtGui.QIcon("gray_icon.png"))

class Show(threading.Thread):
    """
    Realiza la operacion de sincronizado interactivo.
    """

    def __init__(self, process):
        threading.Thread.__init__(self)
        self.process = process

    def run(self):
        subprocess.call(self.process)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    Interfaz grafica para onedrive
    """

    def __init__(self, app, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        sync_now_action = menu.addAction("Sync now")
        sync_now_action.triggered.connect(self._sync)
        start_sync_action = menu.addAction("Start sync service")
        start_sync_action.triggered.connect(self._start_service)
        stop_sync_action = menu.addAction("Stop sync service")
        stop_sync_action.triggered.connect(self._stop_service)
        show_log_action = menu.addAction("Show log")
        show_log_action.triggered.connect(self._show_log)
        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self._show_settings)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self._exit)
        self.setContextMenu(menu)

    def _sync(self):
        sync_thread = Sync(self,['onedrive', '--synchronize', '--verbose'], True)
        sync_thread.start()
        self.setIcon(QtGui.QIcon("red_icon.png"))

    def _start_service(self):
        self.setIcon(QtGui.QIcon("green_icon.png"))
        #sync_thread = Sync(self)
        #sync_thread.start()

    def _stop_service(self):
        self.setIcon(QtGui.QIcon("gray_icon.png"))
        #sync_thread = Sync(self)
        #sync_thread.start()

    def _show_log(self):
        show_thread = Show(['xterm', '-e', 'tail', '-f', 'log.txt'])
        show_thread.start()

    def _show_settings(self):
        show_thread = Show(['xterm', '-hold', '-e', 'onedrive', '--display-config'])
        show_thread.start()

    def _exit(self):
        exit()

def main():
    """
    Funcion principal.
    """
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(app, QtGui.QIcon("gray_icon.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
