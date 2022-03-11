from email import message
import socket
import threading

from flask import g
from game import Game

HEADER = 10
IP = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (IP, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

games = {}
idCount = 0

def get_math_question():
    answer = "2"
    question = "1 + 1"

    return question, answer

def recv(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg

def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    return recv(conn)


def handle_client(conn, addr, p, gameId):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        if games[gameId].p1Went and games[gameId].p2Went:
            if games[gameId].winner == p:
                send("ANSWER You Won")
            else:
                send("ANSWER You Lost")

            games[gameId].p1Went = False
            games[gameId].p2Went = False
        else:
            if games[gameId].sentAnswer == False:
                question = get_math_question()
                answer = send(f"QUESTION {question[0]}", conn)
                if p == 0:
                    games[gameId].answers = [answer, games[gameId.answers[1]]]
                    games[gameId].p1Went = True
                    if games[gameId].answers[0] == question[1]:
                        if games[gameId].winner != -1:
                            games[gameId].winner = 0
                else:
                    games[gameId].answers = [games[gameId.answers[0]], answer]
                    games[gameId].p2Went = True
                    if games[gameId].answers[1] == question[1]:
                        if games[gameId].winner != -1:
                            games[gameId].winner = 1


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}")
    while True:
        conn, addr = server.accept()
        idCount += 1
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            p = 1

        thread = threading.Thread(target=handle_client, args=(conn, addr, p, gameId))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start() 
