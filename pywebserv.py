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
		# do stuff
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

def handlecode(code):
	# handle HTTP codes here


