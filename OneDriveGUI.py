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

    def __init__(self, widget, process, set_buttons_function):
        threading.Thread.__init__(self)
        self.widget = widget
        self.process = process
        self.set_buttons_function = set_buttons_function

    def run(self):
        log_file = open("log.txt", "w")
        subprocess.call(self.process, stdout=log_file)
        self.set_buttons_function()

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
        self._sync_now_action = menu.addAction("Sync now")
        self._sync_now_action.triggered.connect(self._sync)
        self._start_sync_action = menu.addAction("Start sync service")
        self._start_sync_action.triggered.connect(self._start_service)
        self._stop_sync_action = menu.addAction("Stop sync service")
        self._stop_sync_action.triggered.connect(self._stop_service)
        self._show_log_action = menu.addAction("Show log")
        self._show_log_action.triggered.connect(self._show_log)
        self._settings_action = menu.addAction("Settings")
        self._settings_action.triggered.connect(self._show_settings)
        self._exit_action = menu.addAction("Exit")
        self._exit_action.triggered.connect(self._exit)
        self.setContextMenu(menu)
        self.setToolTip("OneDrive GUI")

    def _sync(self):
        sync_thread = Sync(self,['onedrive', '--synchronize', '--verbose'], self.inactive)
        self._sync_now_action.setEnabled(False)
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

    def inactive(self):
        self._sync_now_action.setEnabled(True)

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
