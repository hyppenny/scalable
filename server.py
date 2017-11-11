import socket, sys
from threading import Thread

# if (len(sys.argv) < 3):
#     print("Server usage: python server.py IP PORT")
#     sys.exit(0)

PORT = 5555  # sys.argv[2]
IP = "127.0.0.1"


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
            print("Server received client connection and added it to queue")
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

    def readmessage(self):
        for t in self.room:
            roomRef = t[0]
            clientId = t[1]
            room = self.pool.state.room[roomRef]
            for index in range(len(room.message)):
                if clientId in room.message[index][2]:
                    room.message[index][2].remove(clientId)
                    self.send_message(self.constructMessage(roomRef, room.message[index][0], room.message[index][1]))
            room.message[:] = [m for m in room.message if m[2]]

    def run(self):
        while not (self.pool.kill):
            if (len(self.pool.client) > 0 and not (self.pool.kill)):
                self.connect = self.pool.client.pop(0)
            if self.connect is None:
                continue
            print("Thread {0} got a client".format(self.id))
            self.associatedId = self.pool.state.ID_Counter
            self.pool.state.ID_Counter += 1
            self.readmessage()
            message = self.connect.recv(2048).decode().replace("\\n", '\n')
            print("Thread {0} received message {1}".format(self.id, message.rstrip()))
            if self.process_message(message):
                break
            print("Thread {0} closing client socket".format(self.id))
            self.connect.close()
            self.connect = None
        print("Thread {0} dying".format(self.id))

    def constructReply(self, message):
        reply = "HELO {0}\nIP:{1}\nPort:{2}\nStudentID:{3}\n".format(message, IP,
                                                                     PORT, 17304420)
        return reply

    def constructJoinReply(self, roomName, roomRef, clientId):
        reply = ("JOINED_CHATROOM: {0}\n"
                 "SERVER_IP: {1}\n"
                 "PORT: {2}\n"
                 "ROOM_REF: {3}\n"
                 "JOIN_ID: {4}\n"
                 ).format(roomName, IP, PORT, roomRef, clientId)
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
            self.pool.kill()
            return True
        elif message.startswith("HELO "):
            self.send_message(self.constructReply(message[len("HELO "):].rstrip()))
            return False

        elif message.startswith("JOIN_CHATROOM: "):
            roomName = message.splitlines()[0][len("JOIN_CHATROOM: "):]
            clientName = message.splitlines()[3][len("CLIENT_NAME: "):]
            clientId = self.associatedId
            if roomName in self.pool.state.roomRef:
                roomRef = self.pool.state.roomRef[roomName]
            else:
                roomRef = self.pool.state.REF_Counter
                self.pool.state.roomRef[roomName] = roomRef
                self.pool.state.room[roomRef] = ChatRoom()
                self.pool.state.REF_Counter += 1
                room = self.pool.state.room[roomRef]
                room.client.append(clientId)
            joinMessage = "{0} has joined the chatroom".format(clientName)
            room.message.append([clientName, joinMessage, set(room.client)])

            self.room.append((roomRef, clientId))
            print(roomName, roomRef, clientId, "!!!")
            self.send_message(self.constructJoinReply(roomName, roomRef, clientId))
            return False

        elif message.startswith("LEAVE_CHATROOM: "):
            roomRef = int(message.splitlines()[0][len("LEAVE_CHATROOM: "):])
            clientId = int(message.splitlines()[1][len("JOIN_ID: "):])
            clientName = message.splitlines()[2][len("CLIENT_NAME: "):]

            if (roomRef, clientId) in self.room:
                room = self.pool.state.room[roomRef]
                for index in range(len(room.message)):
                    if clientId in room.message[index][2]:
                        room.message[index][2].remove(clientId)
                room.message[:] = [m for m in room.message if m[2]]
                room.client.remove(clientId)
                leaveMessage = "{0} has left the chatroom".format(clientName)
                if (len(room.client) > 0):
                    room.message.append([clientName, leaveMessage, set(room.client)])

            self.send_message(self.constructLeaveReply(roomRef, clientId))
            if (roomRef, clientId) in self.room:
                self.send_message(self.constructMessage(roomRef, clientName, leaveMessage))
                self.room.remove((roomRef, clientId))

            return False

        elif message.startswith("CHAT: "):
            roomRef = int(message.splitlines()[0][len("CHAT: "):])
            clientId = int(message.splitlines()[1][len("JOIN_ID: "):])
            clientName = message.splitlines()[2][len("CLIENT_NAME: "):]
            message = message.splitlines()[3][len("MESSAGE: "):]

            room = self.pool.state.room[roomRef]
            if (len(room.client) > 0):
                room.message.append([clientName, message, set(room.client)])
            return False

        elif message.startswith("DISCONNECT: "):
            clientName = message.splitlines()[2][len("CLIENT_NAME: "):]

            for t in self.room:
                roomRef = t[0]
                clientId = t[1]
                room = self.pool.state.room[roomRef]
                for index in range(len(room.message)):
                    if clientId in room.message[index][2]:
                        room.message[index][2].remove(clientId)
                room.message[:] = [m for m in room.message if m[2]]
                room.client.remove(clientId)
                discMessage = "{0} was disconnected".format(clientName)
                if (len(room.client) > 0):
                    room.message.append([clientName, discMessage, set(room.client)])
                self.send_message(self.constructMessage(roomRef, clientName, discMessage))

            self.room = []
            return True


class Pool():
    def __init__(self):
        self.process = []
        self.client = []
        self.state = ChatInfo()
        self.threadCounter = 0
        self.kill = False
        for i in range(2):
            self.process.append(Process(self, self.threadCounter))
            self.process[i].start()
            self.threadCounter = self.threadCounter + 1

    def kill(self):
        self.kill = True

    def assignClient(self, conn):
        conn.setblocking(0)
        self.client.append(conn)


print("Loading...")
processPool = Pool()
serverThread = Server(processPool)
serverThread.start()
print("Server Started")

while True:
    if processPool.kill:
        for worker in processPool.process:
            worker.join()
        break
