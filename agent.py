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
    while True:
        try:
            request = json.loads(sock.recv(4096))
            print "Recieved: %s" % request
            command = request["command"]
            timeout = request["timeout"]
            executed_at = time.time()
            exit_code = subprocess.check_output(command, shell=True)
            execution_finished = time.time()
            duration_ms = execution_finished - executed_at / 100
            result = [{"command":command, "executed_at":executed_at, "duration_ms":duration_ms, "exit_code":exit_code, "output":output, "error":error}]
            print result
        except Exception, e:
            output = 'Could not execute: %s' % request
        time.sleep(5)
        try:
            sock.sendall(json.dumps(result)+'\n')
        except:
            break
    sock.close()

if __name__ == '__main__':
    main()