from socket_client_server.socket_client_server import Sock_Client
import os

SERVER_ADDRESS = os.getenv("WIFI_CONF_SOCKET", '/var/run/wifi_conf/wifi_conf.socket')

def start_access_point(ssid):
    """Switch wifi to access point mode.

    `ssid`:   Name of wifi to be spawned.
    """
    sock_client = Sock_Client(SERVER_ADDRESS, timeout_in_sec=20)

    # Construct message
    data = {
        "action": "configure_access_point",
        "data": {
            "ssid": ssid
        }
    }

    answer = sock_client.send(data)
    if answer["status"] != 0:
        raise Exception(answer["message"])
    return

def stop_access_point():
    """
    Swicht back to wifi client mode from access point mode.

    """
    sock_client = Sock_Client(SERVER_ADDRESS, timeout_in_sec=20)

    # Construct message
    data = {
        "action": "unconfigure_access_point",
    }

    answer = sock_client.send(data)
    if answer["status"] != 0:
        raise Exception(answer["message"])
    return

def set_wifi_ssid_and_password(ssid, password):
    """Set ssid and password for wifi 
    client mode during access point mode.

    `ssid`: SSID of wifi network to be joined in client mode.

    `password`:   Password for wifi network to be joined in client mode.
    """
    sock_client = Sock_Client(SERVER_ADDRESS, timeout_in_sec=20)

    # Construct message
    data = {
        "action": "set_wifi_ssid_and_password",
        "data": {
            "ssid": ssid,
            "password": password
        }
    }

    answer = sock_client.send(data)
    if answer["status"] != 0:
        raise Exception(answer["message"])
    return