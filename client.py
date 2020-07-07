import socket
import cryptography
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
public_key = rsa.publ
class PTFClient():
    def __init__(self):
        self.file = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveraddress = "127.0.0.1" # Could be sys.argv[1]
        self.serverport = 5001
        self.state = 0


    def connect(self, serveraddress, serverport):
        try:
            self.sock.connect(self.serveraddress, self.serverport)
            self.sock.sendall(0)
            print("[+]Connection successful" + serveraddress)
        except Exception:
            print("Connection failed")

    def recieve(self):
        while self.state == 0:
            #Recieve public key
            public_key = self.sock.recv(2048)


    def main(self):
        self.connect(self.serveraddress, self.serverport)

