import sys, socket

CRLF = '\r\n'

def config_fn(fn):
	if not (fn[0] is '/'):
		fn = '/' + fn
	return fn

def parse(data):
	data_list = data.split(CRLF * 2)
	headers = data_list[0]
	if len(data_list) > 1:
		entity = (CRLF * 2).join(data_list[1:])
	else:
		entity = ''
	return [headers, entity]

#print sys.argv, len(sys.argv)

method = sys.argv[len(sys.argv)-1]
print method
if len(sys.argv) == 5:
	fn = sys.argv[3]
elif len(sys.argv)== 4 and (method=='GET' or method=='HEAD'):
	print '\n no file name is specified \n'
	fn = 'index.html'
else:
	print '\n***Error: Arguments not enough'
	sys.exit()

path = config_fn(fn)
HOST = sys.argv[1]
PORT = int(sys.argv[2])
if len(sys.argv)==5:
	filename= sys.argv[3]
else:
	filename='index.html'
print filename
print '\n\nClient is running'
print '---Server Host:', HOST
print '---Server Port:', PORT
print path

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


method= method.ljust(len(method)+1)

client_socket.send( method  +  path + ' HTTP/1.0' + CRLF + 'Host: ' + HOST + CRLF * 2)


content = ''
while True:
	data = client_socket.recv(2048)  #socket.error: [Errno 104] Connection reset by peer
	if not data:
		break
	content += data
	#print '(receiving data...)'
#print 'the content is', content
[headers, entity] = parse(content)
print '\n---HTTP Response\n'
print headers

if method == 'GET ' and headers.split()[1] == '200':
	print '\n---HTTP Entity\n'
	with open('./Download' + path, 'wb') as f:
		print '(writing into file)'
		f.write(entity)
	f.close()
elif method == 'HEAD ':
	print '\n---HTTP Header'
	print '\n Header is displayed on terminal and also writing on the file'
	with open('./Download' + path+'_head.txt', 'wb') as f:
		print '(writing into header file)'
		f.write(headers)
	f.close()
	print headers
	

print '\nClient done\n'
client_socket.close()





