# -*- coding: utf-8 -*-
__author__ = "Alvaro Braz e Diego Sanches"

import socket, sys


HOST = '192.168.100.28'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Aplicação cliente executando!")
            while(True):

                texto = input("Digite o palpite a ser enviado ao servidor:\n")
                s.send(texto.encode()) #texto.encode - converte a string para bytes

                data = s.recv(BUFFER_SIZE)
                texto_recebido = data.decode('utf-8') # converte os bytes em string

                print(texto_recebido)

                if (texto_recebido.endswith('3t0m')):
                    print('Você acertou!')
                    print('vai encerrar o socket cliente!')
                    s.close()
                    break

                if (texto == '0'):
                    print('vai encerrar o socket cliente!')
                    s.close()
                    break


    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])
