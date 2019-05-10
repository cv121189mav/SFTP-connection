import json
import pysftp

db: dict = {}

FILENAME = 'db.json'


class DictToJson:

    @staticmethod
    def write_update(filename: str, db: dict):
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(db))


class JsonToDict:
    @staticmethod
    def get_data(filename: str) -> dict:
        with open(filename, 'r') as json_file:
            return json.loads(json_file.read())


class ShowInfo:
    @staticmethod
    def show_data(db: dict):
        for key in db:
            print("Connection name ", key, db[key])


class Connections:

    def update_or_create_connection(filename: str, db: dict):
        input_index = input("Input connection name: ")
        if input_index in db:
            host = input("updated host")
            name = input("updated name")
            password = input('updated password')
            db[input_index] = {"host": host, 'name': name, 'password': password}
        else:
            print('there now user name, create new user?')
            answer = input("y/n")
            if answer == 'y':
                input_index = input("Input new connection name: ")
                host = input("new host")
                name = input("new name")
                password = input('new password')
                db[input_index] = {"host": host, 'name': name, 'password': password}

        DictToJson.write_update(filename, db)

    def remove_connection(filename: str, db: dict):
        input_remove = input("Index for remove: ")
        del db[input_remove]

        DictToJson.write_update(filename, db)


class Connector:

    def back(server_state):
        state = "/".join(server_state.split('/')[:-2])
        if not state.endswith('/'):
            state += '/'
        return state




    db = JsonToDict.get_data(FILENAME)
    while True:
        cmd = input("Enter command: ")

        if cmd == "show":
            ShowInfo.show_data(db)
        if cmd == 'u':
            Connections.update_or_create_connection(FILENAME, db)
        if cmd == "del":
            Connections.remove_connection(FILENAME, db)
        if cmd == "q":
            break
        if cmd == "connect":
            choose_connection = input("Choose connection")
            get_value = db.get(choose_connection)

            with pysftp.Connection(host=get_value['host'], username=get_value['name'], password=get_value['password']) as server:
                server_state = server.pwd  # Current path in server
                while True:
                    cmd = input("Enter command:  ")
                    # Quite program
                    if cmd == 'q':
                        break
                    # List folders and files
                    if cmd == 'ls':
                        print(server.listdir(server_state))
                    # Current path in server
                    if cmd == 'pwd':
                        print('path: ', server_state)
                    # Change directory
                    if cmd == 'cd':
                        print(server.listdir(server_state))
                        path = input('Enter folder for change: ')
                        if server.isdir("{}{}/".format(server_state, path)):
                            server_state = "{}{}/".format(server_state, path)
                        else:
                            print("Folder not found")
                    # Move to back
                    if cmd == 'back':
                        server_state = back(server_state)
                    # Download file from server
                    if cmd == 'd':
                        filename = input('Filename: ')
                        server.get("{}{}".format(server_state, filename))
