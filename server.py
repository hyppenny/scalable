import socket, sys

if (len(sys.argv) < 3):
    print("Server usage: python server.py IP PORT")
    sys.exit(0)

PORT = sys.argv[2]
PORT = int[PORT]


class ChatRoom():
    def __init__(self):
        self.message = []
        self.client = []


class Server():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", PORT))


class ChatInfo():
    def __init__(self):
        self.room = {}
        self.roomRef = {}


