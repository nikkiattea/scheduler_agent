import socket
import subprocess
import time
import json
import time

host = 'localhost'
port = 3000

def main():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            break
        except Exception, e:
            print e
            time.sleep(1)
    sock.close()

if __name__ == '__main__':
    main()