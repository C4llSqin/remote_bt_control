import socket
import threading
import subprocess
import uuid
import re

def while_true_try(f):
    def wrap(*args, **kwargs):
        while True:
            try: return f(*args, **kwargs)
            except: ...
    return wrap

def new_thread(f):
    def wrap(*args, **kwargs):
        thread = threading.Thread(target=f, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
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
    address = ip_section[5:ip_section[5:].find(" ")+5]
    return address

def get_bt_addr() -> tuple[str, int]:
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

@new_thread
@while_true_try
def handle_client(handle: socket.socket):
    while True:
        msg = get_msg(handle)
        if msg == "IP":
            send_msg(handle, get_ip())

@while_true_try
def main():
    addr = (get_bt_addr(), 5)
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.bind(addr)
    sock.listen()
    print(f"Listening @ {addr}")
    while True:
        handle, r_addr = sock.accept()
        handle_client(handle)

if __name__ == "__main__": print(f"`{get_bt_addr()}`")