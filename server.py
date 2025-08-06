import socket
import asyncio
from abc import ABC, abstractmethod
from core.protocols.http import HTTPRequest, HTTPResponse, HTTPParser
from core.routes import routes, not_found, bad_request

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
    def handle_client(self, *args, **kwargs):
        pass

    def process_request(self, raw_request: str) -> HTTPResponse:
        try:
            request = HTTPParser.parse_request(raw_request)
            request.print_self()

            route_key = (request.method, request.path)
            handler = routes.get(route_key, not_found)

            response = handler(request)
            return response
        
        except Exception as e:
            print(f"Exception: {e}")
            return bad_request()

    
    
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

    def setup_socket(self):
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.host, self.port))
        self.listening_socket.listen()
        print(f"Server is running on {self.host}:{self.port}")

    def handle_client(self, conn, addr):
        try:
            print(f"Connnected by {addr}")
            payload = conn.recv(1024)
            raw_request = payload.decode('utf-8')
            response = self.process_request(raw_request)

            conn.sendall(response.to_bytes())
        
        except Exception as e:
            print(e)

        finally:
            conn.close()

class AsyncServer(BaseServer):
    def start(self):
        try:
            asyncio.run(self.setup_server())
        except Exception as e:
            print(f"Error occurred: {e}")

    async def setup_server(self):
        try:
            server = await asyncio.start_server(
                self.handle_client,
                self.host,
                self.port,
                reuse_address = True
            )

            await server.serve_forever()

        except Exception as e:
            raise Exception(f"Error occurred: {e}")
            

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New async connection from {addr}")

        try:
            payload = await reader.read(1024)

            raw_request = payload.decode('utf-8')
            
            response = self.process_request(raw_request)

            writer.write(response.to_bytes())

            await writer.drain()

        except asyncio.CancelledError:
            print(f"Connection with {addr} was cancelled")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()


    



            
