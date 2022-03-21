import socket 
import threading
import time as t
import msgpack
import random
import sys
import time

PORT = 5050
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
FORWARD_MESSAGE = "!F"
TURN_MESSAGE = "!T"
CHECK_MESSAGE = "!C"


def move_forward():
    t.sleep(2)
    print("moving forward")

def turn():
    t.sleep(2)
    print("turning")

def check_front():
    t.sleep(1)
    check = 1
    print("Check for Object")
    return check

def hamster(conn, addr):
    
    msg = None
    try:
        msg = conn.recv(4096).decode(FORMAT)
    except Exception:
        print("[{}]: Connection Lost!".format(addr))
        conn.close()
        return
            
    if msg == None:
        print("[{}]: Empty message.".format(addr))
        conn.close()
        return
           
    elif msg == DISCONNECT_MESSAGE:
        print("[{}]: Disconnected \nShutting down...".format(addr))
        conn.close()
        quit() 
            # use os to shutdown pi?
            
    else:
        if msg == FORWARD_MESSAGE: 
            move_forward()

        elif msg == TURN_MESSAGE: 
            turn()

        elif msg == CHECK_MESSAGE:
            msg = check_front()
                
    answer = str(msg).encode(FORMAT)
    try: conn.send(answer)
    except ConnectionResetError:
        print("Connection reset, cannot reply.")
    conn.close()
    



if __name__ == "__main__":
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print("Hamster is ready!")
    
    while True:
        conn, addr = server.accept()
        hamster(conn, addr)
