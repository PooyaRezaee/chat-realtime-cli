import socket
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init()

users = {}  # Dictionary user and object connection
users_pool = ThreadPoolExecutor(max_workers=10)
PORT = 8001


def read_data(data: bytes) -> (dict, str):
    """data must be have 2 part header and body
    sample message:
        for_user:sajad

        This is my message
    """
    string_data = data.decode()
    header, body = string_data.split("\n\n")
    header = header.strip().split("\n")
    body = body.strip()

    dict_header = {}
    for item in header:
        key, value = item.split(":")
        dict_header[key] = value

    return dict_header, body


def user_message_handler(name, conn: socket.socket, addr=None):
    print(Fore.GREEN + f"User with name '{name}' and address '{addr}' activate")
    while True:
        try:
            data = conn.recv(1024)
            header, body = read_data(data)
            if body == "$exit":
                break
            target_user = header["for_user"]
            users[target_user].send(f"{name} -> {body}".encode())
        except KeyError as k:
            print(Fore.LIGHTRED_EX + f"User message Error : User {k} Don't exist")
            conn.send(f"user {k} don't exist".encode())
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"User message Error : {e}")
            conn.send("Bad Message".encode())
    print(Fore.RED + f"User with name '{name}' and address '{addr}' exited")
    conn.close()


def connection_users_control(s: socket.socket):
    """Control users for add to dictionary of users
    Expected message to join -> Join@{name}

    """
    print(Fore.MAGENTA + "Server is Ready for accept Connection")
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)

        try:
            command, name = data.decode().split("@")
            if command == "Join":
                users[name] = conn
                users_pool.submit(user_message_handler, name=name, conn=conn, addr=addr)
                conn.send("Successful joined.".encode())
            else:
                conn.send("Bad command".encode())
                conn.close()
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Bad Join message")
            conn.send("Bad message".encode())
            conn.close()


def main():
    print(Fore.YELLOW + "Initilizing ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = "", PORT
        s.bind(addr)
        s.listen(10)

        control_connections = Thread(target=connection_users_control, args=[s])
        control_connections.start()

        control_connections.join()


if __name__ == "__main__":
    main()
