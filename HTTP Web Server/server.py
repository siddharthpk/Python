<html>
  <head>
    <meta http-equiv="Content-Style-Type" content="text/css" /> 
    <title>server.py</title>
    <link href="/library/skin/tool_base.css" type="text/css" rel="stylesheet" media="all" />
    <link href="/library/skin/connex-default/tool.css" type="text/css" rel="stylesheet" media="all" />
    <script type="text/javascript" language="JavaScript" src="/library/js/headscripts.js"></script>
    <style>body { padding: 5px !important; }</style>
  </head>
  <body>
#import socket module
from socket import *
import datetime
import sys

"""
memo:
"**".join() :for loop join string and concatenate by **
date format use date.date.now.strftime() 
"""
serverSocket = socket(AF_INET, SOCK_STREAM) #Prepare a sever socket

serverPort = 6789
serverSocket.bind(('',serverPort))
serverSocket.listen(10)


while True:
	#Establish the connection
	print('Ready to serve...')
	connectionSocket, addr = serverSocket.accept()
	print("addr:\n", addr)
	try:
		message = connectionSocket.recv(1024)
		print("message: \n", message)
		filename = message.split()[1]
		f = open(filename[1:])
		outputdata = f.read() 
		print("outputdata:", outputdata)
		now = datetime.datetime.now()
		#Send one HTTP header line into socket
		
		first_header = "HTTP/1.1 200 OK"
		
		header_info = {
			"Date": now.strftime("%Y-%m-%d %H:%M"),
			"Content-Length": len(outputdata),
			"Keep-Alive": "timeout=%d,max=%d" %(10,100),
			"Connection": "Keep-Alive",
			"Content-Type": "text/html"
		}
		
		following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
		print("following_header:", following_header)
		connectionSocket.send("%s\r\n%s\r\n\r\n" %(first_header, following_header))
		
		#Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i])
		connectionSocket.close()
	except IOError:
		#Send response message for file not found
		 
		connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>404 Not Found<h1></body></html>")
		#Close client socket 
		connectionSocket.close()
		
serverSocket.close()

  </body>
</html>
