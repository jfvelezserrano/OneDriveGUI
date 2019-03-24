# OneDriveGUI (beta)

Simple Tray Icon for Abraunegg OneDrive Free Client.

![Screenshot](https://raw.githubusercontent.com/jfvelezserrano/OneDriveGUI/master/Screenshot.png)

This project tries to complement the OneDrive Free Client. It only simplifies the access to a little set of very basic operations that frequently you do with OneDrive Free Client from the CLI. From OneDriveGUI you can invoke:
- onedrive --synchronize --verbose -> Sync now
- onedrive --display-config -> Show settings
- systemctl start -> Start sync service
- systemctl stop -> Stop sync service
- systemctl status -> Show Log

Icon meaning:
![OneDrive Free Client is inactive](https://github.com/jfvelezserrano/OneDriveGUI/blob/master/gray_icon.png)
![OneDrive Free Client is synching](https://github.com/jfvelezserrano/OneDriveGUI/blob/master/red_icon.png)
![OneDrive Free Client daeamon is active and perhaps synching](https://github.com/jfvelezserrano/OneDriveGUI/blob/master/green_icon.png)
![OneDrive Free Client daeamon is active and perhaps synching, but there was errors in last synchronization](https://github.com/jfvelezserrano/OneDriveGUI/blob/master/green_icon.png)

## Project status

The proyect is in a very beta state. It only has been tested on:
- Ubuntu 16.04
- Kubuntu 18.04
- Neon 18.04

## General Setup

Install Abraunegg OneDrive Free Client (https://github.com/abraunegg/onedrive)

### On Ubuntu

sudo pip3 install PyQt5

sudo apt-get install xterm

clone https://github.com/jfvelezserrano/OneDriveGUI.git

cd OneDriveGUI
python3 OneDriveGUI.py

After 5 seconds the tray icon appears.
