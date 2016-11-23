
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


class Solution(object):
    def __init__(self):
        print("ran Solution init")
        self.primes = []
        self.begin = None
        self.end = None
        self.chunks = []
        self.servers = []
        self.progress = []
        self.scheduler = Scheduler.dynamic



class Status(object):
    def __init__(self, solution_in):
        print ("ran status init")
        self.solution = solution_in
        self.servers = []


    def display(self):
        print ("Display")
        print("Current servers:")
        if (self.servers):
            for server in self.servers:
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
        print(">>>", end = " ")


    def getInput(self):
        while True:
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
        pass

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
        

    


def main():
    print ("running in main")

    solutionObject = Solution()
    statusObject = Status(solutionObject)
    statusObject.getInput()
    
    # ready to launch
    

    # create as many sockets as necessary

    # chop up pieces, make solution object



if __name__ == "__main__":
    main()
