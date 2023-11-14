import socket
import threading
import subprocess

def while_true_try(f):
    def wrap(*args, **kwargs):
        while True:
            try: return f(*args, **kwargs)
            except: ...
    return wrap

def get_msg(handle: socket.socket) -> str:
    data_len = int.from_bytes(handle.recv(4), "little")
    data = handle.recv(data_len)
    return data.decode()

def send_msg(handle: socket.socket, text: str):
    data = text.encode()
    data_len = len(data)
    handle.send(data_len.to_bytes(4, 'little'))
    handle.send(data)

def get_ip() -> str:
    terminal_out = subprocess.check_output(["ifconfig"]).decode()
    wlan_section = terminal_out[terminal_out.find("wlan0:"):]
    ip_section = wlan_section[wlan_section.find("inet "):]
    address = ip_section[5:ip_section[5:].find(" ")]
    return address

@while_true_try
def handle_client(handle: socket.socket):
    while True:
        msg = get_msg(handle)
        if msg == "IP":
            send_msg(handle, get_ip())

if __name__ == "__main__": print(get_ip)