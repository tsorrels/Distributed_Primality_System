from config import *
import multiprocessing
import socket
import json
import select
import prime_test
import multiprocessing
import math
from threading import Thread
from threading import Event
from threading import active_count


class Chunk(object):
    def __init__(self, begin_in, end_in, index_in):
        self.begin = begin_in
        self.end = end_in
        self.index = index_in
        self.complete = False
        self.scheduled = False



class ServerSolution(object):
    def __init__(self, begin_in, end_in, chunkID_in):
        self.begin = begin_in
        self.end = end_in
        self.chunkID = chunkID_in
        self.primes = []
        self.scheduler = Scheduler(self.begin, self.end, self.primes)
        

    def findPrimes(self):
        print("Searching for primes between",self.begin, "and", self.end)
        n = self.begin
        if (n % 2 == 0):
            n = n + 1
        while (n <=  self.end):
            if (prime_test.testPrime(n)):
                self.primes.append(n)
            n = n + 2


class Scheduler(object):
    def __init__(self, begin_in, end_in, primes_in):
        self.begin = begin_in
        self.end = end_in
        self.threadEvent = Event()
        self.primesList = primes_in

        self.numThreads = 1
        #self.numThreads = multiprocessing.cpu_count() #- 1
        #if self.numThreads == 0:
        #    self.numThreads = 1

        self.chunks = []
        self.buildChunks()


    def buildChunks(self):
        numChunks = 1
        if self.numThreads > 1:
            numChunks = self.numThreads * CHUNK_FACTOR

        #print ('numThreads =', self.numThreads)
        #print ('numChunks = ', numChunks)
        rangeVal = math.ceil( (self.end - self.begin) / numChunks)
        #print ('rangeVal = ', rangeVal)


        for i in range(0, numChunks):
            chunkStart = int(self.begin + (i * rangeVal))
            chunkEnd = chunkStart + rangeVal - 1
            if (i == numChunks - 1):
                chunkEnd = self.end
            self.chunks.append(Chunk(chunkStart, chunkEnd, i))


    def checkCompletion(self):
        for i in range(0, len(self.chunks)):
            if (self.chunks[i].complete == False):
                #print("chunk ending with", self.chunks[i].end,"not complete")
                return False
        return True

    
    def getNextChunk(self):
        for i in range(0, len(self.chunks)):
            if (self.chunks[i].scheduled == False):
                return self.chunks[i]

        return None


    def run(self):
        threadsStarted = 0
        #threadsList = []
        #more = True
        print("Searching for primes between",self.begin, "and", self.end)

        while threadsStarted < self.numThreads:
            # schedule another thread
            nextChunk = self.getNextChunk()
            nextChunk.scheduled = True
            t = Thread(target=threadRun, args= (nextChunk, self.primesList,
                                                self.threadEvent))

            t.start()
            threadsStarted = threadsStarted + 1
                
        self.threadEvent.wait()
        self.threadEvent.clear()
        #print("Thread completed")

        while (self.getNextChunk()):
            # schedule another thread
            nextChunk = self.getNextChunk()
            nextChunk.scheduled = True
            t = Thread(target=threadRun, args= (nextChunk, self.primesList,
                                                self.threadEvent))

            t.start()
            if (active_count() < self.numThreads + 1):
                # don't wait for a thread to finish, schedule another thread
                continue
            self.threadEvent.wait()        
            self.threadEvent.clear()
            #print("Thread completed")


        #print ("All threads scheduled")
        while not self.checkCompletion():            
            self.threadEvent.wait()
            #print("Thread completed")
            self.threadEvent.clear()

    def findPrimes(self):
        print("Searching for primes between",self.begin, "and", self.end)
        n = self.begin
        if (n % 2 == 0):
            n = n + 1
        while (n <=  self.end):
            if (prime_test.testPrime(n)):
                self.primes.append(n)
            n = n + 2

        #CHUNK_FACTOR
        


def threadRun(chunk, masterList, event):
    print("New thread running, checking between", chunk.begin, "and",chunk.end)
    primes = []
    n = chunk.begin
    if (n % 2 == 0):
        n = n + 1
    while (n <=  chunk.end):
        if (prime_test.testPrime(n)):
            primes.append(n)
        n = n + 2

    # append to global solution
    for prime in primes:
        masterList.append(prime)
    # mark chunk as complete
    chunk.complete = True
    print("Thread until", chunk.end, "complete")
    # signal completion
    event.set()

    



def processMessage(message, clientSocket):
    if message.message_type == "begin":
        solution = ServerSolution(message.data[0], message.data[1], 
                                  message.chunkID)
        #solution.findPrimes()
        solution.scheduler.run()
        solution.primes.sort()
        solutionMessage = Message("solution", solution.primes, solution.chunkID)
        print ("Returning solution", solution.primes)
        mess = MessageEncoder().encode(solutionMessage)
        sendMessage(clientSocket, mess)      

    else:
        print("received message other than type 'begin'")


def main():
    run = True

    # set up server socket-
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversocket.bind((socket.gethostname(), PORT))
    serversocket.bind(('', PORT))
    serversocket.listen(1)

    print ("Server ready")

    while(run):
        (clientSocket, address) = serversocket.accept()
        connected = True
        while connected:
            ready_to_read, ready_to_write, error = \
                        select.select ([clientSocket], [], [])

            if (ready_to_read):
                message = recvMessage(clientSocket)
                if not message:
                    connected = False
                if message:
                    processMessage(message, clientSocket)
                    

if __name__ == "__main__":
    main()
