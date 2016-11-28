from config import *
import multiprocessing
import socket
import json
import select
#from enum import Enum


class ServerSolution(object):
    def __init__(self, begin_in, end_in):
        self.begin = begin_in
        self.end = end_in
        self.primes = []

    def findPrimes(self):
        print("Searching for primes between",self.begin, "and", self.end)
        self.primes.append(1)
        self.primes.append(3)


def processMessage(message, clientSocket):
    if message.message_type == "begin":
        solution = ServerSolution(message.data[0], message.data[1])
        solution.findPrimes()
        solutionMessage = Message("solution", solution.primes)
        print ("Returning solution", solution.primes)
        mess = MessageEncoder().encode(solutionMessage)
        sendMessage(clientSocket, mess)      

    else:
        print("received message other than type 'begin'")


def main():
    run = True

    print(PORT)

    # set up server socket-
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversocket.bind((socket.gethostname(), PORT))
    serversocket.bind(('', PORT))
    serversocket.listen(5)

    while(run):
        (clientSocket, address) = serversocket.accept()
        ready_to_read, ready_to_write, error = \
                select.select ([clientSocket], [], [])

        if (ready_to_read):
            message = recvMessage(clientSocket)
            print ("received message ", message)
            processMessage(message, clientSocket)


if __name__ == "__main__":
    main()
