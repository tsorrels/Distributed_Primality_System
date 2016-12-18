import struct
from enum import Enum
import json

PORT = 19043
SERVER_TIMEOUT = 5 # in seconds
INT_SIZE = 4
CHUNK_FACTOR = 4


class ServerStatus(Enum):
    idle = 1
    working = 2


class MessageType(Enum):
    progress = 1
    begin = 2
    result = 3


class Message(object):
    def __init__(self, in_type = '', in_data = '', in_chunkID = None):
        self.__type__ = 'Message'
        self.message_type = in_type
        self.data = in_data
        self.length = None
        self.chunkID = in_chunkID

# taken from http://stackoverflow.com/questions/6578986/
# how-to-convert-json-data-into-a-python-object
def MessageDecoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Message':
        return Message(obj['message_type'], obj['data'], obj['chunkID'])
    # throw exception
    return obj

class MessageEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

    
def sendMessage(socket, message):
    mess_len = len(message)
    #print("Sending message of length ", mess_len)
    mess_len_packed = struct.pack('>I', mess_len)
    bytesSent = 0

    # send message size
    while bytesSent < INT_SIZE:
        sent = socket.send(mess_len_packed)
        bytesSent = bytesSent + sent
    
    # send message
    bytesSent = 0
    while bytesSent < mess_len:
        sent = socket.send(bytes(message, 'UTF-8'))
        bytesSent = bytesSent + sent



def recvMessage(socket):
    raw_mess_len = recvLength(socket, INT_SIZE)
    if (raw_mess_len):
        mess_len = struct.unpack('>I', raw_mess_len[0])[0]
        message = recvLength(socket, mess_len)[0].decode('UTF-8')
        #print ("message: ", message)
        #print("message = ", message)
        messageObject = json.loads(message, object_hook = MessageDecoder)
        return messageObject



def recvLength(socket, length):
    #print("receiving " , length, " bytes")
    data = []
    bytesReceived = 0
    while bytesReceived < length:
        packet = socket.recv(length - bytesReceived)
        if not packet:
            # throw exception
            break
        data.append(packet)
        bytesReceived = bytesReceived + len(packet)
    return data
