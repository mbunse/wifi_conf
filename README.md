Wifi conf service
=================

```
sudo apt-get install hostapd
sudo apt-get install dnsmasq
sudo systemctl daemon-reload
```

Usage
=====

```python
import wifi_conf

wificonf = wifi_conf.Wifi_Conf()

# configure device as access point
wificonf.configure_access_point()
# Access point has ssid `kids_phone`

# Set wifi password
wificonf.set_wifi_ssid_and_password('Wifi_ssid', 'password')

# switch back to wifi client mode
wificonf.unconfigure_access_point()

```
