import socket, sys
from threading import Thread
import random 


HOST = 'ip'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def receber_dados(clientsocket):
    while True:
        data = clientsocket.recv(BUFFER_SIZE)
        if data:
            texto_recebido = data.decode()
            return texto_recebido
        
def gera_numero_aleatorio():
    num_comp = str(random.randint(100, 1000))
    print(num_comp) # remover depois
    return num_comp

def verifica_palpite(palpite, num_comp):
    tiro, mosca = 0, 0
    num_comp_copy = list(num_comp)
    palpite_copy = list(palpite)

    # Contar os tiros
    for i in range(3):
        if palpite_copy[i] == num_comp_copy[i]:
            tiro += 1
            num_comp_copy[i] = "x"
            palpite_copy[i] = "y"

    # Contar as moscas
    for i in range(3):
        if palpite_copy[i] in num_comp_copy:
            mosca += 1
            index = num_comp_copy.index(palpite_copy[i])
            num_comp_copy[index] = "x"

    return tiro, mosca

def on_new_client(clientsocket, addr):
    numero_computador = gera_numero_aleatorio()
    historico_palpites = []
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break
            texto_recebido = data.decode()

            if texto_recebido == '0':
                    print('\tvai encerrar o socket do cliente {} !'.format(addr[0]))
                    clientsocket.send('sair'.encode())
                    clientsocket.close() 
                    return
            
            if len(texto_recebido) == 3 and texto_recebido.isdigit():       

                tiro, mosca = verifica_palpite(texto_recebido, numero_computador)

                historico_palpites.append(f'{texto_recebido} - {tiro}t{mosca}m')

                clientsocket.send(f'{texto_recebido} - {tiro}t{mosca}m'.encode())

                if tiro == 3:
                    print('ACERTOU')
                    clientsocket.close()
                    return

            else:
                print("Texto recebido em formato inválido")
                clientsocket.send("O palpite deve conter 3 números".encode())

        except Exception as error:
            print("\tErro na conexão com o cliente!!")
            print(error)
            return


def main(argv):
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            print('Vai iniciar servidor.')
            print(f'Servidor registrou a porta {PORT} no Sistema Operacional.')
            while True:
                server_socket.listen()
                print('Servidor está aguardando conexões...')
                clientsocket, addr = server_socket.accept()
                print('\tServidor recebeu conexão do cliente ao cliente no endereço:', addr)
                print('\tThread para tratar conexão será iniciada')
                t = Thread(target=on_new_client, args=(clientsocket,addr))
                t.start()   
    except Exception as error:
        print("\tErro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])
