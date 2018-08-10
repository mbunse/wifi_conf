import os
import subprocess
import re
import shutil
import socket
import struct

from pkg_resources import resource_filename

class Wifi_Conf:
    def __init__(self, 
                 config_file="/etc/wpa_supplicant/wpa_supplicant.conf"):
        self.__config_file      = config_file
        self.conf_dir           = os.path.join(os.path.dirname(__file__), "..", "data")
        self.ip_address_cidr    = "192.168.4.1/24"

        self.ip_address, self.netmask = Wifi_Conf.cidr_to_netmask(self.ip_address_cidr)

    def get_path_for_file(self, filename):
        return resource_filename("wifi_conf", os.path.join("data", filename))

    def set_wifi_ssid_and_password(self, ssid, password):
        # https://www.cisco.com/c/en/us/td/docs/routers/access/wireless/software/guide/ServiceSetID.html
        # The SSID can consist of up to 32 alphanumeric, case-sensitive, characters.
        # The first character cannot be the !, #, or ; character.
        # The +, ], /, ", TAB, and trailing spaces are invalid characters for SSIDs.
        # https://regex101.com/r/ddZ9zc/17
        if re.fullmatch(r"^\w[\w!#;\- ]{0,30}[\w!#;\-]$|^\w$", ssid) == None:
            raise ValueError("SIID is not valid. Should be 32 alphanumeric string")
        if re.fullmatch(r"^[\w\W]{8-63}$", password, flags=re.ASCII) == None:
            raise ValueError("Password is not valid. Should be 8-63 character long ASCII string")
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

    #based on https://stackoverflow.com/questions/33750233/convert-cidr-to-subnet-mask-in-python
    @staticmethod
    def cidr_to_netmask(cidr):
        network, net_bits = cidr.split('/')
        host_bits = 32 - int(net_bits)
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return network, netmask

    def configure_access_point(self, ssid):
        if os.path.isfile("/etc/dnsmasq.conf.kids_phone_orig"):
            raise FileExistsError("/etc/dnsmasq.conf.kids_phone_orig exists. Run Wifi_Conf.unconfigure_access_point() first.")
        if os.path.isfile("/etc/default/hostapd.kids_phone_orig"):
            raise FileExistsError("/etc/default/hostapd.kids_phone_orig exists. Run Wifi_Conf.unconfigure_access_point() first.")

        os.rename("/etc/dnsmasq.conf", "/etc/dnsmasq.conf.kids_phone_orig")
        os.rename("/etc/default/hostapd", "/etc/default/hostapd.kids_phone_orig")

        try:            
            shutil.copy(self.get_path_for_file("dnsmasq.conf"),
                        "/etc/dnsmasq.conf")

            # Set SSID in hostapd configuration file
            with open(self.get_path_for_file("hostapd.conf"), "r") as hostapd_file:
                updated_hostapd_file_data = (hostapd_file.read()
                    .replace("ssid=kids_phone", "ssid={}".format(ssid)))

            with open(self.get_path_for_file("hostapd.conf"), "w") as hostapd_file:
                hostapd_file.write(updated_hostapd_file_data)

            shutil.copy(self.get_path_for_file("hostapd"),
                        "/etc/default/hostapd")
            shutil.copy(self.get_path_for_file("hostapd.conf"),
                        "/etc/hostapd/hostapd.conf")

        except Exception as err:
            os.rename("/etc/dnsmasq.conf.kids_phone_orig", "/etc/dnsmasq.conf")
            os.rename("/etc/default/hostapd.kids_phone_orig", "/etc/default/hostapd")
            if os.path.exists("/etc/hostapd/hostapd.conf"):
                os.remove("/etc/hostapd/hostapd.conf")
            raise err
        
        subprocess.call(['sudo', 'ifconfig', 'wlan0', 'down'])
        subprocess.call(['sudo', 'wpa_cli', 'terminate'])
        subprocess.call(['sudo', 'systemctl', 'enable', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'restart', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'enable', 'dnsmasq'])
        subprocess.call(['sudo', 'systemctl', 'restart', 'dnsmasq'])
        subprocess.call(['sudo', 'systemctl', 'stop', 'dhcpcd'])
        subprocess.call(['ifconfig', 'wlan0', self.ip_address, 'netmask', self.netmask, 'up'])
        return

    def unconfigure_access_point(self):
        if not os.path.isfile("/etc/dnsmasq.conf.kids_phone_orig"):
            raise FileNotFoundError("/etc/dnsmasq.conf.kids_phone_orig does not exist. Run Wifi_Conf.configure_access_point() first.")
        if not os.path.isfile("/etc/default/hostapd.kids_phone_orig"):
            raise FileNotFoundError("/etc/default/hostapd.kids_phone_orig  does not exist. Run Wifi_Conf.configure_access_point() first.")
        subprocess.call(['sudo', 'systemctl', 'stop', 'dhcpcd'])
        subprocess.call(['sudo', 'systemctl', 'stop', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'disable', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'stop', 'dnsmasq'])
        subprocess.call(['sudo', 'systemctl', 'disable', 'dnsmasq'])
        subprocess.call(['sudo', 'wpa_supplicant', '-B', '-i', 'wlan0', '-c', self.__config_file])
        os.rename("/etc/dnsmasq.conf.kids_phone_orig", "/etc/dnsmasq.conf")
        os.rename("/etc/default/hostapd.kids_phone_orig", "/etc/default/hostapd")
        os.remove("/etc/hostapd/hostapd.conf")
        subprocess.call(['sudo', 'systemctl', 'start', 'dhcpcd'])
        subprocess.call(['sudo', 'dhclient', '-v', 'wlan0'])



