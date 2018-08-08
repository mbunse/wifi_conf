#!/bin/bash

# create dedicated user
useradd -r -s /bin/false wifi_conf
# Grant access to sudo
# needed to set up wifi
adduser wifi_conf sudo

# set up service
cp -f wifi_conf.service /etc/systemd/system/wifi_conf.service
chmod ag+r /etc/systemd/system/wifi_conf.service

# Create dir for socket and assign to kids_phone user
mkdir -p /var/run/wifi_conf
chown -R wifi_conf:wifi_conf /var/run/wifi_conf
chmod g+w /var/run/wifi_conf

# reload units
systemctl daemon-reload

# enable services
systemctl enable wifi_conf
systemctl restart wifi_conf
