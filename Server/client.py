from enum import Enum
import datetime
from Server.ServerAPI import serverconn

class Request(Enum):
    CONNECT = 0
    CLOSE = 1
    INSERT = 2
    UPDATE = 3
    SELECT = 4

def Main():
    data = {
        "name": "Web Design",
        "crn": "1710",
        "section": "001",
        "start": datetime.now(),
        "end": datetime.now(),
        "professor": "2",
        "room_num": "2"
    }

    insert("class", data)

if __name__ == '__main__':
    Main()