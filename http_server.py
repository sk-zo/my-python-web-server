import socket

HOST = '0.0.0.0'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        with conn:
            data = conn.recv(1024)
            request = data.decode('utf-8')
            print(f"Received request: {request}")

            if request:
                with open('templates/index.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                response = f"HTTP/1.1 200 OK\r\n"
                response += f"Content-Type: text/html; charset=utf-8\r\n"
                response += f"Content-Length: {len(content.encode('utf-8'))}\r\n"
                response += f"Connection: close\r\n"
                response += f"\r\n"
                response += content

                conn.sendall(response.encode('utf-8'))

                conn.close()


    s.close()
    print("Server is closed")
