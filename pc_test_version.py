import socket
import msgpack
import threading
import time as t
import os
import sys

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!D"
FORWARD_MESSAGE = "!F"
TURN_MESSAGE = "!T"
IP = "127.0.0.1"
PORT = 5050
status_running = True


if sys.version_info < (3, 6):
    print("Es wird eine Python Version 3.6 oder höher benötigt!")
    quit()      

class Master():
    def __init__(self, ip, port):
        self.__address = (ip, port)
        self.__message = ""
        self.__connection_status = "Connection Lost!"

    def __str__(self):
        x = ""
        
        x = self.__connection_status + " " + self.__message
 
        return x

    def establish_connection(self):
        while status_running:
            try:
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.connect(self.__address)
                self.__connection_status = "connection established"
                self.__sock.settimeout(10)
                print("connection establsiehd")
                break
            except ConnectionRefusedError:
                self.__connection_status = "connection refused"
                print("katastrophe")
                t.sleep(5)
                continue
            
    
    def send_msg(self, msg):
        #self.establish_connection()
        message = msg.encode(FORMAT)
        try: 
            self.__sock.send(message)
            print("msgsent")
            answer = self.__sock.recv(4096).decode(FORMAT)
            print(answer)
        except ConnectionResetError:
            print("connection reset during send, try again")
            self.establish_connection()
            self.send_msg(msg)
            """self.__sock.send(message)
            print("msgsent")
            answer = self.__sock.recv(4096).decode(FORMAT)
            print(answer)"""
        except socket.timeout:
            print("connection lost during send, try again")
            self.establish_connection()
            self.send_msg(msg)
            """self.__sock.send(message)
            print("msgsent")
            answer = self.__sock.recv(4096)
            answer = answer.decode(FORMAT)
            print(answer)"""
            


    def forward(self):
        self.send_msg(FORWARD_MESSAGE)

    def turn(self):
        self.send_msg(TURN_MESSAGE)

    def disconnect(self):
        self.send_msg(DISCONNECT_MESSAGE)
    
#def check_status:


try:
    print("probier ma moul")
    my_master = Master(IP, PORT)
    print("sall hent gang")
    my_master.establish_connection() #des in eigene thread?
    print("sall got ou")


    if __name__ == "__main__":
        while 1:
            print("while 1")
            try:
                my_master.forward()
                print("forward sent")
                print(my_master)
                print("\n")
                
                my_master.turn()
                print("turn sent")
                print(my_master)
                print("\n")
                
            

            except ConnectionRefusedError:
                print("some error occured, trying again")
                t.sleep(1)
                pass
    #my_master.send_msg(DISCONNECT_MESSAGE)
    #status_running = False
finally:
    print("finally")