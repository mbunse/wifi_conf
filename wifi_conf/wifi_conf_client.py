from socket_client_server.socket_client_server import Sock_Client
import os

SERVER_ADDRESS = os.getenv("WIFI_CONF_SOCKET", './wifi_conf.sock')

def start_access_point(ssid):
    sock_client = Sock_Client(SERVER_ADDRESS)

    # Construct message
    data = {
        "action": "configure_access_point",
        "data": {
            "ssid": ssid
        }
    }

    sock_client.send(data)
    return

def stop_access_point():
    sock_client = Sock_Client(SERVER_ADDRESS)

    # Construct message
    data = {
        "action": "unconfigure_access_point",
    }

    sock_client.send(data)
    return

def set_wifi_ssid_and_password(ssid, password):
    sock_client = Sock_Client(SERVER_ADDRESS)

    # Construct message
    data = {
        "action": "set_wifi_ssid_and_password",
        "data": {
            "ssid": ssid,
            "password": password
        }
    }

    sock_client.send(data)
    return