#!/bin/bash

systemctl disable wifi_conf
systemctl stop wifi_conf

# remove service
rm -f /etc/systemd/system/wifi_conf.service

# Remove socket dir
rm -rf /var/run/wifi_conf

# Remove binary dir
rm -rf /usr/bin/wifi_conf

# reload units
systemctl daemon-reload

# remove dedicated user
userdel wifi_conf
delgroup wifi_conf