import socket
import time
from threading import Thread
from colorama import Fore, init
import os


init()

messages = []
for_user = None
RUNNING = True


def print_page(msg, clear_input=False):
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
    while RUNNING:
        try:
            data = s.recv(1024)
            print_page(data.decode())
        except (KeyboardInterrupt, OSError):
            pass


def main(name, addr):
    global for_user
    global RUNNING

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        s.send(f"Join@{name}".encode())

        thread = Thread(target=reiving_data, args=[s])
        thread.start()

        while RUNNING:
            try:
                for_user = input(Fore.LIGHTCYAN_EX + "for > ")
                message = input(Fore.LIGHTCYAN_EX + "Message > ")
                if for_user == "exit" and message == "exit":
                    raise KeyboardInterrupt
                s.send(generate_data_message(message, for_user=for_user))
                for_user = None
                print_page("", clear_input=True)
                time.sleep(0.1)
            except (KeyboardInterrupt, OSError):
                s.send(generate_data_message("$exit", for_user="server"))
                RUNNING = False


if __name__ == "__main__":
    HOST = input(Fore.MAGENTA + "Enter IP v4 Server : ")
    PORT = int(input("Enter Port Server : "))
    main(input("Enter Your Name: "), (HOST, PORT))
