from unittest.mock import patch, call
import unittest
import wifi_conf.wifi_conf
import filecmp
from os import path, rename, remove
from shutil import copyfile
import re

class Test_Wifi_Conf(unittest.TestCase):
    def setUp(self):
        self.path = path.dirname(__file__)
        self.data_path = path.join(path.dirname(__file__),"..", "data")
        copyfile(path.join(self.data_path, "wpa_supplicant.conf"), path.join(self.path, "wpa_supplicant.conf"))
        self.wificonf = wifi_conf.Wifi_Conf(config_file=path.join(self.path, "wpa_supplicant.conf"))

    def test_set_wifi_password_and_ssid(self):
        self.wificonf.set_wifi_ssid_and_password('Wifi_ssid', 'password')
        self.assertTrue(filecmp.cmp(path.join(self.path, "wpa_supplicant.conf"), 
                                    path.join(self.path, "wpa_supplicant.test"),
                                    shallow=False),
                        "wpa_supplicant.conf not as expected")

    def tearDown(self):
        remove(path.join(self.path, "wpa_supplicant.conf"))

    @patch("subprocess.call", autospec=True)
    def test_reconfigure(self, mock):
        self.wificonf.reconfigure()
        # Check that subprocess.call has been called with the following parameters
        mock.assert_has_calls([call(['wpa_cli', '-i', 'wlan0', 'reconfigure'])])

        
class Test_Access_Point(unittest.TestCase):
    def setUp(self):
        self.path = path.dirname(__file__)
        self.data_path = path.join(path.dirname(__file__),"..", "data")
        self.wificonf = wifi_conf.Wifi_Conf()
        if path.isfile("/etc/dnsmasq.conf"):
            copyfile("/etc/dnsmasq.conf", "/etc/dnsmasq.conf.orig")
        if path.isfile(" /etc/default/hostapd"):
            copyfile(" /etc/default/hostapd", "/etc/default/hostapd")

    def tearDown(self):
        if path.isfile("/etc/dnsmasq.conf.orig"):
            rename("/etc/dnsmasq.conf.orig", "/etc/dnsmasq.conf")
        if path.isfile(" /etc/default/hostapd.orig"):
            rename(" /etc/default/hostapd.orig", "/etc/default/hostapd")
        pass

    @patch("subprocess.call", autospec=True)
    def test_set_up_access_point(self, mock):
        self.wificonf.configure_access_point()

        # Check that hostapd config files are updated
        self.assertTrue(filecmp.cmp(path.join("/etc/default/", "hostapd"),
                                    path.join(self.data_path, "hostapd"), shallow=False),
                        "/etc/default/hostapd not as expected")        
        self.assertTrue(filecmp.cmp(path.join("/etc/hostapd/", "hostapd.conf"),
                                    path.join(self.data_path, "hostapd.conf"), shallow=False),
                        "/etc/hostapd/hostapd.conf not as expected")

        # Check that dhcpcd config file is updated
        with open("/etc/dhcpcd.conf", "r") as f:
            conf = "".join(f.readlines())
            self.assertIn('interface wlan0\nstatic ip_address=192.168.4.1/24\n', conf)

        # Check that services are restarted
        mock.assert_has_calls([
                               call(['sudo', 'ifconfig', 'wlan0', 'down']),
                               call(['sudo', 'wpa_cli', 'terminate']), 
                               call(['sudo', 'systemctl', 'enable', 'hostapd']),
                               call(['sudo', 'systemctl', 'restart', 'hostapd']),
                               call(['sudo', 'systemctl', 'enable', 'dnsmasq']),
                               call(['sudo', 'systemctl', 'restart', 'dnsmasq']),
                               call(['sudo', 'systemctl', 'restart', 'dhcpcd']),
                               call(['ifconfig', 'wlan0', '192.168.4.1', 'netmask', '255.255.255.0', 'up'])
                              ])

        self.wificonf.unconfigure_access_point()

        # Check that hostapd config files are changed back
        self.assertFalse(filecmp.cmp(path.join("/etc/default/", "hostapd"),
                                    path.join(self.data_path, "hostapd"), shallow=False),
                        "/etc/default/hostapd not as expected")        
        self.assertFalse(path.isfile(path.join("/etc/hostapd/", "hostapd.conf")))

        # Check that dhcpcd config file is changed back
        with open("/etc/dhcpcd.conf", "r") as f:
            conf = "".join(f.readlines())
            self.assertNotIn('interface wlan0\nstatic ip_address=192.168.4.1/24\n', conf)

        # Check that services are stoped and disabled
        mock.assert_has_calls([
                               call(['sudo', 'systemctl', 'stop', 'dhcpcd']),
                               call(['sudo', 'systemctl', 'stop', 'hostapd']),
                               call(['sudo', 'systemctl', 'disable', 'hostapd']),
                               call(['sudo', 'systemctl', 'stop', 'dnsmasq']),
                               call(['sudo', 'systemctl', 'disable', 'dnsmasq']),
                               call(['sudo', 'wpa_supplicant', '-B', '-i', 'wlan0', '-c', '/etc/wpa_supplicant/wpa_supplicant.conf']),
                               call(['sudo', 'systemctl', 'start', 'dhcpcd']),
                               call(['sudo', 'dhclient', '-v', 'wlan0']),
                              ])

        # Check that hostapd conf has been removed
        self.assertFalse(path.isfile("/etc/hostapd/hostapd.conf"))

if __name__ == "__main__":
    unittest.main()
