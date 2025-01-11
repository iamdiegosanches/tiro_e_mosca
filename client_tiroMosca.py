import pygame
from network import Network

# Configurações da janela
width = 800
height = 600
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tiro e Mosca")

# Cores
bg_color = (30, 30, 30)  # Alterada para um tom mais escuro e moderno
text_color = (255, 255, 255)
highlight_color = (255, 0, 0)
success_color = (0, 255, 0)
input_color = (200, 200, 200)
history_color = (0, 0, 0)

# Fonte
font = pygame.font.SysFont('comicsans', 30)
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

def set_secret_number(n, player):
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

def draw_game(window, game, player, player_name, guess, feedback):
    """Desenha o estado do jogo na tela."""
    window.fill(bg_color)

    if not game.ready:
        text = font.render("Aguardando outro jogador...", True, highlight_color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))
    elif not game.post_secret:
        text = font.render("Aguardando ambos os códigos secretos...", True, highlight_color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))
    else:
        # Mostrar turno e resultados
        turno_texto = "Sua vez" if game.turn == player else "Vez do adversário"
        turno_cor = success_color if game.turn == player else highlight_color
        turno_render = font.render(turno_texto, True, turno_cor)
        window.blit(turno_render, (10, 10))

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

        # Exibir feedback atual
        feedback_render = font.render(feedback, True, highlight_color if "Inválido" in feedback else success_color)
        window.blit(feedback_render, (10, 500))

        # Exibir retângulos de entrada para o palpite
        draw_input_boxes(window, [str(num) for num in guess], x_start=width // 2 - 100, y_start=height // 2 - 40, box_width=60, gap=10)

        # Exibir vencedor, se houver
        if game.winner is not None:
            resultado = "Você venceu!" if game.winner == player else "Você perdeu!"
            resultado_render = font.render(resultado, True, success_color)
            screen.blit(resultado_render, (width // 2 - resultado_render.get_width() // 2, height // 2))

    # Exibir o nome do jogador
    nome_render = font.render(f"Jogador: {player_name}", True, text_color)
    screen.blit(nome_render, (10, 40))

    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    running = True
    n = Network()

    # Obter nome do jogador
    player_name = get_player_name()

    # Conectar ao servidor
    player = int(n.getP())
    print(f"Você é o jogador {player + 1}")

    # Definir número secreto
    secret = set_secret_number(n, player)

    feedback = ""
    guess = []

    while running:
        screen.fill(bg_color)
        clock.tick(60)

        try:
            game = n.send("get")
        except Exception as e:
            print(f"Erro ao receber jogo: {e}")
            break

        draw_game(screen, game, player, player_name, guess, feedback)

        if game.winner is not None:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        n.send("reset")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if game.ready and game.post_secret and game.turn == player and game.winner is None:
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

if __name__ == "__main__":
    main()
