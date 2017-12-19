import SInvalid

class HttpRequest(object):
	def __init__(self, request):
		self._request = request
		(self.method, self.path, self.protocol, self.headers) = self.parse()

	def parse(self):
		line = [i.strip() for i in self._request.splitlines()]
		if len(line) == 0:
			print self._request
			raise SInvalid.InvalidRequest('Invalid Request')
		if line[0].find('HTTP') == -1:
			(method, path) = [i.strip() for i in line[0].split()]
			print method
			#raise SInvalid.InvalidRequest('Protocol wrong!')
		else:
			(method, path, protocol) = [i.strip() for i in line[0].split()]
			print method

		headers = {}
		if method == 'GET' or method == 'HEAD':
			print path
			
			for j, k in [i.split(':', 1) for i in line[1:-1]]:
				headers[j.strip()] = k.strip()
		else:
			raise SInvalid.InvalidRequest('Http Method not' + method + '!')

		return (method, path, protocol, headers)
