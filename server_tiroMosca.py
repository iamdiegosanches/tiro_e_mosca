import socket
import threading
import pickle
from tiroMosca import TiroMosca

server = "ip"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Servidor aguardando conexões...")

games = {}
idCount = 0


def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str(player).encode())

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    print("Conexão encerrada")
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data == "get":
                        conn.sendall(pickle.dumps(game))
                    elif data.startswith("set_numbers"):
                        _, numbers = data.split(":")
                        numbers = list(map(int, numbers.split(",")))
                        print(f"numbers: {numbers}")
                        if game.set_numbers(player, numbers):
                            print(f"Jogador {player} definiu o código secreto: {numbers}")
                        else:
                            print(f"Jogador {player} tentou redefinir o código secreto.")
                    elif data.startswith("play"):
                        _, guess = data.split(":")
                        guess = list(map(int, guess.split(",")))
                        game.play(player, guess)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print(f"Erro no cliente: {e}")
            break

    print(f"Conexão perdida com jogador {player}")
    try:
        if gameId in games:
            del games[gameId]
            print(f"Fechando jogo {gameId}")
    except Exception as e:
        print(f"Erro ao fechar jogo {gameId}: {e}")
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Conectado por", addr)

    idCount += 1
    player = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = TiroMosca(gameId)
        print(f"Novo jogo criado com ID {gameId}")
    else:
        games[gameId].ready = True
        player = 1
        print(f"Jogador 1 conectado ao jogo {gameId}")

    thread = threading.Thread(target=threaded_client, args=(conn, player, gameId))
    thread.start()
