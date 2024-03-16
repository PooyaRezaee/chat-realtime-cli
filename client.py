import socket
import time
from threading import Thread
from colorama import Fore, init
import os


init()
PORT = 8001
HOST = "127.0.0.1"

messages = []
for_user = None


def print_page(msg,clear_input=False):
    os.system("clear")
    messages.append(msg)
    text = ""
    for message in messages:
        text += Fore.CYAN + message + "\n"

    text += Fore.YELLOW + "\n-----------------\n"

    if not clear_input:
        if for_user is None:
            text += Fore.LIGHTCYAN_EX + "for > "
        else:
            text += Fore.LIGHTCYAN_EX + "for > " + f"{for_user}\n"
            text += Fore.LIGHTCYAN_EX + "Message > "

    print(text, end="")


def generate_data_message(message, **kwargs):
    data = ""
    for k, v in kwargs.items():
        data += f"{k}:{v}\n"

    data += "\n"

    data += message
    return data.encode()


def reiving_data(s: socket.socket):
    while True:
        data = s.recv(1024)
        print_page(data.decode())


def main(name):
    global for_user

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(f"Join@{name}".encode())

        thread = Thread(target=reiving_data, args=[s])
        thread.start()

        while True:
            for_user = input(Fore.LIGHTCYAN_EX + "for > ")
            message = input(Fore.LIGHTCYAN_EX + "Message > ")
            s.send(generate_data_message(message, for_user=for_user))
            for_user = None
            print_page('',clear_input=True)
            time.sleep(0.1)


if __name__ == "__main__":
    main(input(Fore.MAGENTA + "Enter Your Name: "))
