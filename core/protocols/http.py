class HTTPRequest:
    def __init__(self, method, path, version, headers, body):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body

    def print_self(self):
        request = "Received request: \r\n"
        request += self.method + ' ' + self.path + ' ' + self.version
        
        for key, value in self.headers.items():
            request += '\r\n' + key + ": " + value

        request += '\r\n' + self.body

        print(request)
        


class HTTPParser:
    @staticmethod
    def parse_request(raw_request):
        lines = raw_request.split("\r\n")
        
        request_line = lines[0]
        method, path, version = request_line.split(' ')

        headers = {}
        i = 1
        while i < len(lines) and lines[i] != '':
            header_line = lines[i]
            key, value = header_line.split(': ', 1)
            headers[key] = value
            i += 1

        body = ''
        if i + 1 < len(lines):
            body = '\r\n'.join(lines[i + 1:])

        return HTTPRequest(method, path, version, headers, body)

    

        
        