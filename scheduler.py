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
    #sock_input = agent.makefile('r')

    for request in json_data:
        print 'Sending: %s' % request
        agent.sendall(json.dumps(request))
        result = json.loads(agent.recv(4096))
        print 'Recieved task result: %s\n' % result
    agent.close()

def main():
    json_data=[]
    with open('input.json', 'r') as file:
        for line in file:
            line = line.split("\n")[0]
            json_data.append(json.loads(line))
        file.close()

    json_data = [{"command": ["echo", "hello"], "timeout": 1000},{"command": ["echo", "world"], "timeout": 1000},{"command": ["echo", "!"], "timeout": 1000}]
    while True:
        agent,addr = sock.accept()
        print 'Accepted connection from: %s:%d on port %d' % (addr[0], addr[1], port)
        agent_handler = threading.Thread(target=handler,args=(agent,json_data))
        agent_handler.start()
        break

if __name__ == '__main__':
    main()