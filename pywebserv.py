#!/usr/bin/env python3

# cs435 computer networks
# fall 16
# adam

import os
import datetime
from datetime import date
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
		opts, args = getopt.getopt(sys.argv[1:], "hp:r:")
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

def formatdate():
	return "Date: " + date.strftime(datetime.datetime.now(), format) + "\n"

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
	print("code start")
	print(code)
	print("code end")
	headers = parseheaders(req)
	for h,v in headers.items():
		print("{} => {}".format(h,v))
	if code != "GET":
		response = "HTTP/1.1 405 Method Not Allowed\n" + formatdate()
	try:
		for file in code.split():
			if(file.startswith("/")):
				reqfile = root + file
				break
		print("reqfile is")
		print(reqfile)
		print("reqfile end")
		if(reqfile.endswith("html")):
			mimetype = content["html"]
		elif(reqfile.endswith("css")):
			mimetype = content["css"]
		elif(reqfile.endswith("gif")):
			mimetype = content["gif"]
		elif(reqfile.endswith("png")):
			mimetype = content["png"]
		elif(reqfile.endswith("jpg") or reqfile.endswith("jpeg")):
			mimetype = content["jpg"]
		elif(reqfile.endswith("js")):
			mimetype = content["js"]
		ctype = "Content-Type: " + mimetype + "\n"
		if "If-Modified-Since" in headers:
			headertime = datetime.datetime.strptime(headers["if-modified-since"])
			filetime = datetime.datetime(os.getmtime(reqfile))
			if headertime > filetime:
				response = "HTTP/1.1 304 Not Modified\n" + formatdate()
		with open(reqfile, 'rb') as f:
			respheader = "HTTP/1.1 200 OK\n" + formatdate() + ctype + mimetype + "\n\n"
			return bytes(respheader, 'UTF-8') + f.read(), mimetype
	except IOError:
		response = "HTTP/1.1 404 File Not Found\n" + formatdate()
	return response + "\n\n", mimetype

def main(argv):
	port, root = getopts(argv)
	sock = servinit(port, root)
	sock.listen(1)
	while True:
		conn, addr = sock.accept()
		msg = conn.recv(2048)
		resp, mimetype = handlereq(msg.decode('UTF-8'), root)
		print("resp start")
		print(resp)
		print("resp end")
		conn.send(resp)
		conn.close()
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

if __name__ == "__main__":
	main(sys.argv)
