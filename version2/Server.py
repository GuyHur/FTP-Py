import socket
import threading
import os
import sys
import time

delete = False

try:
    HOST = socket.gethostname(socket.gethostname())
except socket.gaierror:
    HOST = '127.0.0.1'
PORT = 21

CWD = os.getenv('windir')


def log(func, cmd):
    msg = time.strftime("%Y-%m-%d %H-%M-%S [-] " + func)
    print("\033[31m%s\033[0m: \033[32m%s\033[0m" % (msg, cmd))


class FTPServer(threading.Thread):
    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.authenticated = False
        self.cwd = CWD
        self.sock = sock
        self.addr = addr

    def run(self):
        """
        run: the main function
        :return: None
        """
        self.sendWelcome()
        while True:
            try:
                data = self.sock.recv(1024)
                try:
                    cmd = data.decode('utf-8')
                except AttributeError:
                    cmd = data
                log('Data Received', cmd)
                if not cmd:
                    break
            except socket.error as err:
                log('Receive', err)
            try:
                cmd, arg = cmd[:4].strip().upper(), cmd[4:].strip() or None
                func = getattr(self, cmd)
                func(arg)
            except AttributeError as err:
                self.sendCommand('500 Syntax error, command unrecognized.'
                                'This may include errors such as command line too long.\r\n')
                log('Receive', err)

    def sendCommand(self, cmd):
        self.sock.send(cmd.encode('utf-8'))

    def sendWelcome(self):
        self.sendCommand("220 Hello client! \r\n")

    def sendData(self, data):
        self.sock.send(data.encode('utf-8'))

    """
    ------------
    FTP Commands
    ------------
    """

    def LOGIN(self, username, password):


    def TYPE(self, type):
        pass

    def PASV(self, type):
        """

        :param type:
        :return:
        """
        pass

    def LIST(self, dirpath):
        """

        :param dirpath:
        :return:
        """

        pass

    def CWD(self, cwd):
        """
        CWD: sets the CWD on the server

        :param cwd:
        :return: None
        """
        pass

    def GET(self, file):
        pass

    def EXIT(self):
        pass

def listener():
    global listen_sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(5)

    log('Accept', 'Created a new connection {}'.format(listen_sock.getsockname()))
    while True:
        s, address = listen_sock.accept()
        f = FTPServer(s, address)
        f.start()
        log('Accept', 'Created a new connection {}'.format(address))

        if input().lower() == "q":
            listen_sock.close()
            log('Server stopped', 'Server closed')
            sys.exit()
if __name__ == '__main__':
    log('Started server', 'Enter q or Q to stop the server...')
    l = threading.Thread(target = listener)
    l.start()

