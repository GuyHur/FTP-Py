import socket
import threading
import os
import sys
import time

class Server(threading.Thread):
    def __init__(self, sock, addr, port):
        threading.Thread.__init__(self)
        self.auth = False
        self.sock = sock
        self.addr = addr
        self.port = port
        self.cwd = "/home/Desktop"

    
    def run(self):
        while True:
            try:
                data = self.sock.recv(1024).rstrip()
                try:
                    command = data.decode('utf-8')
                except AttributeError:
                    command = data
                
                if not command:
                    break
            except socket.error as err:
                print(err)

            try:
                command, arg = command[:4].strip().upper(), command[4:].strip( ) or None
                func = getattr(self, command)
            except AttributeError as err:
                print("Command not found.")
    def init(self):
        print("Starting the server socket...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.addr, self.port))
        
        except socket.error as err:
            print("Error starting socket. " + err)

    def sendCommand(self, command):
        self.sock.send(command.encode('utf-8'))

    def LIST(self, dirpath):
        if not self.auth:
            self.sendCommand("[-]User not logged in")
            return

        if not dirpath:
            # List current directory
            pathname = os.path.abspath(os.path.join(self.cwd, '.'))

        elif dirpath.startswith(os.path.sep):
            pathname = os.path.abspath(dirpath)
        else:
            pathname = os.path.abspath(os.path.join(self.cwd, dirpath))


