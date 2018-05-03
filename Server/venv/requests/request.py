"""------------------------------------------------------------------------------
* class name: Requests
* file name: request.py
* author: Jathan
---------------------------------------------------------------------------------
* purpose: Class to hold the different commands for server use.
------------------------------------------------------------------------------"""

import json
import sqlalchemy
from enum import Enum
from .database.building import *
from .database.Class import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

engine = create_engine('mysql://bucboard:Raspberry314@127.0.0.1:3306/BucBoardProject')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Request(Enum):
    CONNECT = 0
    CLOSE = 1
    INSERT = 2
    UPDATE = 3
    SELECT = 4


class Requests(object):
    def __init__(self):
        self.commands = dict()
        self.conns = dict()

    def addRequest(self, key, request):
        self.commands[key] = request

    def removeRequest(self, key):
        del self.commands[key]

    def addConnection(self, key, conn, addr):
            self.conns[key] = (conn, addr)

    def removeConnection(self, key):
            self.conns[key][0].close()
            del self.conns[key]

#command to add connections to the server
class ConnectionRequest(object):

    @staticmethod
    def execute(key, conn, addr, request):
        #write connection code
        request.addConnection(key, conn, addr)
        print("I connected fine!!")

#command to close connections on the server
class CloseRequest(object):

    @staticmethod
    def execute(data, request):
        #write closing code
        addr = ""
        addr = addr.join(str(request.conns[data["key"]][1]))
        print("I closed the connection with: " + addr)
        request.removeConnection(data["key"])

#command to insert data into the database
class InsertRequest(object):

    @staticmethod
    def execute():
        #add code to insert
        new_session = Session()

        payload = request.conns[query["key"]][0].recv(4098)
        payload = payload.decode()
        payload = json.loads(payload)

        new_class = Class(
            name=payload['name'],
            crn=payload['crn'],
            section=payload['section'],
            start=payload['start'],
            end=payload['end'],
            professor=payload['professor'],
            room_num=payload['room_num']
        )

        session.add(new_class)
        session.commit()

        new_session.close()


#command to update database items
class UpdateRequest(object):

    @staticmethod
    def execute(conn, query, request):
        #add code to update

        new_session = Session()

        for row in new_session.query(building).all():
            payload = {
                "id": str(row.id),
                "name": str(row.name),
                "campus": str(row.campus),
                "message_type": Request.UPDATE.value
            }

            payload = json.dumps(payload)
            payload = payload.encode('utf-8')

            request.conns[query["key"]][0].send(payload)

            payload = request.conns[query["key"]][0].recv(4098)
            payload = payload.decode()
            payload = json.loads(payload)

        payload = {
            "message_type": Request.CLOSE.value
        }

        payload = json.dumps(payload)
        payload = payload.encode('utf-8')

        request.conns[query["key"]][0].send(payload)

        new_session.close()

#command to select from the database
class SelectRequest(object):

    @staticmethod
    def execute(conn, query, request):
        print("Sent message to: " + str(request.conns[query["key"]][1]))

        new_session = Session()

        if query['table'] == "building":
            table = Building

            for row in new_session.query(table).all():
                payload = {
                    "id": str(row.id),
                    "name": str(row.name),
                    "campus": str(row.campus),
                    "message_type": Request.UPDATE
                }

                payload = json.dumps(payload)
                payload = payload.encode('utf-8')

                request.conns[query["key"]][0].send(payload)

                payload = request.conns[query["key"]][0].recv(4098)
                payload = payload.decode()
                payload = json.loads(payload)

        elif query['table'] == "class":
            table = Class

            for row in new_session.query(table).all():
                payload = {
                    "id": str(row.id),
                    "name": str(row.name),
                    "crn": str(row.crn),
                    "section": str(row.crn),
                    "start": str(row.start),
                    "end": str(row.end),
                    "professor": str(row.professor),
                    "room_num": str(row.room_num),
                    "message_type": Request.UPDATE
                }

                payload = json.dumps(payload)
                payload = payload.encode('utf-8')

                request.conns[query["key"]][0].send(payload)

                payload = request.conns[query["key"]][0].recv(4098)
                payload = payload.decode()
                payload = json.loads(payload)

        payload = {
            "message_type": Request.CLOSE
        }

        payload = json.dumps(payload)
        payload = payload.encode('utf-8')

        request.conns[query["key"]][0].send(payload)

        new_session.close()
