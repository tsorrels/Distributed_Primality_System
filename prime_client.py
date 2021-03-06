import json
import socket
import select
import math
import struct
import time
import sys
from config import *


class Scheduler(Enum):
    static = 1
    dynamic = 2


class Chunk(object):
    def __init__(self, start_in, end_in, index_in = None, server_in = None):
        self.index = index_in
        self.start = start_in
        self.end = end_in
        self.server = server_in
        self.scheduled = False
        self.complete = False
        self.timeStart = None
        self.timeFinish = None

class Server(object):
    def __init__(self, serverName, chunk):
        self.status = ServerStatus.idle
        self.connected = False
        self.name = serverName
        self.socket = None
        self.currentChunk = chunk
        self.currentChunkID = -1
        self.complete = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            print("connecting to", end = " ")
            print (self.name)
            self.socket.connect((self.name, PORT))
            self.connected = True
        except socket.error:
            print(self.name + " refused connection, removing from servers")
            return False
        return True
            

class Solution(object):
    def __init__(self):
        self.primes = []
        self.begin = 100000#None
        self.end = 110000#None
        self.chunks = []
        self.serverNames = []
        self.servers = []
        self.progress = []
        self.scheduler = Scheduler.dynamic
        self.timeStart = None 
        self.timeFinish = None


    def getNextChunk(self):
        for chunk in self.chunks:
            if chunk.scheduled == False:
                return chunk
        return False

    def checkCompletion(self):
        returnValue = True
        for chunk in self.chunks:
            if chunk.complete == False:
                returnValue = False
                break;
        return returnValue


    def printSolution(self):
        self.primes.sort()
        print("Computation complete")
        print ("Elapsed time:", "{0:.2f}".format(
            self.timeFinish - self.timeStart), 
               "seconds")

        print("Primes in range", self.begin, "and", self.end, ":")
        print(self.primes)
              


    def buildChunks(self):
        numChunks = len(self.serverNames)
        if (self.scheduler == Scheduler.dynamic):
            numChunks = numChunks * CHUNK_FACTOR

        rangeVal = math.ceil( (self.end - self.begin) / numChunks)

        for i in range(0, numChunks):
            chunkStart = int(self.begin + (i * rangeVal))
            chunkEnd = chunkStart + rangeVal - 1
            if (i == numChunks - 1):
                chunkEnd = self.end
            #print("Chunk start, end ", chunkStart, chunkEnd)
            self.chunks.append(Chunk(chunkStart, chunkEnd, i))


    def buildServers(self):
        for serverName in self.serverNames:
            newChunk = Chunk(None, None, None, None)
            server = Server(serverName, newChunk)
            if server.connect():
                self.servers.append(server)

    def initiate(self):
        #print (len(self.servers))
        self.timeStart = time.time()
        for i in range (0, len(self.servers)):
            currentChunk = self.chunks[i]
            # assign first chunk to server
            self.servers[i].currentChunk = currentChunk
            print ("sending server",i, "chunk index",i)


            messObj = Message("begin", (currentChunk.start,
                                        currentChunk.end), 
                              currentChunk.index)
            jsonString = MessageEncoder().encode(messObj)
            #print(jsonString)
            #length = len(jsonString)

            # mark chunk as scheduled
            currentChunk.scheduled = True
            currentChunk.timeStart = time.time()
            sendMessage(self.servers[i].socket, jsonString)



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

        print ("Scheduler: ", self.solution.scheduler.name)



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

    
def processMessage(message, solution, socket):
    serverIndex = -1

    for i in range(0, len(solution.servers)):
        if solution.servers[i].socket == socket:
            serverIndex = i
            break

    if serverIndex == -1:
        # raise exception
        print ("Could not map socket to a server in processMessage")


    # update solution and servers
    if message.message_type == 'solution':

        # add primes to solution
        for prime in message.data:
            solution.primes.append(prime)
        # mark chunks as complete
        for chunk in solution.chunks:
            if chunk.index == message.chunkID:
                chunk.complete = True
                chunk.timeFinish = time.time()

                print ("received solution from server", serverIndex,"for chunk",                       message.chunkID, "in", "{0:.2f}".format(
                           chunk.timeFinish - chunk.timeStart), 
                       "s; primes:", message.data)

                break
        # mark server as idle
        for server in solution.servers:
            if server.currentChunkID == message.chunkID:
                server.status = ServerStatus.idle
                break

        # send next chunk
        nextChunk = solution.getNextChunk()
        if nextChunk:
            messObj = Message("begin", (nextChunk.start,
                                        nextChunk.end),
                              nextChunk.index)

            jsonString = MessageEncoder().encode(messObj)
            #print(jsonString)

            print ("sending server", serverIndex, "chunk index",nextChunk.index)

            # mark chunk as scheduled
            nextChunk.scheduled = True
            nextChunk.timeStart = time.time()

            sendMessage(socket, jsonString)          

        elif solution.checkCompletion():
            solution.timeFinish = time.time()
            solution.printSolution()

        
    else:
        print ("received message other than solution ")


def loadServersFromFile(path, solution):
    f = open(path, 'r')
    for line in f:
        solution.serverNames.append(line.rstrip('\n'))

    

def main():
    sockets = []

    print ("running in main")


    complete = False

    solutionObject = Solution()
    if (len(sys.argv) == 2):
        loadServersFromFile(sys.argv[1], solutionObject)
    setupObject = Setup(solutionObject)
    setupObject.getInput()
    
    # ready to launch
    solutionObject.buildChunks()
    solutionObject.buildServers()
    solutionObject.initiate()

    for server in solutionObject.servers:
        sockets.append(server.socket)

    while not complete:
        ready_to_read, ready_to_write, error = \
                select.select (sockets, [], [])

        if (ready_to_read):
            for socket in ready_to_read:
                message = recvMessage(socket)
                processMessage(message, solutionObject, socket)
                complete = solutionObject.checkCompletion()


if __name__ == "__main__":
    main()
