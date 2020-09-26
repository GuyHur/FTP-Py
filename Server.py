from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import socket
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
import sys
import threading
class FTPServer():
    """
    FTPServer
    Server for the FTP program: http://github.com/GuyHur/FTP
    """

    class Client():
        """
        Client class for inventory keep
        """

        def __init__(self, socket, address, name):
            self.s = socket
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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = None
        self.public_key = None
        self.ThreadCount = 0
        self.host = "0.0.0.0"
        self.server_port = 5001
        self.buffer = 4096
        self.encrypted_file = None
        self.connections = []
        self.path = "Desktop/FTP/"
        self.client = self.Client(None, None, None)

    def handle_client(self, client_socket, client_address):
        print("[NEW CONNECTION]" + str(client_address) + "connected.")
        self.send_public_key(client_socket, client_address)
        print("[+] Sent public key to client.")
        with open('recieved_file_encrypted', 'wb') as encrypted_file:

            data = True
            while data:
                data = self.s.recv(self.buffer)

                if not data:
                    print("Finished receiving file.")
                    break
            encrypted_file.write(data)


    def send_public_key(self, client_socket, client_address):
        print("[+]Sending public key to client at :" + self.client.address)
        with open("public_key.pem", "rb") as public_key:
            data = public_key.read(self.buffer)
            while data:
                client_socket.send(data)
                print("Sent", repr(data))




    def decrypt_file(self):
        """
        decrypts the file with the private key in private_key.pm
        """
        original_file = self.private_key.decrypt(
                    encrypted,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
        with open('decrypted_file', 'wb') as decrypted:
            decrypted.write(original_file)

    def start(self):
        self.init()
        try:
            while True:
                client_socket, client_address = self.s.accept()
                thread = threading.Thread(target=self.handle_client(), args=(client_socket, client_address) )
                thread.start()

                self.send_public_key()
                self.receive_encrypted_file()
                self.decrypt_file()
                self.s.close()

        except Exception as e:
            print(e)

    def init(self):
        """
        Server starts here!!!
        Initialize everything on the program
        -Server initializes
        """
        try:
            self.generate_keypairs()
            self.save_keypairs()
            print("[+]Generated keys...")
            # Creates Public & Private RSA keys and save them to self.public_key and self.private_key
            self.s.bind((self.host, self.server_port))
            print("Binding " + self.host + "to " + str(self.server_port))
            self.s.listen()

        except Exception as exc:
            print(str(exc))

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
    server = FTPServer()
    server.start()


if __name__ == '__main__':
    main()
