"""
Tray System Icon for Free One Drive Cliente of abraunegg
https://github.com/abraunegg/onedrive
"""

import sys
import subprocess
import threading
import getpass
import time
import re
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
#import debugpy

class Sync(QtCore.QThread):
    """
    Realiza la operacion de sincronizado interactivo.
    """

    def __init__(self, parent, process, inactive_signal, error_signal):
        QtCore.QThread.__init__(self, parent)
        self.process = process
        self.inactive_signal = inactive_signal
        self.error_signal = error_signal
        self.parent_widget = parent

    def run(self):
        """
        Launch a thread with a blocking process
        """
        #debugpy.debug_this_thread()
        log_file = open("log.txt", "w")
        subprocess.call(self.process, stdout=log_file, stderr=log_file)
        self.parent_widget.last_update = time.strftime("%b %d %H:%M:%S\n", time.localtime())
        log_file.write(self.parent_widget.last_update)
        log_file.close()

        mensaje = ""
        with open("log.txt", "r") as file:
            mensaje += file.read()
        self.inactive_signal.emit()

        if (mensaje.find("Skipping uploading this new file as it exceeds the maximum size allowed")>=0) \
            or (mensaje.find("Giving up on sync after three attempts") >= 0) \
            or (mensaje.find("\nERROR:") >= 0):
            self.error_signal.emit()


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

    error_signal = QtCore.pyqtSignal()
    inactive_signal = QtCore.pyqtSignal()

    def __init__(self, app, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

        self.system_username = getpass.getuser()
        self.service_enabled = False
        self.last_update = ""

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
            message = subprocess.getoutput('ps axj | grep "onedrive --[m]onitor"')
            if message != "":
                self.service_enabled = True
                self.service_on()
            else:
                message = subprocess.getoutput("systemctl status onedrive@" + self.system_username + ".service")
                
                reg_exp = '\\n([a-z]{3}\ [0-9]{2}\ [0-9]{2}:[0-9]{2}:[0-9]{2})'

                date_search = re.findall(reg_exp, message)

                if not date_search:
                    log = open("log.txt", "r")
                    log = log.read(-1)
                    date_search = re.findall(reg_exp, log)

                if date_search:
                    self.last_update = date_search[-1]

                if (message.find("]: ERROR:") > 0) or (message.find("\nERROR:") > 0) or (message.find("]: Skipping:") > 0):
                    self.service_enabled = True
                    self.service_on(True)
                elif message.find("@.service; disabled;") > 0 or (message.find("could not be found.") > 0):
                    self.service_enabled = False
                    self.inactive()
                elif message.find("Active: inactive (dead)") > 0:
                    self.service_enabled = True
                    self.inactive()
                else:
                    self.service_enabled = True
                    self.service_on()

    def _sync(self):
        self.error_signal.connect(self._error_message)
        self.inactive_signal.connect(self.inactive)
        sync_thread = Sync(self, ['onedrive', '--synchronize', '--verbose'], self.inactive_signal, self.error_signal)
        self.setToolTip("OneDrive Service\nSynching")
        self._sync_now_action.setEnabled(False)
        self._synching = True
        sync_thread.start()
        self.setIcon(QtGui.QIcon("red_icon.png"))

    def _error_message(self):
        self.service_on(True)
        if self.supportsMessages():
            self.showMessage("OneDrive Tray Icon", "Some errors occur during sync. Review log and resolve the errors.",icon = self.Critical)
        else:
            QtWidgets.QMessageBox.critical(self.parent, "OneDrive Tray Icon", "Some errors occur during sync. Review log and resolve the errors.")

    def _start_service(self):
        #subprocess.call(["systemctl", "start", "onedrive@" + self.system_username + ".service"])
        subprocess.call(["systemctl", "--user", "start", "onedrive"])
        self._set_status()

    def _stop_service(self):
        subprocess.call(["systemctl", "--user", "stop", "onedrive"])
        self._set_status()

    def _show_log(self):
        if self.service_running:
            log_file = open("log.txt", "w")
            #subprocess.call(["systemctl", "status", "onedrive@" + self.system_username + ".service"],stdout=log_file)
            subprocess.call(["systemctl", "--user", "status", "onedrive"],stdout=log_file)

        show_thread = Show(['xterm', '-e', 'tail', '-f', '-n', '+0', 'log.txt'])
        show_thread.start()

    def _show_settings(self):
        if self.service_enabled:
            message = "One Drive Service enabled - To disable it, execute in shell: systemctl disable onedrive@" + self.system_username + ".service\n"
        else:
            message = "One Drive Service disabled - To enable it, execute in shell: systemctl enable onedrive@" + self.system_username + ".service\n"

        message += subprocess.getoutput("onedrive --display-config")

        show_thread = Show(['xterm', '-hold', '-e', 'echo', message])
        show_thread.start()

    def inactive(self):
        self.setIcon(QtGui.QIcon("gray_icon.png"))

        if threading.currentThread().getName() == "MainThread":
            self._sync_now_action.setEnabled(True)

        self._stop_sync_action.setEnabled(False)
        if self.service_enabled:
            self._start_sync_action.setEnabled(False)
        else:
            self._start_sync_action.setEnabled(True)

        self.service_running = False
        self._synching = False
        message = "OneDrive Service Inactive"
        if self.last_update:
            message += "\nUpdated at " + self.last_update
        self.setToolTip(message)

    def service_on(self, errors=False):

        message = "OneDrive Service Active"
        if self.last_update:
            message += "\nUpdated at " + self.last_update
        if errors:
            self.setIcon(QtGui.QIcon("yellow_icon.png"))
            message += "\nRevise log to solve some problems"
        else:
            self.setIcon(QtGui.QIcon("green_icon.png"))
        self.setToolTip(message)
        self._start_sync_action.setToolTip("")
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

    time.sleep(5)

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    while not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
        time.sleep(5)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(app, QtGui.QIcon("gray_icon.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
