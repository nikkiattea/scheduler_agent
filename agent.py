import socket
from subprocess import Popen, PIPE
import time
import json
import time
import datetime

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
    running = True
    while running:
        try:
            request = json.loads(sock.recv(4096))
            print "Recieved: %s" % request
            command = request["command"]
            timeout = request["timeout"]
            startTime = time.time()
            executed_at = str(time.ctime(int(startTime)))
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
            output, error = proc.communicate()
            exit_code = proc.returncode
            finishTime = time.time()
            duration_ms = (finishTime - startTime) * 100
            result={"command":command, "executed_at":executed_at, "duration_ms":duration_ms, "exit_code":exit_code, "output":output, "error":error}
        except Exception, e:
            output = 'Could not execute: %s' % request

        try:
            sock.sendall(json.dumps(result))
        except Exception, e:
            running = False
    sock.close()

if __name__ == '__main__':
    main()