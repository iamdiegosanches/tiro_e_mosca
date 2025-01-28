import pygame
from network import Network
from tiroMosca import TiroMosca

# Configurações da janela
width = 800
height = 600
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tiro e Mosca")

# Cores
bg_color = (30, 30, 30) 
text_color = (255, 255, 255)
highlight_color = (255, 0, 0)
success_color = (0, 255, 0)
input_color = (200, 200, 200)
history_color = (0, 0, 0)
menu_button_color = (79, 170, 105)
menu_hover_color = (88, 181, 83)

# Fonte
font = pygame.font.SysFont('comicsans', 30)
font_med_button = pygame.font.SysFont('comicsans', 40)
font_input = pygame.font.SysFont('comicsans', 60)
font_history = pygame.font.SysFont('comicsans', 20)


def draw_input_boxes(window, values, x_start, y_start, box_width, gap):
    """Desenha as caixas de entrada para números."""
    for i in range(3):
        rect = pygame.Rect(x_start + i * (box_width + gap), y_start, box_width, 80)
        pygame.draw.rect(window, input_color, rect, border_radius=5)
        if i < len(values):
            text_surface = font_input.render(str(values[i]), True, history_color)
            window.blit(text_surface, (rect.x + 15, rect.y + 10))

def draw_text_centered(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def get_player_name():
    """Solicita o nome do jogador antes de iniciar o jogo, com cursor piscante."""
    name = ""
    active = True
    cursor_visible = True
    cursor_blink_time = pygame.time.get_ticks()

    while active:
        screen.fill(bg_color)
        prompt = font.render("Digite seu nome e pressione Enter:", True, text_color)
        screen.blit(prompt, (width // 2 - prompt.get_width() // 2, height // 3))

        # Desenha o nome e o cursor
        name_render = font.render(name, True, text_color)
        screen.blit(name_render, (width // 2 - name_render.get_width() // 2, height // 2))

        # Controle do cursor piscante
        if cursor_visible:
            cursor_x = width // 2 - name_render.get_width() // 2 + name_render.get_width() + 5
            cursor_y = height // 2
            pygame.draw.line(screen, text_color, (cursor_x, cursor_y - 10), (cursor_x, cursor_y + 10), 2)

        if pygame.time.get_ticks() - cursor_blink_time > 500:
            cursor_visible = not cursor_visible
            cursor_blink_time = pygame.time.get_ticks()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name.strip()

def set_secret_number(n):
    """Define os números secretos do jogador e os envia ao servidor."""
    secret = []
    feedback = ""
    active = True

    while active:
        screen.fill(bg_color)
        prompt = font.render("Digite 3 números como seu segredo e pressione Enter:", True, text_color)
        screen.blit(prompt, (width // 2 - prompt.get_width() // 2, height // 3))

        # Exibir quadrados de entrada para o código secreto
        draw_input_boxes(screen, secret, x_start=width // 2 - 150, y_start=height // 2 - 40, box_width=80, gap=20)

        feedback_render = font.render(feedback, True, highlight_color if "Erro" in feedback else success_color)
        screen.blit(feedback_render, (width // 2 - feedback_render.get_width() // 2, height // 2 + 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(secret) == 3:
                    try:
                        n.send(f"set_numbers:{','.join(map(str, secret))}")
                        feedback = "Número secreto enviado com sucesso!"
                        active = False
                    except Exception as e:
                        feedback = f"Erro ao enviar número secreto: {e}"
                elif event.key == pygame.K_BACKSPACE and secret:
                    secret.pop()
                elif event.unicode.isdigit() and len(secret) < 3:
                    secret.append(int(event.unicode))
    return secret

def set_computer_secret_number(n):
    """Diz ao servidor para escolher um número"""
    try:
        n.send("set_random_number")
        print("Solicitado número secreto")
    except Exception as e:
        print("Erro ao iniciar o número secreto")

def draw_game(window, game, player, player_name, guess, feedback):
    """Desenha o estado do jogo na tela."""
    window.fill(bg_color)

    if isinstance(game, TiroMosca):
        if not game.ready and not game.singlePlayer:
            text = font.render("Aguardando outro jogador...", True, highlight_color)
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))
        elif not game.post_secret and not game.singlePlayer:
            text = font.render("Aguardando ambos os códigos secretos...", True, highlight_color)
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))
        else:
            # Mostrar turno e resultados
            turno_texto = "Sua vez" if game.turn == player else "Vez do adversário"
            turno_cor = success_color if game.turn == player else highlight_color
            turno_render = font.render(turno_texto, True, turno_cor)
            window.blit(turno_render, (10, 10))

            if game.singlePlayer and game.winner is None:
                desistiu_rect = pygame.Rect(width // 2 + 100, height // 2 + 150, 125, 50)
                pygame.draw.rect(screen, menu_hover_color if desistiu_rect.collidepoint(
                    pygame.mouse.get_pos()) else menu_button_color, desistiu_rect, border_radius=10)
                draw_text_centered("Desistir", font, text_color, screen, desistiu_rect.centerx,
                                   desistiu_rect.centery)
            
            if game.winner is not None:
                reset_rect = pygame.Rect(width // 2 + 250, height // 2 + 80, 125, 50)
                pygame.draw.rect(screen, menu_hover_color if reset_rect.collidepoint(
                    pygame.mouse.get_pos()) else menu_button_color, reset_rect, border_radius=10)
                draw_text_centered("Reset", font, text_color, screen, reset_rect.centerx,
                                    reset_rect.centery)

            sair_rect = pygame.Rect(width // 2 + 250, height // 2 + 150, 125, 50)
            pygame.draw.rect(screen, menu_hover_color if sair_rect.collidepoint(
                pygame.mouse.get_pos()) else menu_button_color, sair_rect, border_radius=10)
            draw_text_centered("Sair", font, text_color, screen, sair_rect.centerx,
                                sair_rect.centery)

            # Exibir histórico de palpites do jogador atual
            history_y_player = 100
            player_history_title = font.render("Seus palpites:", True, text_color)
            window.blit(player_history_title, (10, 70))

            for entry in game.history[player][-5:]:  # Últimos 5 palpites
                palpite, tiros, moscas = entry
                history_text = f"Palpite: {palpite} | Tiros: {tiros} | Moscas: {moscas}"
                history_render = font_history.render(history_text, True, text_color)
                window.blit(history_render, (10, history_y_player))
                history_y_player += 30

            if not game.singlePlayer:
                # Exibir histórico de palpites do adversário
                history_y_opponent = 100
                opponent = 1 - player
                opponent_history_title = font.render("Palpites do adversário:", True, text_color)
                window.blit(opponent_history_title, (400, 70))

                for entry in game.history[opponent][-5:]:  # Últimos 5 palpites do adversário
                    palpite, tiros, moscas = entry
                    history_text = f"Palpite: {palpite} | Tiros: {tiros} | Moscas: {moscas}"
                    history_render = font_history.render(history_text, True, text_color)
                    window.blit(history_render, (400, history_y_opponent))
                    history_y_opponent += 30

            # Exibir retângulos de entrada para o palpite
            draw_input_boxes(window, [str(num) for num in guess], x_start=width // 2 - 100, y_start=height // 2 - 40,
                             box_width=60, gap=10)

            # Exibir histórico de vitórias e rodadas necessárias
            history_wins = 400
            history_wins_title = font.render("Histórico de vitórias:", True, text_color)
            window.blit(history_wins_title, (10, history_wins))

            max_display = 5
            coords = [10, 400]

            for p in range(2 if not game.singlePlayer else 1):
                player_wins = f"Jogador {p + 1}: {game.wins[p]} vitórias"
                win_render = font_history.render(player_wins, True, text_color)
                window.blit(win_render, (coords[p], history_wins + 30))

                # Mostrar apenas as últimas vitórias
                if game.rounds_per_win[p]:
                    last_wins = game.rounds_per_win[p][-max_display:]
                    for i, rounds in enumerate(last_wins, start=1):
                        rounds_text = f"Vitória {i}: {rounds} rodadas"
                        rounds_render = font_history.render(rounds_text, True, text_color)
                        window.blit(rounds_render, (coords[p], history_wins + 30 + i * 15))

            # Exibir vencedor, se houver
            if game.winner is not None and not game.quit:
                resultado = "Você venceu!" if game.winner == player else "Você perdeu!"
                resultado_render = font.render(resultado, True, success_color)
                screen.blit(resultado_render, (width // 2 - resultado_render.get_width() // 2, height // 2 - 80))

    # Exibir o nome do jogador
    nome_render = font.render(f"Jogador: {player_name}", True, text_color)
    screen.blit(nome_render, (10, 40))

    pygame.display.update()

def draw_reset(window, game, player):
    window.fill(bg_color)

    if game.reset_players[player]:
        text = font.render("Aguardando confirmação do outro jogador...", True, highlight_color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))
    else:
        sim_rect = pygame.Rect(width // 2 + 50, height // 2 + 150, 125, 50)
        pygame.draw.rect(screen, menu_hover_color if sim_rect.collidepoint(
            pygame.mouse.get_pos()) else menu_button_color, sim_rect, border_radius=10)
        draw_text_centered("Sim", font, text_color, screen, sim_rect.centerx,
                            sim_rect.centery)
        nao_rect = pygame.Rect(width // 2 + 200, height // 2 + 150, 125, 50)
        pygame.draw.rect(screen, menu_hover_color if nao_rect.collidepoint(
            pygame.mouse.get_pos()) else menu_button_color, nao_rect, border_radius=10)
        draw_text_centered("Não", font, text_color, screen, nao_rect.centerx,
                            nao_rect.centery)
        text = font.render("Você deseja jogar novamente?", True, highlight_color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 3))


    pygame.display.update()
    


def main(tipo_jogo):
    clock = pygame.time.Clock()
    running = True
    n = Network()

    # Obter nome do jogador
    player_name = get_player_name()

    # Conectar ao servidor
    try:
        player = int(n.getP())
        print(f"Você é o jogador {player + 1}")
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        running = False

    if tipo_jogo == 'computador':
        set_computer_secret_number(n)
    elif tipo_jogo == 'multiplayer':
        # Definir número secreto
        secret = set_secret_number(n)
        print(secret)

    feedback = ""
    guess = []

    while running:
        screen.fill(bg_color)
        clock.tick(60)

        try:
            game = n.send("get")
            if game is None:
                raise Exception("Jogo desconectado.")
        except Exception as e:
            print(f"Erro ao receber jogo: {e}")
            break

        if not (game.reset_players[player] or game.reset_players[1 - player]):
            draw_game(screen, game, player, player_name, guess, feedback)

        if isinstance(game, TiroMosca):
            if game.secret == [["" for _ in range(3)] for _ in range(2)] and not game.singlePlayer:
                secret = set_secret_number(n)

            if (game.reset_players[player] or game.reset_players[1 - player]) and game.winner is not None and not game.singlePlayer:
                draw_reset(screen, game, player)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        sim_rect = pygame.Rect(width // 2 + 50, height // 2 + 150, 125, 50)
                        if sim_rect.collidepoint(mouse_pos):
                            try:
                                n.send("resetplayer")
                            except Exception as e:
                                print(f"Erro ao reiniciar o jogo: {e}")
                        nao_rect = pygame.Rect(width // 2 + 200, height // 2 + 150, 125, 50)
                        if nao_rect.collidepoint(mouse_pos):
                            running = False
                            break

            if game.winner is not None and not game.quit and not game.singlePlayer:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        reset_rect = pygame.Rect(width // 2 + 250, height // 2 + 80, 125, 50)
                        sair_rect = pygame.Rect(width // 2 + 200, height // 2 + 150, 125, 50)
                        if reset_rect.collidepoint(mouse_pos):
                            try:
                                n.send("resetplayer")
                            except Exception as e:
                                print(f"Erro ao reiniciar o jogo: {e}")
                        if sair_rect.collidepoint(mouse_pos):
                            print("Cliquei no botão para sair")
                            n.send("quit")
                            text = font.render("Você saiu da partida!", True, highlight_color)
                            screen.blit(text, (width // 2 - text.get_width() // 2, height // 3))
                            pygame.display.update()
                            pygame.time.delay(2000)
                            if game.singlePlayer:
                                running = False
                            else:
                                menu_screen()
                continue
            
            if game.winner is not None and game.quit and not game.singlePlayer:
                text = font.render("O outro jogador saiu da partida!", True, highlight_color)
                screen.blit(text, (width // 2 - text.get_width() // 2, height // 3))
                pygame.display.update()
                pygame.time.delay(2000)
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if game.ready and game.singlePlayer and game.winner is None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        desistiu_rect = pygame.Rect(width // 2 + 100, height // 2 + 150, 125, 50)
                        if desistiu_rect.collidepoint(mouse_pos):
                            text = font.render("Você desistiu", True, text_color)
                            screen.blit(text, (width // 2 - text.get_width() // 2, height // 3))
                            pygame.display.update()
                            pygame.time.delay(2000)
                            try:
                                n.send("reset")
                                guess = []
                                feedback = ""
                                set_computer_secret_number(n)
                            except Exception as e:
                                print(f"Erro ao reiniciar o jogo após desistir: {e}")
                
                if game.ready and game.winner is None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        sair_rect = pygame.Rect(width // 2 + 200, height // 2 + 150, 125, 50)
                        if sair_rect.collidepoint(mouse_pos):
                            try:
                                print("Cliquei no botão para sair")
                                n.send("quit")
                                if not game.singlePlayer:
                                    text = font.render("Você saiu da partida!", True, highlight_color)
                                    screen.blit(text, (width // 2 - text.get_width() // 2, height // 3))
                                    pygame.display.update()
                                    pygame.time.delay(2000)
                                if game.singlePlayer:
                                    running = False
                                else:
                                    menu_screen()
                            except Exception as e:
                                print(f"Erro ao processar desistência: {e}")
                
                if game.ready and game.winner is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        reset_rect = pygame.Rect(width // 2 + 250, height // 2 + 80, 125, 50)
                        if reset_rect.collidepoint(mouse_pos):
                            try:
                                n.send("reset")
                                guess = []
                                feedback = ""
                                set_computer_secret_number(n)
                            except Exception as e:
                                print(f"Erro ao reiniciar o jogo: {e}")

                if game.ready and (game.post_secret and game.turn == player or game.singlePlayer) and game.winner is None:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(guess) == 3:
                            try:
                                n.send(f"play:{','.join(map(str, guess))}")
                                feedback = f"Palpite enviado: {guess}"
                                guess = []
                            except Exception as e:
                                feedback = f"Erro ao enviar palpite: {e}"
                        elif event.key == pygame.K_BACKSPACE and guess:
                            guess.pop()
                        elif event.unicode.isdigit() and len(guess) < 3:
                            guess.append(int(event.unicode))
                            feedback = f"Palpite atual: {guess}"


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        tipo_jogo = ""
        clock.tick(60)
        screen.fill(bg_color)
        fonte = pygame.font.SysFont('comicsans', 60)
        text = fonte.render("Escolha o modo de jogo", True, (255, 255, 255))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))

        # Botão 1: Modo Multiplayer
        multiplayer_rect = pygame.Rect(100, 250, 250, 100)
        pygame.draw.rect(screen, menu_hover_color if multiplayer_rect.collidepoint(pygame.mouse.get_pos()) else menu_button_color, multiplayer_rect, border_radius=10)
        draw_text_centered("Multiplayer", font_med_button, text_color, screen, multiplayer_rect.centerx, multiplayer_rect.centery)

        # Botão 2: Contra Computador
        computer_rect = pygame.Rect(450, 250, 250, 100)
        pygame.draw.rect(screen, menu_hover_color if computer_rect.collidepoint(pygame.mouse.get_pos()) else menu_button_color, computer_rect, border_radius=10)
        draw_text_centered("Computador", font_med_button, text_color, screen, computer_rect.centerx, computer_rect.centery)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if multiplayer_rect.collidepoint(mouse_pos):
                    tipo_jogo = "multiplayer"
                    run = False
                if computer_rect.collidepoint(mouse_pos):
                    tipo_jogo = "computador"
                    run = False

    main(tipo_jogo)


if __name__ == "__main__":
    while True:
        menu_screen()
