#!/usr/bin/env python3

# cs435 computer networks
# fall 16
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

headers = [
	"Host",
	"If-Modified-Since"
]

format = "%a, %d %b %Y %H:%M:%S %Z"

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
	port = 43500
	root = "{}/html/".format(os.getcwd())
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
	return sock

def parseheaders(req):
	headers = {}
	for curline in req.split('\n')[1:]:
		if curline == '\r':
			break
		curheader = curline.partition(':')
		headers[curheader[0].lower()] = curheader[2].strip()
	return headers

def handlereq(req, root):
	code = req.split('\n')[0]
	headers = parseheaders(req)
	for h,v in headers.items():
		print("{} => {}".format(h,v))
	if code != "GET":
		response = "HTTP/1.1 405 Method Not Allowed"
	try:
		file = "{}{}".format(root, req)
		if "If-Modified-Since" in headers:
			headertime = datetime.datetime.strptime(headers["if-modified-since"])
			filetime = datetime.datetime(os.getmtime(file))
			if headertime > filetime:
				response = "HTTP/1.1 304 Not Modified"
		with open(file) as f:
			print(f.read())
			response = "HTTP/1.1 200 OK\n" + f.read()
	except IOError:
		response = "HTTP/1.1 404 File Not Found"
	return response

def main(argv):
	port, root = getopts(argv)
	sock = servinit(port, root)
	sock.listen(1)
	while True:
		conn, addr = sock.accept()
		msg = conn.recv(2048)
		resp = handlereq(msg.decode('UTF-8'), root)
		conn.send(bytes(resp, 'UTF-8'))
		#conn.close()
	conn.close()
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

if __name__ == "__main__":
	main(sys.argv)
