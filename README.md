# OneDriveGUI

Simple Tray Icon for Abraunegg OneDrive Free Client.

Tested on:
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

To stop automatic synchronization run:

systemctl --user stop onedrive

You can add the script OneDriveGUI.sh at startup sequence.
