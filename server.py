import socket, sys
from threading import Thread

# if (len(sys.argv) < 3):
#     print("Server usage: python server.py IP PORT")
#     sys.exit(0)

PORT = 5555 #sys.argv[2]
IP = "127.0.0.1"
#PORT = int(PORT)


class ChatRoom():
    def __init__(self):
        self.message = []
        self.client = []


class Server(Thread):
    def __init__(self, pool):
        Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((IP, PORT))
        self.pool = pool

    def run(self):
        while True:
            self.server.listen(5)
            (connect, (ip, port)) = self.server.accept()
            print("Connection Established")
            self.pool.assignClient(connect)


class ChatInfo():
    def __init__(self):
        self.room = {}
        self.roomRef = {}
        self.ID_Counter = 0
        self.REF_Counter = 0


class Process(Thread):
    def __init__(self, pool, id):
        Thread.__init__(self)
        self.room = []
        self.id = id
        self.pool = pool
        self.connect = None


    def send_message(self, text):
        self.connect.send(text.encode())
        print("Thread 0 send this to client:{1}".format(self.id, text))

    def readMessage(self):
        for t in self.room:
            roomRef = t[0]
            clientID = t[1]
            room = self.pool.state.rooms[roomRef]
            for index in range(len(room.message)):
                    if clientID in room.message[index][2]:
                        room.message[index][2].remove(clientID)
                        self.send_message("stringx")

            room.message[:] = [m for m in room.message if m[2]]

    def run(self):
        while not (self.pool.killService):
            if (len(self.pool.clients)) > 0:
                self.connect = self.pool.client.pop(0)
            if self.connect is None:
                continue
            print("Thread {0} got a client".format(self.id))
            self.associatedId = self.pool.state.ID_Counter
            self.pool.state.ID_Counter = self.pool.state.ID_Counter + 1
            self.readMessage()
            message = self.connect.recv(2048).decode().replace("\\n", '\n')
            print("Thread {0} received message {1}.".format(self.id, message.rstrip()))
            print("Thread {0} closing client socket".format(self.id))
            self.connect.close()
            self.connect = None
            print("Thread {0} dying".format(self.id))

    def constructReply(self, data):
        reply = "{0}IP:{1}\nPort:{2}\nStudentID:{3}\n".format(data, IP,
                                                              PORT, 17304420)
        return reply

    def constructJoinReply(self, roomName, roomRef, clientId):
        reply = ("JOINED_CHATROOM: {0}\n"
                 "SERVER_IP: {1}\n"
                 "PORT: {2}\n"
                 "ROOM_REF: {3}\n"
                 "JOIN_ID: {4}\n"
                 ).format(roomName, socket.gethostbyname(socket.gethostname()), PORT, roomRef, clientId)
        return reply

    def constructLeaveReply(self, roomRef, clientId):
        reply = ("LEFT_CHATROOM: {0}\n"
                 "JOIN_ID: {1}\n"
                 ).format(roomRef, clientId)
        return reply

    def constructMessage(self, roomRef, clientName, message):
        reply = ("CHAT: {0}\n"
                 "CLIENT_NAME: {1}\n"
                 "MESSAGE: {2}\n\n"
                 ).format(roomRef, clientName, message)
        return reply

    def process_message(self, message):
        if message == "KILL_SERVICE\n":
            self.pool.killService()
            return True
        elif message.startswith("HELO "):
            self.send_message("hello")
            return False

        elif message.startswith("JOIN_CHATROOM: "):
            roomName = message.splitlines()[0][len("JOIN_CHATROOM: "):]
            clientName = message.splitlines()[3][len("CLIENT_NAME: "):]
            clientID = self.associatedId

            if roomName in self.pool.state.rooms:
                roomRef = self.pool.state.roomRef[roomName]
            else:
                roomRef = self.pool.state.refCounter
                self.pool.state.roomRef[roomName] = roomRef
                self.pool.state.room[roomRef] = ChatRoom()
                self.pool.state.refCounter += 1
                room = self.pool.state.room[roomRef]

                joinMessage = "{0} has joined the chatroom".format(clientName)
                room.message.append([clientName, joinMessage, set(room.clients)])
                return False


class Pool():
    def __init__(self):
        self.process  = []
        self.client = []
        self.state = ChatInfo()
        self.threadCounter = 0
        self.kill = False
        for i in range(2):
            self.process.append(Process(self, self.threadCounter))
            self.process[i].start()
            self.threadCounter = self.threadCounter + 1

    def killService(self):
        self.kill = True

    def assignClient(self, connect):
        connect.setblocking(0)
        self.client.append(connect)


print("Loading...")
processPool = Pool()
serverThread = Server(processPool)
serverThread.start()
print("Server Started")

while True:
    if processPool.killService:
        for process in processPool.process:
            process.join()
        break
