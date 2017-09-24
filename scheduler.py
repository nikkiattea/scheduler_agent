import socket
import threading
import json
import argparse

host = '0.0.0.0'
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

def handler(agent, json_data, outfile):
    print 'Recieved: %s' % agent
    json_result=[]
    for request in json_data:
        print 'Sending: %s' % request
        agent.sendall(json.dumps(request))
        result = json.loads(agent.recv(4096))
        print 'Recieved: %s' % result
        json_result.append(result)
    writeResults(json_result, outfile)
    agent.close()

def writeResults(json_result, filename):
    if filename is None:
        filename = "output.json"
    with open(filename, 'w') as outfile:
        for line in json_result:
            outfile.write(json.dumps(line)+"\n")
        outfile.close()

def readRequests(filename):
    json_data=[]
    if filename is None:
        filename = "input.json"
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.split("\n")[0]
            json_data.append(json.loads(line))
        infile.close()
    return json_data

def getOptions():
    parser = argparse.ArgumentParser(description='Starts the scheduler service accepting an optional input and output file')
    parser.add_argument('--infile', '-i', dest='infile', help='path of the input file, default is input.json ex: input.json')
    parser.add_argument('--outfile', '-o', dest='outfile', help='path of the out file, default is out.json ex: output.json')
    options = parser.parse_args()
    return options

def main():
    options = getOptions()
    json_data = readRequests(options.infile)

    while True:
        print "Waiting for agent to open..."
        agent,addr = sock.accept()
        print 'Accepted connection from: %s:%d on port %d' % (addr[0], addr[1], port)
        agent_handler = threading.Thread(target=handler,args=(agent,json_data,options.outfile))
        agent_handler.start()
        break
    sock.close()

if __name__ == '__main__':
    main()