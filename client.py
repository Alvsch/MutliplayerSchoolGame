import socket


HEADER = 10
IP = "127.0.0.1" #Change to server host IP address
PORT = 5555 #Change to same as server.py
ADDR = (IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def recv(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return recv_handler(msg, conn)

def recv_handler(msg, conn):
    msg = str(msg)

    args = msg.split(" ")
    command = args.pop(0).upper()
    if command == "PRINT":
        print(' '.join(args))
    elif command == "QUESTION":
        answer = input(' '.join(args) + ':\n')
        send(answer, conn)
    elif command == "ANSWER":
        print(' '.join(args))
        send("RECEIVED", conn)
    else:
        return msg


def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    return recv(conn)



while True:
    recv(client)