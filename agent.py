import socket
from subprocess import Popen, PIPE
import time
import json
import time
import datetime
from threading import Timer

host = 'localhost'
port = 3000

def runCommandWithTimeout(request):
    try:
        command = request["command"]
        timeout = request["timeout"]
        startTime = time.time()
        executed_at = str(time.ctime(int(startTime)))
        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        kill_proc = lambda process: process.kill()
        timer = Timer(timeout, kill_proc, [proc])
        try:
            timer.start()
            output, error = proc.communicate()
            exit_code = proc.returncode
            if exit_code != 0:
                exit_code = -1
                result={"command":command, "exit_code":exit_code, "error":"timeout exceeded"}
                return result
        finally:
            timer.cancel()
        finishTime = time.time()
        duration_ms = (finishTime - startTime) * 100
        result={"command":command, "executed_at":executed_at, "duration_ms":duration_ms, "exit_code":exit_code, "output":output, "error":error}
    except Exception, e:
        error = str(e)
        exit_code = -1
        result={"command":command, "exit_code":exit_code, "error":error}
    return result

def main():
    print "Waiting for scheduler to open..."
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            break
        except Exception, e:
            time.sleep(1)
    running = True
    while running:
        try:
            request = json.loads(sock.recv(4096))
            print "Recieved: %s" % request
            result = runCommandWithTimeout(request)
            try:
                print "Sending: %s" % result
                sock.sendall(json.dumps(result))
            except Exception, e:
                print "cannot allow concurrent executions: %s"%str(e)
        except Exception, e:
            running = False
    sock.close()

if __name__ == '__main__':
    main()