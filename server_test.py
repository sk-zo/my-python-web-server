import socket

HOST = '0.0.0.0'  # 모든 인터페이스에서 수신
PORT = 43251

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # TCP 소켓 생성
        s.bind((HOST, PORT)) # 소켓에 주소와 포트 바인딩
        s.listen() # 클라이언트 연결 요청 대기
        print(f"Server is running on {HOST}:{PORT}")

        # 클라이언트 연결 요청을 지속적으로 처리
        while True:
            conn, addr = s.accept()  # 새로운 클라이언트 연결 수락
            print(f"Connected by {addr}")

            # 클라이언트로부터 HTTP 요청 수신
            payload = conn.recv(1024)
            print(f"Received payload: {payload}")

            # HTTP 응답 전송
            response = b"HTTP/1.1 200 OK\r\n\r\nHello World"
            conn.send(response)

            conn.close()  # 클라이언트 연결 종료
except KeyboardInterrupt:
    print("\nServer is shutting down...")
except Exception as e:
    print(f"Server error: {e}")
        

    