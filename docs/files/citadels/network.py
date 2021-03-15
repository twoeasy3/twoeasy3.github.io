import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = '192.168.1.123'
        self.port = 5555
        self.addr = (self.server,self.port)
        
    def getPos(self):
        return self.pos

    def connect(self):
        print("I AM CONNECTING")
        try:
            self.client.connect(self.addr)
            return(pickle.loads(self.client.recv(2048)))
        except:
            pass

    def send(self,data):
        try:
            sendData = pickle.dumps(data)
            self.client.send(sendData)
            receive = None
            while receive == None or receive == b'':
                receive = self.client.recv(2048)
            receiveP = pickle.loads(receive)
            return(receiveP)
        except socket.error as e:
            print(e)

    def sendNoReply(self,data):
        try:
            sendData = pickle.dumps(data)
            self.client.send(sendData)
        except socket.error as e:
            print(e)
            
    def ping_server(self,ping):
        try:
            self.client.send(ping.encode())
        except socket.error as e:
            print(e)
    def receive(self):
        try:
            data = self.client.recv(2048)
            dataP = pickle.loads(data)
            return(dataP)
        except socket.error as e:
            print(e)



