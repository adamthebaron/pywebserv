#!/usr/bin/env python3

# CS435 Computer Networks
# Fall 16
# adam

import os
import datetime
import getopt
import socket
import sys

content = {
    'html': 'text/html',
    'css':  'text/css',
    'js':   'application/x-javascript',
    'jpg':  'image/jpeg',
    'gif':  'image/gif',
    'png':  'image/png' 
}

resp = {
    '200': 'OK',
    '304': 'Not Modified',
    '404': 'Not Found',
    '405': 'Method Not Allowed'
}

def usage():
    print("pywebserv -h -p port -r root")
    print("default port is 43500")
    print("default root is cwd")

def getopts(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:s:")
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-p':
            port = int(arg)
        elif opt == '-r':
            root = arg
        elif opt == '-h':
            usage()
        sys.exit()
    return port, root

def servinit(port, root):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',port))
    print("socket initialized")

#def parseheader(req):
    # parse the header here

#def handlecode(code):
    # handle HTTP codes here
	
def main(argv):
    port, root = getopts(argv)
    sock = servinit(port, root)
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        message = conn.recv(2048)
        resp = handlecode(message.decode('UTF-8'))
        conn.send(bytes(resp, 'UTF-8'))
        conn.close()
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    
if __name__ == "__main__":
    main(sys.argv)
