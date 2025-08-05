import socket
from abc import ABC, abstractmethod
from core.protocols.http import HTTPRequest, HTTPResponse, HTTPParser
from core.routes import routes, not_found

class BaseServer(ABC):
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.listening_socket = None
        self.is_running = False
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def handle_client(self, conn, addr):
        pass

    def setup_socket(self):
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen()
        print(f"Server is running on {self.host}:{self.port}")
    
    def stop(self):
        self.is_running = False
        if self.listening_socket:
            self.listening_socket.close()


class SyncServer(BaseServer):
    def start(self):
        try:
            self.setup_socket()
            self.is_running = True
            # 수신 요청 처리
            while self.is_running:
                # 클라이언트 연결 소켓 생성
                conn, addr = self.listening_socket.accept()
                self.handle_client(conn, addr)

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.stop()

    def handle_client(self, conn, addr):
        try:
            print(f"Connnected by {addr}")
            payload = conn.recv(1024)
            raw_request = payload.decode('utf-8')
            request = HTTPParser.parse_request(raw_request)
            request.print_self()

            route_key = (request.method, request.path)
            handler = routes.get(route_key, not_found)

            response = handler(request)

            conn.sendall(response.to_bytes())
        finally:
            conn.close()

    



            
