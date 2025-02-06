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

multiplayer_games = {}
singleplayer_games = {}
idCount = 0
singlePlayerIdCount = 0

def threaded_client(conn, player, gameId, game_type):
    global idCount, singlePlayerIdCount
    conn.send(str(player).encode())


    while True:
        try:
            data = conn.recv(4096).decode()

            if game_type == "multiplayer":
                games = multiplayer_games
            else:
                games = singleplayer_games

            if gameId in games:
                game = games[gameId]

                if game.quit:
                    break

                if not data:
                    print("Conexão encerrada")
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data == "resetplayer":
                        turn = game.getTurn()
                        game.reset_player(player, turn)
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
                    elif data == "set_random_number":
                        print("Servidor gerando números")
                        game.set_random_number(1 - player)
                    elif data.startswith("play"):
                        _, guess = data.split(":")
                        guess = list(map(int, guess.split(",")))
                        game.play(player, guess)
                    elif data == "quit":
                        print("Algum jogador saiu da partida")
                        print("Excluindo jogo...")
                        game.quit_game(player)
                        break
                        # if game_type == "multiplayer":
                        #     idCount -= 1
                        # else:
                        #     singlePlayerIdCount -= 1

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

    if game_type == "multiplayer":
        idCount -= 1
    else:
        singlePlayerIdCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Conectado por", addr)

    # Receber o tipo de jogo do cliente
    game_type = conn.recv(4096).decode()
    print(f"Tipo de jogo solicitado: {game_type}")

    player = 0
    gameId = None

    if game_type == "multiplayer":
        idCount += 1
        idCount = 1 if idCount < 0 else idCount
        gameId = (idCount - 1) // 2
        gameId = 0 if gameId < 0 else gameId

        if idCount % 2 == 1:
            multiplayer_games[gameId] = TiroMosca(gameId)
            print(f"Novo jogo multiplayer criado com ID {gameId}")
        else:
            gameId = 0 if gameId < 0 else gameId
            print("GameId", gameId)
            if gameId in multiplayer_games:
                multiplayer_games[gameId].ready = True
                player = 1
                print(f"Jogador 1 conectado ao jogo multiplayer {gameId}")
            else:
                idCount = -1
                continue

    elif game_type == "computador":
        singlePlayerIdCount += 1
        gameId = singlePlayerIdCount
        singleplayer_games[gameId] = TiroMosca(gameId)
        singleplayer_games[gameId].singlePlayer = True
        singleplayer_games[gameId].ready = True
        print(f"Novo jogo contra o computador criado com ID {gameId}")

    thread = threading.Thread(target=threaded_client, args=(conn, player, gameId, game_type))
    thread.start()