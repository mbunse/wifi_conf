import os
import subprocess
import re
import shutil
class Wifi_Conf:
    def __init__(self, config_file="/etc/wpa_supplicant/wpa_supplicant.conf"):
        self.__config_file = config_file
        self.conf_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    def get_path_for_file(self, filename):
        return os.path.join(self.conf_dir, filename)

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

    def configure_access_point(self):
        if os.path.isfile("/etc/dnsmasq.conf.kids_phone_orig"):
            raise FileExistsError("/etc/dnsmasq.conf.kids_phone_orig exists. Run Wifi_Conf.unconfigure_access_point() first.")
        if os.path.isfile("/etc/dhcpcd.conf.kids_phone_orig"):
            raise FileExistsError("/etc/dhcpcd.conf.kids_phone_orig exists. Run Wifi_Conf.unconfigure_access_point() first.")
        if os.path.isfile("/etc/default/hostapd.kids_phone_orig"):
            raise FileExistsError("/etc/default/hostapd.kids_phone_orig exists. Run Wifi_Conf.unconfigure_access_point() first.")
        os.rename("/etc/dnsmasq.conf", "/etc/dnsmasq.conf.kids_phone_orig")
        shutil.copy("/etc/dhcpcd.conf", "/etc/dhcpcd.conf.kids_phone_orig")
        os.rename("/etc/default/hostapd", "/etc/default/hostapd.kids_phone_orig")
        shutil.copy(self.get_path_for_file("dnsmasq.conf"),
                    "/etc/dnsmasq.conf")
        shutil.copy(self.get_path_for_file("hostapd"),
                    "/etc/default/hostapd")
        shutil.copy(self.get_path_for_file("hostapd.conf"),
                    "/etc/hostapd/hostapd.conf")
                    

        dhcp_add = "interface wlan0\n" + \
                   "static ip_address=192.168.4.1/24\n"
        with open("/etc/dhcpcd.conf", "a") as f:
            f.write(dhcp_add)
        subprocess.call(['sudo', 'ifconfig', 'wlan0', 'down'])
        subprocess.call(['sudo', 'wpa_cli', 'terminate'])
        subprocess.call(['sudo', 'systemctl', 'enable', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'restart', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'enable', 'dnsmasq'])
        subprocess.call(['sudo', 'systemctl', 'restart', 'dnsmasq'])
        subprocess.call(['sudo', 'systemctl', 'restart', 'dhcpcd'])
        subprocess.call(['ifconfig', 'wlan0', '192.168.4.1', 'netmask', '255.255.255.0', 'up'])
        return

    def unconfigure_access_point(self):
        if not os.path.isfile("/etc/dnsmasq.conf.kids_phone_orig"):
            raise FileNotFoundError("/etc/dnsmasq.conf.kids_phone_orig does not exist. Run Wifi_Conf.configure_access_point() first.")
        if not os.path.isfile("/etc/dhcpcd.conf.kids_phone_orig"):
            raise FileNotFoundError("/etc/dhcpcd.conf.kids_phone_orig  does not exist. Run Wifi_Conf.configure_access_point() first.")
        if not os.path.isfile("/etc/default/hostapd.kids_phone_orig"):
            raise FileNotFoundError("/etc/default/hostapd.kids_phone_orig  does not exist. Run Wifi_Conf.configure_access_point() first.")
        subprocess.call(['sudo', 'systemctl', 'stop', 'dhcpcd'])
        subprocess.call(['sudo', 'systemctl', 'stop', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'disable', 'hostapd'])
        subprocess.call(['sudo', 'systemctl', 'stop', 'dnsmasq'])
        subprocess.call(['sudo', 'systemctl', 'disable', 'dnsmasq'])
        subprocess.call(['sudo', 'wpa_supplicant', '-B', '-i', 'wlan0', '-c', self.__config_file])
        os.rename("/etc/dnsmasq.conf.kids_phone_orig", "/etc/dnsmasq.conf")
        os.rename("/etc/dhcpcd.conf.kids_phone_orig", "/etc/dhcpcd.conf")
        os.rename("/etc/default/hostapd.kids_phone_orig", "/etc/default/hostapd")
        os.remove("/etc/hostapd/hostapd.conf")
        subprocess.call(['sudo', 'systemctl', 'start', 'dhcpcd'])
        subprocess.call(['sudo', 'dhclient', '-v', 'wlan0'])



