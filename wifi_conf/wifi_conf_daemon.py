import os
from socket_client_server.socket_client_server import Sock_Server
from wifi_conf.wifi_conf import Wifi_Conf
import logging

class Wifi_Conf_Daemon():
    def __init__(self,
                 config_file="/etc/wpa_supplicant/wpa_supplicant.conf"):
        self.wifi_conf = Wifi_Conf(config_file)

        server_address = os.getenv("WIFI_CONF_SOCKET", './wifi_conf.sock')
        self.sock_server = Sock_Server(server_address, self.request_handler)
        self.sock_server.start()

    def request_handler(self, data):
        try:
            if data["action"] == "configure_access_point":
                ssid = data["data"]["ssid"]
                self.wifi_conf.configure_access_point(ssid)
                return None
            # TODO: request auth data
            elif data["action"] == "unconfigure_access_point":
                self.wifi_conf.unconfigure_access_point()
                return None
            elif data["action"] == "set_wifi_ssid_and_password":
                ssid = data["data"]["ssid"]
                password = data["data"]["password"]
                self.wifi_conf.set_wifi_ssid_and_password(ssid, password)
                return None
            elif data["action"] == "quit":
                self.quit()
                return None

        except KeyError:
            logging.error("missing key in message.")
        return None
    
    def quit(self):
        logging.info("exiting Wifi_Conf_Daemon")
        self.sock_server.quit()
        return  

def run_daemon():
    import time
    os.getenv("LOG_LEVEL", 'INFO')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    daemon = Wifi_Conf_Daemon()
    time.sleep(1)
    return

if __name__ == "__main__":
    import time
    os.getenv("LOG_LEVEL", 'INFO')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    daemon = Wifi_Conf_Daemon()
    time.sleep(1)

    import wifi_conf_client 
    wifi_conf_client.start_access_point(ssid="kids_phone")
    time.sleep(20)
    wifi_conf_client.stop_access_point()
    
    daemon.quit()
