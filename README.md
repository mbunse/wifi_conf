# Wifi conf service

This python package provides a daemon that can be used to setup an access point for headless wifi configuration.

## Installation

The package requires [`hostapd`](https://en.wikipedia.org/wiki/Hostapd) and [`dnsmasq`](https://en.wikipedia.org/wiki/Dnsmasq) to be installed.

```console
sudo apt-get install hostapd
sudo apt-get install dnsmasq

sudo pip install wifi_conf

sudo install_wifi_conf
```

The status of the daemon can be checked with

```sh
sudo systemctl status wifi_conf
```

## Usage

```python
import wifi_conf
from wifi_conf import wifi_conf_client

# configure device as access point
# Access point has ssid `test`
wifi_conf_client.start_access_point(ssid="test")

# Wait some time to see effect
time.sleep(20)

# Set wifi password
wifi_conf_client.set_wifi_ssid_and_password('Wifi_ssid', 'password')

# switch back to wifi client mode
wifi_conf_client.stop_access_point()
```

## Testing

```bash
sudo python3 -m unittest test/wifi_conf_test.py
```

## Security

Currently, the `wifi_conf` user is added to the sudo group to be able to start and stop services connected to setting up an access point. For other solution see https://serverfault.com/questions/841099/systemd-grant-an-unprivileged-user-permission-to-alter-one-specific-service.
