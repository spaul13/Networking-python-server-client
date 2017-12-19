import SRequest, SInvalid, socket, os, threading, sys

CRLF = '\r\n'

FILE_DIR = os.getcwd() + '/Upload' #to find the working directory
print FILE_DIR

TYPE = ['html', 'txt', 'jpeg', 'jpg', 'png']
CON_TYPE = ['text/html', 'text/txt', 'image/jpeg', 'image/jpg', 'image/png']
'''if len(sys.argv) < 2:
	print '\n----Please specify the port no'
	sys.exit()'''

def config_path(path):
	if path is '/':
		path += 'index.html'
	return path[1:]

def search_file(filename):
	filelist = os.listdir(FILE_DIR)
	if filename in filelist:
		return True
	else:
		return False

def listen_to_client(client_socket, client_address):
	try:
		request = client_socket.recv(1024)
		print 'the request is', request
		#print request
		if len(request) == 0:
			#print 'len(request) == 0'
			return
		req = SRequest.HttpRequest(request)
		filename = config_path(req.path)
		filepath = FILE_DIR + '/' + filename
		if search_file(filename):
			perms = oct(os.stat(filepath).st_mode)[3:]
			print '(I am entering)'
			print perms
			if int(perms[3]) >= 4:
				suffix_index = filename.rfind('.')
				filetype = filename[(suffix_index + 1):]
				if filetype in TYPE:
					typeindex = TYPE.index(filetype)
					client_socket.send('HTTP/1.0 200' + CRLF + 'Content-Type: ' + CON_TYPE[typeindex] + CRLF * 2)
					fp = open(filepath, 'r+')
					client_socket.send(fp.read())
					fp.close()
				else:
					raise SInvalid.InvalidRequest(filetype + 'not supported')
			else:
				print perms				
				client_socket.send('HTTP/1.0 403 Permissions denied' + CRLF * 2)
		else:
			client_socket.send('HTTP/1.0 404 Not Found' + CRLF * 2)
		client_socket.close()
	except:
		SInvalid.InvalidRequest("Exception while listening to client")
		client_socket.close()

HOST = ''
PORT = int(sys.argv[1])
print HOST



print '\n\nServer running'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

while True:
	try:
		(client_socket, client_address) = server_socket.accept()
		print '\n\nConnected by ', client_address
		print 'GOT Connection From', client_socket.getpeername()
		threading.Thread(target = listen_to_client, args = (client_socket, client_address)).start()
		#ct = client_thread(client_socket)
    		#ct.run()
	except:
		server_socket.shutdown(socket.SHUT_RDWR)
		break

#http://localhost:5746/index.html
