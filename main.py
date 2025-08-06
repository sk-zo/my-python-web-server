from server import SyncServer, AsyncServer

if __name__ == "__main__":
    # server = SyncServer()
    server = AsyncServer()
    server.start()