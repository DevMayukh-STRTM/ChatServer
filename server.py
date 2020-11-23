import socket
import threading

host = '0.0.0.0'
port = 8080

ADDR = (host, port)

server = socket.socket()
server.bind(ADDR)

server.listen()

clients = []
nicknames = []

def broadcast(code):
    for x in clients:
        x.send(code)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} Left the Chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def start():
    while True:
        client, address = server.accept()
        print(f'{address}: Connected | {client}')
        client.send('NICK'.encode('ascii'))
        x = client.recv(1024)
        nicknames.append(x)
        clients.append(client)

        broadcast(f'{x} Joined The Chat'.encode('ascii'))
        client.send('You Are Now Connected'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

print("Started Chat Server")
start()
