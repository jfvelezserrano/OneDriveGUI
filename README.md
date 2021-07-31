# OneDriveGUI (beta)

Simple Tray Icon for Abraunegg OneDrive Free Client.

![Screenshot](https://raw.githubusercontent.com/jfvelezserrano/OneDriveGUI/master/Screenshot.png)

This project tries to complement the OneDrive Free Client. It only simplifies the access to a little set of very basic operations that frequently you do with OneDrive Free Client from the CLI. From OneDriveGUI you can invoke:
- onedrive --synchronize --verbose -> Sync now
- onedrive --display-config -> Show settings
- systemctl start -> Start sync service
- systemctl --user stop -> Stop sync service
- systemctl --user status -> Show Log
- systemctl --user disable onedrive -> Stop for ever

Icon meaning:

<img src="https://github.com/jfvelezserrano/OneDriveGUI/blob/master/gray_icon.png" width="48"> OneDrive Free Client is inactive

<img src="https://github.com/jfvelezserrano/OneDriveGUI/blob/master/red_icon.png" width="48"> OneDrive Free Client is synching

<img src="https://github.com/jfvelezserrano/OneDriveGUI/blob/master/green_icon.png" width="48"> OneDrive Free Client daeamon is active and perhaps synching

<img src="https://github.com/jfvelezserrano/OneDriveGUI/blob/master/yellow_icon.png" width="48"> OneDrive Free Client daeamon is active and perhaps synching, but there was errors in last synchronization

## Project status

The proyect is in a very beta state. It only has been tested on:
- Ubuntu 16.04
- Kubuntu 18.04
- Neon 18.04

## General Setup

Install Abraunegg OneDrive Free Client (https://github.com/abraunegg/onedrive)

### On Ubuntu

```sh
cd ~ 

sudo pip3 install PyQt5

sudo apt-get install xterm

git clone https://github.com/jfvelezserrano/OneDriveGUI.git

cd OneDriveGUI

python3 OneDriveGUI.py
```

After 5 seconds the tray icon appears.

To stop automatic synchronization run:

systemctl --user stop onedrive

You can add the script OneDriveGUI.sh at startup sequence.
