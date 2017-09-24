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
    sock_input = agent.makefile('r')

    for request in json_data:
        print 'Sending: %s' % request
        agent.sendall(json.dumps(request))
        print json.loads(next(sock_input))
    agent.close()

def main():

    while True:
        agent,addr = sock.accept()
        print 'Accepted connection from: %s:%d on port %d' % (addr[0], addr[1], port)
        agent_handler = threading.Thread(target=handler,args=(agent,json_data))
        agent_handler.start()
        break

if __name__ == '__main__':
    main()