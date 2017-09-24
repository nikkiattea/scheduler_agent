import socket
import threading
import json
import argparse

host = '0.0.0.0'
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

"""
Handles the outgoing TaskRequests and incoming
TaskResults from the agent. Concurrent executions
are not permitted, as per requirements.
"""
def handler(agent, json_data, outfile):
    print 'Recieved: %s' % agent
    json_result=[]
    for request in json_data:
        print 'Sending: %s' % request
        agent.sendall(json.dumps(request))
        result = json.loads(agent.recv(4096))
        print 'Recieved: %s' % result
        json_result.append(result)
    write_results(json_result, outfile)
    agent.close()

"""
Writes to a new line delimited json file per
the json_result dictionary

Default file: output.json
"""
def write_results(json_result, filename):
    if filename is None:
        filename = "output.json"
    with open(filename, 'w') as outfile:
        for line in json_result:
            outfile.write(json.dumps(line)+"\n")
        outfile.close()

"""
Reads from a new line delimited json file and inserts
those lines into a json dictionary

Default file: input.json
"""
def read_requests(filename):
    json_data=[]
    if filename is None:
        filename = "input.json"
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.split("\n")[0]
            json_data.append(json.loads(line))
        infile.close()
    return json_data

"""
Parses command line arguments from scheduler.py

usage: scheduler.py [-h] [--infile INFILE] [--outfile OUTFILE]

Starts the scheduler service accepting an optional input and output file

optional arguments:
  -h, --help            show this help message and exit
  --infile INFILE, -i INFILE
                        path of the input file, default is input.json ex:
                        input.json
  --outfile OUTFILE, -o OUTFILE
                        path of the out file, default is out.json ex:
                        output.json
"""
def get_options():
    parser = argparse.ArgumentParser(description='Starts the scheduler service accepting an optional input and output file')
    parser.add_argument('--infile', '-i', dest='infile', help='path of the input file, default is input.json ex: input.json')
    parser.add_argument('--outfile', '-o', dest='outfile', help='path of the out file, default is out.json ex: output.json')
    options = parser.parse_args()
    return options

"""
Parses command line arguments and json input.
Scheduler will listen on TCP port 3000 until a
connection with an agent is established. It will 
process all TaskRequests from the input file and
return all TaskResults to the output file through
the agent handler.
"""
def main():
    options = get_options()
    json_data = read_requests(options.infile)

    print "Waiting for agent to open..."
    agent,addr = sock.accept()
    print 'Accepted connection from: %s:%d on port %d' % (addr[0], addr[1], port)
    agent_handler = threading.Thread(target=handler,args=(agent,json_data,options.outfile))
    agent_handler.start()
    sock.close()

if __name__ == '__main__':
    main()