import socket
import pickle  # converte objetos Python (como listas, dicionários, classes, etc.) em um formato de byte que pode ser
# armazenado em um arquivo ou transmitido pela rede


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'ip'
        self.port = 8080
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()  # recebe p do servidor
        except socket.error as msg:
            print(msg)

    def send(self, data):
        try:
            self.client.send(data.encode())
            data = self.client.recv(4096)
            if not data:
                print("Nenhum dado recebido do servidor.")
                return None
            return pickle.loads(data)
        except socket.error as msg:
            print(msg)

