from unittest.mock import patch, call
import unittest
import wifi_conf.wifi_conf
import filecmp
from os import path 
from shutil import copyfile


class Test_Wifi_Conf(unittest.TestCase):
    def setUp(self):
        self.path = path.dirname(__file__)
        copyfile(path.join(self.path, "wpa_supplicant.conf.orig"), path.join(self.path, "wpa_supplicant.conf"))
        self.wificonf = wifi_conf.Wifi_Conf(config_file=path.join(self.path, "wpa_supplicant.conf"))

    def test(self):
        self.wificonf.set_wifi_ssid_and_password('Wifi_ssid', 'password')
        self.assertTrue(filecmp.cmp(path.join(self.path, "wpa_supplicant.conf"), path.join(self.path, "wpa_supplicant.test"),shallow=False), "Configuration not as expected")

    def tearDown(self):
        pass    
    @patch("subprocess.call", autospec=True)
    def test2(self, mock):
        self.wificonf.reconfigure()
        # Check that subprocess.call has been called with the following parameters
        mock.assert_has_calls([call(['wpa_cli', '-i', 'wlan0', 'reconfigure'])])

if __name__ == "__main__":
    unittest.main()
