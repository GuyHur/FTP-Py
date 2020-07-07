import socket
from .data import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import socket
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from .generate_keys import *
import os

def main():
    """
    starting function
    :return: None
    """
    server = PTFServer()
    server.init()


if __name__ == '__main__':
    main()

    class PTFServer():
        """
        PTFServer
        Server for the PTF program: http://github.com/GuyHur


        """
        def __init__(self):
            """
            init server
            :var private_key - server private key[DO NOT SEND THE CLIENT]
            :var public_key - send to the client to encrypt the file
            :var string host- server ip
            :var int server_port - server port, initializes at 5001
            :var int buffer - file buffer
            :var connections[] - array of Clients
            :var socket- socket
            :var client - client class
            """
            self.private_key = None
            self.public_key = None
            self.host = "0.0.0.0"
            self.server_port = 5001
            self.buffer = 4096
            self.connections = []
            self.socket = socket
            self.path = "Desktop/PTF/"

        def new_connections(self):
            while True:
                sock,address = self.socket.accept()
                self.connections.append(address)
        def get_state(self):
            while True:
                data = self.socket.socket.recv(1024)
                if data is not 0 or 1 or 2:
                    print("[-]Anomaly State, forcing connection to close...")
                if not data:
                    break

        def init(self):
            """
            Server starts here!!!
            Initialize everything on the program
            :return: None
            """
            try:
                self.handle_keypairs()
                #Create Public & Private RSA keys
                self.new_connections()

            except Exception as exc:
                print (exc)


        def handle_keypairs(self):
            """
            read private key from private_key.pem and save it to self.private_key
            read public key from public_key.pem and save it to self.public_key
            :var private_key - private key
            :return: None
            """
            with open(self.path + "private_key.pem", "rb") as private_key_data:
                self.private_key = load_pem_private_key(private_key_data.read(), password=None, backend=default_backend())
            with open(self.path + "public_key.pem", "rb") as public_key_data:
                self.public_key = load_pem_private_key(public_key_data.read(), password=None, backend=default_backend())


