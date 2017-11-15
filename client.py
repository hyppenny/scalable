import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(("127.0.0.1",5555))


# sock.send(b"HELO \n")
#sock.send(b"KILL_SERVICE\n")
sock.send(b'JOIN_CHATROOM: ROOM1\n' + b'CLIENT_IP: 127.0.0.1\n' + b'PORT: 5555\n' + b'CLIENT_NAME: C1\n')
# sock.send(b'LEAVE_CHATROOM: 0\n' + b'JOIN_ID: 0\n' + b'CLIENT_NAME: C1\n')
#sock.send(b'CHAT: 0\n' + b'JOIN_ID: 0\n' + b'CLIENT_NAME: C1\n' + b'MESSAGE: ooo\n')
print(sock.recv(2048).decode())