from Server.database.building import *
from Server.ServerAPI.serverconn import *
import json


def main():
    objects = []

    objects = select_all("building")

    print(objects)

    data = json

    data = {
        "id": "3",
        "name": "Gilbreath Hall",
        "campus": "1"
    }

    update("building", data)

    objects = select_all("building")

    print(objects)

if __name__ == '__main__':
    main()
