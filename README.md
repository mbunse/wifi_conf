# Wifi conf service

This python package allows to


## Installation

The package requires [`hostapd`](https://en.wikipedia.org/wiki/Hostapd) and [`dnsmasq`](https://en.wikipedia.org/wiki/Dnsmasq) to be installed.

```bash
sudo apt-get install hostapd
sudo apt-get install dnsmasq
sudo systemctl daemon-reload
```

## Usage

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

## Testing

```bash
sudo python3 -m unittest test/wifi_conf_test.py
```

## Security

Currently, the `wifi_conf` user is added to the sudo group to be able to start and stop services connected to setting up an access point. For other solution see https://serverfault.com/questions/841099/systemd-grant-an-unprivileged-user-permission-to-alter-one-specific-service.
