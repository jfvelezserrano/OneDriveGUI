"""
    https://github.com/abraunegg/onedrive
"""

import sys
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
import threading
import getpass

class Sync(QtCore.QThread):
    """
    Realiza la operacion de sincronizado interactivo.
    """

    def __init__(self, parent, process, set_buttons_function, signal):
        QtCore.QThread.__init__(self, parent)
        self.process = process
        self.set_buttons_function = set_buttons_function
        self.signal = signal

    def run(self):
        log_file = open("log.txt", "w")
        subprocess.call(self.process, stdout=log_file)
        log_file.close()

        mensaje = ""
        with open("log.txt", "r") as file:
            mensaje += file.read()
        self.set_buttons_function()

        if (mensaje.find("Skipping uploading this new file as it exceeds the maximum size allowed")) or (mensaje.find("Giving up on sync after three attempts") >= 0):
            self.signal.emit()




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
    signal = QtCore.pyqtSignal()

    def __init__(self, app, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.system_username = getpass.getuser()
        self.parent = parent
        menu = QtWidgets.QMenu(parent)
        title = menu.addAction("OneDrive deamon")
        title.setEnabled(False)
 
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
        self._stop_sync_action.setEnabled(False)
        self.setContextMenu(menu)
        self._synching = False
        self._set_status()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._set_status)
        self.timer.start(120*1000)
        
    def _set_status(self):
        if not self._synching:
            message = subprocess.getoutput("systemctl status onedrive@" + self.system_username + ".service")

            if message.find("Active: inactive (dead)") > 0:
                self.inactive()
            elif (message.find("]: ERROR:") > 0) or (message.find("]: Skipping:") > 0):
                self.service_on(True)
            else:
                self.service_on()

    def _sync(self):
        self.signal.connect(self._error_message)
        sync_thread = Sync(self, ['onedrive', '--synchronize', '--verbose'], self.inactive, self.signal)
        self.setToolTip("OneDrive Service\nSynching")
        self._sync_now_action.setEnabled(False)
        self._synching = True        
        sync_thread.start()
        self.setIcon(QtGui.QIcon("red_icon.png"))

    def _error_message(self):
        QtWidgets.QMessageBox.critical(self.parent, "OneDrive Tray Icon", "Some errors occur during sync. Review log and resolve the errors.")

    def _start_service(self):
        subprocess.call(["systemctl", "start", "onedrive@" + self.system_username + ".service"])
        self._set_status()

    def _stop_service(self):
        subprocess.call(["systemctl", "stop", "onedrive@" + self.system_username + ".service"])
        self._set_status()

    def _show_log(self):
        if self.service_running:
            log_file = open("log.txt", "w")
            subprocess.call(["systemctl", "status", "onedrive@" + self.system_username + ".service"],stdout=log_file)

        show_thread = Show(['xterm', '-e', 'tail', '-f', '-n', '+0', 'log.txt'])
        show_thread.start()

    def _show_settings(self):
        show_thread = Show(['xterm', '-hold', '-e', 'onedrive', '--display-config'])
        show_thread.start()

    def inactive(self):
        self.setIcon(QtGui.QIcon("gray_icon.png"))
        self._sync_now_action.setEnabled(True)
        self._start_sync_action.setEnabled(True)
        self._stop_sync_action.setEnabled(False)
        self.service_running = False
        self._synching = False
        self.setToolTip("OneDrive Service\nInactive")
        

    def service_on(self, errors=False):
        if errors:
            self.setIcon(QtGui.QIcon("yellow_icon.png"))
            self.setToolTip("OneDrive Service\nActive\nErrors - See log")
        else:
            self.setIcon(QtGui.QIcon("green_icon.png"))
            self.setToolTip("OneDrive Service\nActive")
        self._sync_now_action.setEnabled(False)
        self._start_sync_action.setEnabled(False)
        self._stop_sync_action.setEnabled(True)
        self.service_running = True

    def _exit(self):
        exit()

def main():
    """
    Funcion principal.
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(app, QtGui.QIcon("gray_icon.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
