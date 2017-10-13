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


class Server(Thread):
    def __init__(self, pool):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", PORT))

    def run(self):
        self.server.listen(5)
        (connect, (IP,PORT)) = self.server.accept()
        print("Connection Established")
        self.pool.assignClient

class ChatInfo():
    def __init__(self):
        self.room = {}
        self.roomRef = {}


class Process():
    def __init__(self, poll, id):
        self.room = []
        self.id = id
        self.pool = pool

    def send_message(self, text):
        pass

    def process_message(self, message):
        if message == "KILL_SERVICE\n":
            self.pool.kill()
        elif message.startswith("HELO "):
            self.connect.send("hello")
        elif message.startswith("JOIN_CHATROOM: "):
            roomName = message.splitlines()[0][len("JOIN_CHATROOM: "):]
            clientName = message.splitlines()[3][len("CLIENT_NAME: "):]
            self.pool.lockState.acquire()

            clientID = self.pool.state.idCounter
            self.pool.state.idCounter += 1

            if roomName in self.pool.state.rooms:
                roomRef = self.pool.state.rooms[roomName].ref
            else:
                roomRef = self.pool.state.refCounter
                self.pool.state.rooms[roomName] = ChatRoom(roomRef)
                self.pool.state.refCounter += 1
                room = self.pool.state.rooms[roomName]

            if (len(room.client) > 0):
                joinMessage = "{0} has joined the chatroom".format(clientName)
                room.messages.append([clientName, joinMessage, set(room.clients)])
                self.pool.state.rooms[roomName].clients.append(clientID)
                self.pool.lockState.release()

class Pool():
    def __init__(self):
        self.client = []
        self.worker = []
        self.state = ChatInfo()
        self.threadCounter = 0
        self.kill = False
        self.connect = None
        for i in range(2):
            reply = "HELO"
            return reply

    def kill(self):
        self.kill = True

    def assignClient(self, connect):
        pass
