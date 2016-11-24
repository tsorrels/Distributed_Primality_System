PORT = 19043
SERVER_TIMEOUT = 5 # in seconds
INT_SIZE = 4




class MessageType(object):
    progress = 1
    begin = 2
    result = 3


class Message(object):
    def __init__(self, in_type = None, in_data = '', in_length = 0):
        __type__ = 'Message'
        message_type = in_type
        data = in_data
        length = in_length

# taken from http://stackoverflow.com/questions/6578986/
# how-to-convert-json-data-into-a-python-object
def MessageDecoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Message':
        return Message(obj['message_type'], obj['data'], obj['length'])
    # throw exception
    return obj



def recvMessage(socket):
    raw_mess_len = recvLength(socket, INT_SIZE)
    mess_len = struct.unpack('>I', raw_mess_len)[0]
    message = recvLength(socket, mess_len)
    messageObject = json.loads(message, object_hook = MessageDecoder)
    return messageObject

def recvLength(socket, length):
    data = ''
    while len(data) < length:
        packet = socket.recv(length - len(data))
        if not packet:
            # throw exception
            break
        data += packet
    return data

