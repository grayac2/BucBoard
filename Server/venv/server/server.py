import socket
from requests.request import *
from enum import Enum
import json
import threading

class Request(Enum):
    CONNECT = 0
    CLOSE = 1
    INSERT = 2
    UPDATE = 3
    SELECT = 4


request = Requests()
conn_id = 0


def acceptconnections(server_socket):
    global conn_id
    global request

    conn, addr = server_socket.accept()

    request.commands[Request.CONNECT.value].execute(str(conn_id), conn, addr,  request)

    payload = {
        "key": str(conn_id)
    }

    connection, addr = request.conns[str(conn_id)]

    payload = json.dumps(payload)
    payload = payload.encode('utf-8')

    connection.send(payload)

    conn_id += 1

    print("Connection from " + str(addr))

    newthread = threading.Thread(name=addr, target=handlerequest, args=(conn, addr))
    newthread.start()


def handlerequest(conn, addr):
    while True:
        data = conn.recv(4098)
        data = data.decode()
        data = json.loads(data)

        if data['messagetype'] == Request.CLOSE.value:
            request.commands[data['messagetype']].execute(data, request)
            break

        request.commands[data['messagetype']].execute(conn, data, request)

    conn.close()

def Main():

    host = '172.31.64.211'
    port = 1337

    #instantiate the command pattern to handle requests and add commands
    request.addRequest(Request.CONNECT.value, ConnectionRequest)
    request.addRequest(Request.CLOSE.value, CloseRequest)
    request.addRequest(Request.INSERT.value, InsertRequest)
    request.addRequest(Request.UPDATE.value, UpdateRequest)
    request.addRequest(Request.SELECT.value, SelectRequest)

    #setup socket to listen on
    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(5)
    print("Server started and waiting on connections...")

    while True:
        acceptconnections(server_socket)


if __name__ == '__main__':
    Main()
