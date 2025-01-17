# -*- coding: utf-8 -*-
__author__ = "Alvaro Braz e Diego Sanches"

import socket, sys, pygame

pygame.init()

HOST = 'ip'
PORT = 20000
BUFFER_SIZE = 1024

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cliente Tiro e Mosca")


# Cores interface
BACKGROUND_COLOR = (195, 219, 230)
INPUT_COLOR = (255, 255, 255)
HISTORY_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 128, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (5, 48, 5)
EXIT_BUTTON_COLOR = (255, 69, 0)
EXIT_BUTTON_HOVER_COLOR = (79, 23, 2)
MENU_BUTTON_COLOR = (82, 154, 179)
MENU_HOVER_COLOR = (40, 76, 99)

# Fontes
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_input = pygame.font.Font(pygame.font.match_font('arial'), 60)
font_history = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 40)

history_scroll = 0
historico = []
input_values = ["", "", ""]
nome_jogador = ""

def draw_text_centered(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def main_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)

        # Título
        draw_text_centered("Escolha o modo de jogo", font_title, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)

        # Botão 1: Modo Multiplayer
        multiplayer_rect = pygame.Rect(100, 250, 250, 100)
        pygame.draw.rect(screen, MENU_HOVER_COLOR if multiplayer_rect.collidepoint(pygame.mouse.get_pos()) else MENU_BUTTON_COLOR, multiplayer_rect, border_radius=10)
        draw_text_centered("Multiplayer", font_button, TEXT_COLOR, screen, multiplayer_rect.centerx, multiplayer_rect.centery)

        # Botão 2: Contra Computador
        computer_rect = pygame.Rect(450, 250, 250, 100)
        pygame.draw.rect(screen, MENU_HOVER_COLOR if computer_rect.collidepoint(pygame.mouse.get_pos()) else MENU_BUTTON_COLOR, computer_rect, border_radius=10)
        draw_text_centered("Computador", font_button, TEXT_COLOR, screen, computer_rect.centerx, computer_rect.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if multiplayer_rect.collidepoint(mouse_pos):
                    return "multiplayer"
                if computer_rect.collidepoint(mouse_pos):
                    return "computador"

def draw_input_box(screen, values):
    gap = 10
    box_width = 60
    x_start = (SCREEN_WIDTH - (3 * box_width + 2 * gap)) // 2
    y_start = SCREEN_HEIGHT // 2 - 50

    for i, value in enumerate(values):
        rect = pygame.Rect(x_start + i * (box_width + gap), y_start, box_width, 80)
        pygame.draw.rect(screen, INPUT_COLOR, rect, border_radius=5)
        text_surface = font_input.render(value, True, HISTORY_COLOR)
        screen.blit(text_surface, (rect.x + 15, rect.y + 10))

def draw_button(screen, x, y, width, height, text, color, hover_color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, hover_color if button_rect.collidepoint(pygame.mouse.get_pos()) else color, button_rect, border_radius=10)
    text_surface = font_button.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_history(screen, history, scroll):
    x, y = 50, SCREEN_HEIGHT - 150
    visible_lines = 5
    start_index = max(0, len(history) - visible_lines - scroll)
    end_index = len(history) - scroll
    for line in history[start_index:end_index]:
        text_surface = font_history.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (x, y))
        y += 30

def recebe_nome_jogador():
    global nome_jogador
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40, 300, 80)
    typing = True

    while typing:
        screen.fill(BACKGROUND_COLOR)

        # Instruções
        draw_text_centered("Digite seu nome:", font_title, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        # Caixa de entrada
        pygame.draw.rect(screen, INPUT_COLOR, input_box, border_radius=10)
        text_surface = font_input.render(nome_jogador, True, HISTORY_COLOR)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Botão Continuar
        continue_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 60, 150, 50)
        draw_button(screen, continue_rect.x, continue_rect.y, continue_rect.width, continue_rect.height, 
                    "Start", BUTTON_COLOR, BUTTON_HOVER_COLOR)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    if nome_jogador.strip():
                        typing = False
                else:
                    if len(nome_jogador) < 20:  # Limite de caracteres para o nome
                        nome_jogador += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos) and nome_jogador.strip():
                    typing = False


def main(argv):
    global history_scroll
    global historico

    recebe_nome_jogador()
    mode = main_menu()

    running = True
    acertou = False
    desistiu = False

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)  # Timeout para evitar bloqueios
            s.connect((HOST, PORT))

            s.send("".join(f"/usu {nome_jogador}").encode())

            print("Aplicação cliente executando!")
            print(f"Modo escolhido: {mode}. Iniciando o jogo...")
            while running:
                screen.fill(BACKGROUND_COLOR)

                # entrada
                draw_input_box(screen, input_values)

                # botão Enviar
                button_x, button_y = SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50
                draw_button(screen, button_x, button_y, 150, 50, "Enviar", BUTTON_COLOR, BUTTON_HOVER_COLOR)


                # histórico
                draw_history(screen, historico, history_scroll)

                if acertou: 
                    draw_text_centered("Você Venceu!!!", font_title, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)
                    # botão Jogar Novamente
                    novo_button_x, novo_button_y = SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 200
                    draw_button(screen, novo_button_x, novo_button_y, 150, 50, "Novo", EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR)
                else:
                    novo_button_x, novo_button_y = -1000, -1000
                    if desistiu:
                        draw_text_centered("Você Desistiu! Comece o novo jogo!", font_title, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)
                    else:
                        draw_text_centered("Escolha Seu Palpite", font_title, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)
                    
                    # botão Desistir
                    exit_button_x, exit_button_y = SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 120
                    draw_button(screen, exit_button_x, exit_button_y, 150, 50, "Desistir", EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        s.send("".join('0').encode())
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                        pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_KP0, pygame.K_KP1, 
                                        pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, 
                                        pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]:
                            for i in range(3):
                                if input_values[i] == "":
                                    input_values[i] = event.unicode
                                    break

                        elif event.key == pygame.K_BACKSPACE:
                            for i in range(2, -1, -1):
                                if input_values[i] != "":
                                    input_values[i] = ""
                                    break
                                
                        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            if all(len(val) == 1 for val in input_values):
                                s.send("".join(input_values).encode())
                                input_values[:] = ["", "", ""]
                                
                        elif event.key == pygame.K_UP:
                            history_scroll = min(history_scroll + 1, len(historico) - 5)

                        elif event.key == pygame.K_DOWN:
                            history_scroll = max(0, history_scroll - 1)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if button_x < mouse_pos[0] < button_x + 150 and button_y < mouse_pos[1] < button_y + 50:
                            if all(len(val) == 1 for val in input_values):
                                s.send("".join(input_values).encode())
                                input_values[:] = ["", "", ""]
                        if exit_button_x < mouse_pos[0] < exit_button_x + 150 and exit_button_y < mouse_pos[1] < exit_button_y + 50:
                            s.send("".join('novo_jogo').encode())
                            desistiu = True
                            historico = []
                        if novo_button_x < mouse_pos[0] < novo_button_x + 150 and novo_button_y < mouse_pos[1] < novo_button_y + 50:
                            s.send("".join('novo_jogo').encode())
                            acertou = False
                            desistiu = False
                            historico = []
                    if event.type == pygame.MOUSEWHEEL:
                        history_scroll -= event.y
                        history_scroll = max(0, min(history_scroll, len(historico) - 5))

                try:
                    data = s.recv(BUFFER_SIZE)
                    if data:
                        texto_recebido = data.decode('utf-8')
                        historico.append(texto_recebido)
                        if texto_recebido.endswith("3t0m"):
                            acertou = True

                except socket.timeout:
                    pass  # Ignorar ausência de dados

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(f"Erro: {error}")
    finally:
        pygame.quit()
        print("Cliente encerrado!")
        s.close

if __name__ == "__main__":
    main(sys.argv[1:])
