import prime_header.py
import multiprocessing
import socket











def main():
    print "running in main"

    run = true

    # set up server socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), PORT))
    serversocket.listen(5)

    while(run):
        ready_to_read, ready_to_write, error = \
                select.select (serversocket, [], [])

        
        



if __name__ == "__main__":
    main()
