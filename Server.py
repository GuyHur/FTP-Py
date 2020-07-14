import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import socket
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
import sys
class PTFServer():
    """
    PTFServer
    Server for the PTF program: http://github.com/GuyHur
    """

    class Client():
        """
        Client class for inventory keep
        """

        def __init__(self, socket, address, name):
            self.socket = socket
            self.address = address
            self.name = name

        def __str__(self):
            return 'Client id: {id}, Client address: {address}'.format(id=self.id, address=self.address)

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
        self.encrypted_file = None
        self.connections = []
        self.path = "Desktop/PTF/"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = self.Client(None, None, None)

    def new_connections(self):
        while True:
            name = self.socket.gethostbyname()
            client_socket, client_address = self.server_socket.accept()
            self.connections.append(self.Client(client_socket, client_address, name))
            self.client = self.Client(client_socket, client_address, name)
            print("[+] New Connection from: " + client_address)

    def send_public_key(self):
        """
        send_public_key(self) - sends client the public key
        """
        print("[+]Sending public key to client at :" + self.client.address)
        self.socket.send(self.public_key)

    def decrypt_file(self):
        """
        decrypts the file with the private key in private_key.pm
        """
        original_file = private_key.decrypt(
                    encrypted,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
        with open('decrypted_file', 'wb') as decrypted:
            decrypted.write(original_file)

    def recieve_encrypted_file(self):
        """
        recieves the file from the client.
        :return:
        """
        while True:
            data = self.socket.recv(self.buffer)
            if not data:
                print("Finished reciving file.")
                break
        self.encrypted_file = data

    def init(self):
        """
        Server starts here!!!
        Initialize everything on the program
        -Server initializes
        """
        try:
            self.generate_keypairs()
            self.save_keypairs()
            # Creates Public & Private RSA keys and save them to self.public_key and self.private_key
            self.new_connections()
            # Accepts the connection and creates a new Client instance.
            self.send_public_key()
            # Sends the connected client the public key
            self.recieve_encrypted_file()
            # Recieves encrypted file from client
            self.decrypt_file()
            # Decrypts file from client using the private key
            # Saves the decrypted file to the server output folder.
            self.socket.close()

        except Exception as exc:
            print(exc)

    def generate_keypairs(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        public_key = private_key.public_key()
        self.private_key = private_key
        self.public_key = public_key

    def save_keypairs(self):
        try:
            if self.private_key == None or self.public_key == None:
                print("Keys are not valid to save..")
            pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open('private_key.pem', 'wb') as f:
                f.write(pem)
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open('public_key.pem', 'wb') as f:
                f.write(pem)

        except Exception as e:
            print(e)


def main():
    """
    starting function
    Runs server
    """
    server = PTFServer()
    server.init()


if __name__ == '__main__':
    main()
