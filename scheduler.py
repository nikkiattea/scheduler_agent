import socket
import threading
import json

host = '0.0.0.0'
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

def handler(agent, json_data):
    print 'Recieved: %s' % agent
    json_result=[]
    for request in json_data:
        print 'Sending: %s' % request
        agent.sendall(json.dumps(request))
        result = json.loads(agent.recv(4096))
        json_result.append(result)
    writeResults(json_result)
    agent.close()

def writeResults(json_result):
    with open('output.json', 'w') as outfile:
        for line in json_result:
            outfile.write(json.dumps(line)+"\n")
        outfile.close()

def readRequests(filename):
    json_data=[]
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.split("\n")[0]
            json_data.append(json.loads(line))
        infile.close()
    return json_data

def main():
    json_data = readRequests('input.json')

    while True:
        agent,addr = sock.accept()
        print 'Accepted connection from: %s:%d on port %d' % (addr[0], addr[1], port)
        agent_handler = threading.Thread(target=handler,args=(agent,json_data))
        agent_handler.start()
        break

if __name__ == '__main__':
    main()