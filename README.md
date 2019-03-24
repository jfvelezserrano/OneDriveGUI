# OneDriveGUI (beta)

Simple Tray Icon for Abraunegg OneDrive Free Client.

This project tries to complement the OneDrive Free Client. It only simplifies the access to a little set of very basic operations that frequently you do with OneDrive Free Client from the CLI. From OneDriveGUI you can invoke:
- onedrive --synchronize --verbose -> Sync now
- onedrive --display-config -> Show settings
- systemctl start -> Start sync service
- systemctl stop -> Stop sync service
- systemctl status -> Show Log

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
