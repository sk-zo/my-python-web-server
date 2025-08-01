import socket
from abc import ABC, abstractmethod

class BaseServer(ABC):
    def __init__(self, host='0.0.0.0', port=43252):
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
                # 클라이언트 연결 예외 처리
                print(f"Connecdted by {addr}")

                # 데이터 수신
                payload = conn.recv(1024)
                # 데이터 수신 예외 처리

                print(f"Received payload: {payload}")

                conn.sendall("response".encode('utf-8'))
                conn.close()

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.stop()

    def handle_client(conn, addr):
        try:
            print(f"Connencted by {addr}")
            payload = conn.recv(1024)
            print(f"Receieved payload: {payload}")
            with open('templates/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                    
                response = f"HTTP/1.1 200 OK\r\n"
                response += f"Content-Type: text/html; charset=utf-8\r\n"
                response += f"Content-Length: {len(content.encode('utf-8'))}\r\n"
                response += f"Connection: close\r\n"
                response += f"\r\n"
                response += content

                conn.sendall(response.encode('utf-8'))
        finally:
            conn.close()

    



            
