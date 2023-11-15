from server import get_msg, send_msg
import socket

def main(addr: tuple[str, int]):
    print(f"connecting to {addr}")
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    try:
        sock.connect(addr)
        send_msg(sock, "IP")
        print(f"Remote IP: `{get_msg(sock)}`")
    except:
        print("Comunications Error")

if __name__ == "__main__":
    mac = input("MAC adress> ")
    port = int(input("port> "))
    main((mac, port))
