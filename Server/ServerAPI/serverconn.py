

import socket
import json
from enum import Enum


class Request(Enum):
    CONNECT = 0
    CLOSE = 1
    INSERT = 2
    UPDATE = 3
    SELECT = 4


def select_all(table):
    #Host and port to connect to
    host = '34.207.93.186'
    port = 1337

    #Variable to hold list of JSON objects
    db_list = []

    #Create Socket and connect
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((host, port))

    receive = my_socket.recv(4098)
    receive = receive.decode()
    receive = json.loads(receive)

    #Create initial payload variable to be sent
    payload = {
        "messagetype": Request.SELECT.value,
        "table": table,
        "key": receive['key']
    }

    key = receive['key']

    #Format the json object and send across the socket
    payload = json.dumps(payload)
    my_socket.send(payload.encode('utf-8'))

    #Loop through and get all messages returned from server
    while True:
        receive = my_socket.recv(4098)
        receive = receive.decode()
        receive = json.loads(receive)

        db_list.append(receive)

        if receive["message_type"] == 1:
            break
        else:
            payload = {
                "messagetype": Request.SELECT.value
            }

            payload = json.dumps(payload)
            my_socket.send(payload.encode('utf-8'))
        #End if
    #End Loop

    #Send quit payload
    payload = {
        "messagetype": Request.CLOSE.value,
        "key": key
    }

    #Send the quit payload
    payload = json.dumps(payload)
    my_socket.send(payload.encode('utf-8'))

    #Close the socket
    my_socket.close()

    #Return list of JSON objects
    return db_list


def insert(table, data):
    # Host and port to connect to
    host = '34.207.93.186'
    port = 1337

    # Variable to hold list of JSON objects
    db_list = []

    # Create Socket and connect
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((host, port))

    receive = my_socket.recv(4098)
    receive = receive.decode()
    receive = json.loads(receive)

    key = receive['key']

    if table == "class":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "name": data['name'],
            "crn": data['crn'],
            "section": data['section'],
            "start": data['start'],
            "end": data['end'],
            "professor": data['professor'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "announcements":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "title": data['title'],
            "info": data['info'],
            "image": data['image'],
            "professor": data['professor'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "building":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "name": data['name'],
            "campus": data['campus'],
            "key": receive['key']
        }

    elif table == "campus":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "city": data['city'],
            "state": data['state'],
            "name": data['name'],
            "key": receive['key']
        }

    elif table == "events":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "name": data['name'],
            "host": data['host'],
            "image": data['image'],
            "start": data['start'],
            "end": data['end'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "office_hours":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "start": data['start'],
            "end": data['end'],
            "professor": data['professor'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "room":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "type": data['type'],
            "room_num": data['room_num'],
            "building": data['building'],
            "key": receive['key']
        }

    elif table == "user":
        payload = {
            "messagetype": Request.INSERT.value,
            "table": table,
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "prefix": data['prefix'],
            "office": data['office'],
            "key": receive['key']
        }

    # Format the json object and send across the socket
    payload = json.dumps(payload)
    my_socket.send(payload.encode('utf-8'))

    # Close the socket
    my_socket.close()

def update(table, data):
    # Host and port to connect to
    host = '34.207.93.186'
    port = 1337

    # Variable to hold list of JSON objects
    db_list = []

    # Create Socket and connect
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((host, port))

    receive = my_socket.recv(4098)
    receive = receive.decode()
    receive = json.loads(receive)

    key = receive['key']

    if table == "class":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "name": data['name'],
            "crn": data['crn'],
            "section": data['section'],
            "start": data['start'],
            "end": data['end'],
            "professor": data['professor'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "announcements":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "title": data['title'],
            "info": data['info'],
            "image": data['image'],
            "professor": data['professor'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "building":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "name": data['name'],
            "campus": data['campus'],
            "key": receive['key']
        }

    elif table == "campus":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "city": data['city'],
            "state": data['state'],
            "name": data['name'],
            "key": receive['key']
        }

    elif table == "events":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "name": data['name'],
            "host": data['host'],
            "image": data['image'],
            "start": data['start'],
            "end": data['end'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "office_hours":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "start": data['start'],
            "end": data['end'],
            "professor": data['professor'],
            "room_num": data['room_num'],
            "key": receive['key']
        }

    elif table == "room":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "type": data['type'],
            "room_num": data['room_num'],
            "building": data['building'],
            "key": receive['key']
        }

    elif table == "user":
        payload = {
            "messagetype": Request.UPDATE.value,
            "table": table,
            "id": data['id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "prefix": data['prefix'],
            "office": data['office'],
            "key": receive['key']
        }

    # Format the json object and send across the socket
    payload = json.dumps(payload)
    my_socket.send(payload.encode('utf-8'))

    # Close the socket
    my_socket.close()