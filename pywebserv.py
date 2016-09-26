#!/usr/bin/env python3
import socket
import sys

if __name__ == "__main__":
	main()

def getopts(argv):
	try:
		opts, args = getopt.getopt(argv[1:], "p:s:")
	except getopt.GetoptError:
		print("pywebserv -p port -r root")
		sys.exit()
	for opt, arg in opts:
		if opt == '-p':
			port = int(arg)
		elif opt == '-r':
			root = arg
	return port, root

def servinit(port, root):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('',port))
	sock.listen(1)
	print("socket initialized")
	while True:
		conn, addr = sock.accept()
		message = conn.recv(2048)
		resp = handlecode(message.decode('UTF-8'))
		conn.send(bytes(resp, 'UTF-8'))
		conn.close()
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

def parseheader(req):
	# parse the header here

def handlecode(code):
	# handle HTTP codes here