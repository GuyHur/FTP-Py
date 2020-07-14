import socket
import cryptography
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

#Constants:

FILEPATH = 'Desktop/PTF/input/'




#End Constants


class PTFClient():
    def __init__(self, file):
        self.file = file
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveraddress = "127.0.0.1"# Could be sys.argv[1]
        self.serverport = 5001
        self.public_key = None
        self.encrypted = None


    def connect_to_server(self):
        try:
            self.sock.connect(self.serveraddress, self.serverport)
            print("[+]Connection successful" + self.serveraddress)

        except Exception as e:
            print(e)

    def recieve_key(self):
        while True:
            public_key = self.sock.recv(1024)
            if not public_key:
                print("Recieved public key.")
                break
        self.public_key = public_key
    def handle_file(self):
        with open(self.file, 'rb') as client_file:
            self.encrypt_file(client_file.read(), self.public_key)


    def encrypt_file(self,file, public_key):
        encrypted = public_key.encrypt(file)
        self.encrypted = encrypted

    def send_file_to_server(self):
        self.sock.send(self.encrypted)

def main():
    #Initialize client

    #Creates instance of client --> python client.py filepath
    client = PTFClient(file=sys.argv[1])
    try:
        client.connect_to_server()
        client.recieve_key()
        client.handle_file()


    except Exception as e:
        print(e)

