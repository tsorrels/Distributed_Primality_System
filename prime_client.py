import socket
import select
from config import *
from enum import Enum


class Scheduler(Enum):
    static = 1
    dynamic = 2


class Chunk(object):
    def __init__(self, index_in, start_in, end_in, server_in):
        self.index = index_in
        self.start = start_in
        self.end = end_in
        self.server = server_in
        self.complete = 0

class Server(object):
    def __init__(self, serverName, chunk):
        self.connected = False
        self.name = serverName
        self.socket = None
        self.currentChunk = chunk
        self.complete = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((serverName, PORT))
            self.connected = True
        except socket.error:
            print(serverName + " refused connection, removing from servers")
            

class Solution(object):
    def __init__(self):
        print("ran Solution init")
        self.primes = []
        self.begin = None
        self.end = None
        self.chunks = []
        self.serverNames = []
        self.servers = []
        self.progress = []
        self.scheduler = Scheduler.dynamic


    def buildChunks(self):
        pass


    def buildServers(self):
        for serverName in self.serverNames:
            newChunk = Chunk(None, None, None, None)
            server = Server(serverName, newChunk)
            self.servers.append(server)

    def initiate(self):
        pass



class Setup(object):
    def __init__(self, solution_in):
        print ("ran status init")
        self.solution = solution_in
        self.finished = False


    def display(self):
        print ("________________________________________________________")
        print ("Status")
        print("Current servers:")
        if (self.solution.serverNames):
            for server in self.solution.serverNames:
                print("\t", server)
        else:
            print("\tNone - enter 'a' to add a server")
            
        print ("Range to search:")
        print ("\tStart:", end = " ")
        if (self.solution.begin):
            print (self.solution.begin)
        else:
            print ("Not set - enter 'b' to set start of range")
        print ("\tEnd:", end = " ")
        if (self.solution.end):
            print (self.solution.end)
        else:
            print ("Not set - enter 'e' to set end of range")

        print ("Scheduler: ", self.solution.scheduler)



    def printMenu(self):
        print("\n")
        print("Enter:")
        print("\t'a' to add a server")
        print("\t'b' to set beginning of range")
        print("\t'e' to set end of range")
        print("\t's' to set scheduler")
        print("\t'l' to launch")
        print("\t'q' to quit")
        print(">>>", end = " ")


    def getInput(self):
        while not self.finished:
            self.display()
            self.printMenu()
            userInput = input()
            userFunction = self.matchInput(userInput)
            if (userFunction):
                userFunction()

            else:
                print("Command not recognized")


    def matchInput(self, input):
        switch = {
            'a' : self.addServer,
            'b' : self.setBegin,
            'e' : self.setEnd,
            's' : self.setScheduler,
            'l' : self.launch,
            'q' : exit
        }
        return switch.get(input, None)


    def setBegin(self):
        print("Enter numeric value for beginning of range go search: ", end ='')
        userInput = input()
        try:
            val = int(userInput)
            self.solution.begin = val
        except Valueerror:
            print("Error: entry must be a number")

    def setEnd(self):
        print("Enter numeric value for end of range go search: ", end ='')
        userInput = input()
        try:
            val = int(userInput)
            self.solution.end = val
        except Valueerror:
            print("Error: entry must be a number")

    def addServer(self):
        print("Enter an ipv4 address or name of server to add:", end = " ")
        serverName = input()
        self.solution.serverNames.append(serverName)

    def setScheduler(self):
        print ("Enter 's' for static or 'd' for dynamic: ", end = " ")
        schedInput = input()
        if schedInput == 's':
            self.solution.scheduler = Scheduler.static

        elif schedInput == 'd':
            self.solution.scheduler = Scheduler.dynamic

        else:
            print ("Input must be 's' or 'd'")


    def launch(self):
        print ("Skipping conditions check")
        self.finished = True

    

def main():
    print ("running in main")

    complete = False

    solutionObject = Solution()
    setupObject = Setup(solutionObject)
    setupObject.getInput()
    
    # ready to launch
    solutionObject.buildChunks()
    solutionObject.buildServers()
    solutionObject.initiate()

    while not complete:
        pass

    # create as many sockets as necessary

    # chop up pieces, make solution object



if __name__ == "__main__":
    main()
