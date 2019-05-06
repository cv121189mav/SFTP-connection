import pysftp

HOST: str = "test.rebex.net"
USERNAME: str = "demo"
PASSWORD: str = "password"


def back(server_state):
    state = "/".join(server_state.split('/')[:-2])
    if not state.endswith('/'):
        state += '/'
    return state


if __name__ == "__main__":
    with pysftp.Connection(host=HOST, username=USERNAME, password=PASSWORD) as server:
        server_state = server.pwd  # Current path in server
        while True:
            cmd = input("Enter command:  ")
            
            # Quit program
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
                    
            # Move step back
            if cmd == 'back':
                server_state = back(server_state)
                
            # Download file from server
            if cmd == 'd':
                filename = input('Filename: ')
                server.get("{}{}".format(server_state, filename))
    server.close()        
