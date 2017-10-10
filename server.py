import socket, sys
from threading import Thread

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


class Process():
    def __init__(self):
        self.room = []
        self.id = id

    def send_message(self, text):
        pass

    def process_message(self, message):
        if message == "KILL_SERVICE\n":
            self.pool.kill()
        elif message.startswith("HELO "):
            self.connect.send("hello")


class Pool():
    def __init__(self):
        self.lockClient = threading.Lock()
        self.lockState = threading.Lock()
        self.client = []
        self.worker = []
        self.state = ChatInfo()
        self.threadCounter = 0
        self.kill = False
        for i in range(2):
            reply = "HELO"
            return reply

    def kill(self):
        self.kill = True

