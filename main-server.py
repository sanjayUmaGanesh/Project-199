import socket 
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address  = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

clients = []
print("Server is running")

questions = ['When do we celebrate independence day in India? a)15th August b) 1st April c) 30th Feb d) All of the above '
            ,'What should you do if masked man offers you a chocolate if you go home with him? a) Dance b) Go with him c) Shoot him d) Refuse the offer and tell your mom'
            ,'Who is the prime minister of India(sorry could not think of a better question :|)? a) Jshlatt b) Narendra Modi c) Mick Gordon d) Dj Blyatman'
            ]

answers = ['a', 'd', 'b']

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def broadcast(message,connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove(client)


def picker(conn):
    pick = random.randint(0,len(questions)-1)
    pick_question = questions[pick]
    pick_answer = questions[pick]

    return pick, pick_question, pick_answer
    
def popper(question,answer):
    questions.pop(question)
    answer.pop(answer)


def clientThread(conn,):
    score = 0
    conn.send("         WELCOME TO THE SUPER HARD QUIZ   !!!".encode("utf-8"))
    conn.send("_____________________________________________________".encode("utf-8"))
    conn.send("         WE ASK QUESTIONS AND YOU ANSWER".encode("utf-8"))
    conn.send(" IF ANSWER WRONG WE WILL COME TO YOUR HOUSE AND SHOOT YOU (JUST KIDDING)".encode("utf-8"))

    chosen_one,question,answer = picker(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send("That's the right answer :). Your score is {score}\n\n".encode("utf-8"))

                else:
                    conn.send("NOPE (0 _ 0)".encode("utf-8"))
                popper(chosen_one, answer)
                chosen_one,question,answer = picker(conn)

            else:
                remove(conn)
                
        except:
            continue





while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')

    clients.append(conn)
    #nicknames.append(nickname)
    message = "{} joined this server!".format(nickname)

    print(addr[0]+" connected")
    print(message)

    broadcast(message,conn)

    new_thread = Thread(target= clientThread,args = (conn,addr))
    new_thread.start()

    broadcast(message,conn)