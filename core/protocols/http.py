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

class HTTPResponse:
    def __init__(self, status_code=200, body="", headers=None):
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}

        # # CORS 헤더 자동 추가
        # self.headers.setdefault('Access-Control-Allow-Origin', 'localhost:8080')
        # self.headers.setdefault('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        # self.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        # # Content-Length 자동 설정
        # if 'Content-Length' not in self.headers:
        #     self.headers['Content-Length'] = str(len(body.encode('utf-8')))

    @classmethod
    def html(cls, status_code, body):
        headers = {"Content-Type": "text/html; charset=utf-8"}
        return cls(status_code=status_code, body=body, headers=headers)  # 명시적으로 지정!

    @classmethod
    def json(cls, status_code, body):
        import json
        json_body = json.dumps(body)
        headers = {"Content-Type": "application/json; charset=utf-8"}
        return cls(status_code=status_code, body=json_body, headers=headers)

    def to_http_string(self):
        response = f"HTTP/1.1 {self.status_code} {self._get_status_text()}\r\n"
        
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"

        response += f"\r\n{self.body}"
        return response

    def to_bytes(self):
        return self.to_http_string().encode('utf-8')

    def _get_status_text(self):
        status_texts = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error",
            400: "Bad Request"
        }

        return status_texts[self.status_code]
        


class HTTPParser:
    @staticmethod
    def parse_request(raw_request):
        lines = raw_request.split("\r\n")

        if not lines or not lines[0].strip():
            raise ValueError("Emptry request")
        
        request_line = lines[0]
        parts = request_line.split(' ')
        if len(parts) != 3:
            raise ValueError(f"Invalid request line: {request_line}")
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

    

        
        