import os
import subprocess
import re

class Wifi_Conf:
    def __init__(self, config_file):
        self.__config_file = config_file
    def set_wifi_ssid_and_password(self, ssid, password):
        ret = subprocess.check_output(['wpa_passphrase',ssid ,password])
        with open(self.__config_file, "r+") as f:
            conf = "".join(f.readlines())

        new_conf = re.sub('network={.*?}', ret.decode(), conf, flags=re.DOTALL)
        with open(self.__config_file, "w") as f:
           f.write(new_conf)
            
        return
    def reconfigure(self):
        subprocess.call(['wpa_cli', '-i', 'wlan0', 'reconfigure'])
        return


