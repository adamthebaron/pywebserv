#!/usr/bin/env python3
import socket
import sys

if __name__ == "__main__":
	main()

def servinit(argv):
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
