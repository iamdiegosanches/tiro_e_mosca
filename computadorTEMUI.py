import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Contra o computador")

# Cores
BACKGROUND_COLOR = (195, 219, 230)
INPUT_COLOR = (255, 255, 255)
HISTORY_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 128, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (5, 48, 5)
EXIT_BUTTON_COLOR = (255, 69, 0)
EXIT_BUTTON_HOVER_COLOR = (79, 23, 2)

# Fontes
font_input = pygame.font.Font(pygame.font.match_font('arial'), 60)
font_history = pygame.font.Font(pygame.font.match_font('arial'), 30)
font_button = pygame.font.Font(pygame.font.match_font('arial'), 40)

# Configuração do jogo
num_comp = str(random.randint(100, 1000))
historico_palpites = []
rodando = True
input_values = ["", "", ""]
history_scroll = 0

def verifica_palpite(palpite, num_comp):
    tiro, mosca = 0, 0
    num_comp_copy = list(num_comp)
    palpite_copy = list(palpite)

    # Contar os tiros
    for i in range(3):
        if palpite_copy[i] == num_comp_copy[i]:
            tiro += 1
            num_comp_copy[i] = "x"  # Marca como usado
            palpite_copy[i] = "y"

    # Contar as moscas
    for i in range(3):
        if palpite_copy[i] in num_comp_copy:
            mosca += 1
            index = num_comp_copy.index(palpite_copy[i])
            num_comp_copy[index] = "x"  # Marca como usado

    return tiro, mosca

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

def processa_palpite():
    global input_values, rodando
    palpite = "".join(input_values)
    tiro, mosca = verifica_palpite(palpite, num_comp)
    historico_palpites.append(f'{palpite} - {tiro}t{mosca}m')
    input_values = ["", "", ""]

    if tiro == 3:
        historico_palpites.append("FIM DE JOGO!")
        rodando = False

while rodando:
    screen.fill(BACKGROUND_COLOR)

    # entrada
    draw_input_box(screen, input_values)

    # botão Enviar
    button_x, button_y = SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50
    draw_button(screen, button_x, button_y, 150, 50, "Enviar", BUTTON_COLOR, BUTTON_HOVER_COLOR)

    # botão Desistir
    exit_button_x, exit_button_y = SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 120
    draw_button(screen, exit_button_x, exit_button_y, 150, 50, "Desistir", EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR)

    # histórico
    draw_history(screen, historico_palpites, history_scroll)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

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
                    processa_palpite()

            elif event.key == pygame.K_UP:
                history_scroll = min(history_scroll + 1, len(historico_palpites) - 5)
            elif event.key == pygame.K_DOWN:
                history_scroll = max(0, history_scroll - 1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Botão "Enviar"
            if button_x < mouse_pos[0] < button_x + 150 and button_y < mouse_pos[1] < button_y + 50:
                if all(len(val) == 1 for val in input_values):
                    processa_palpite()

            # Botão "Desistir"
            if exit_button_x < mouse_pos[0] < exit_button_x + 150 and exit_button_y < mouse_pos[1] < exit_button_y + 50:
                historico_palpites.append("Jogador desistiu. FIM DE JOGO!")
                rodando = False

        if event.type == pygame.MOUSEWHEEL:
            history_scroll -= event.y
            history_scroll = max(0, min(history_scroll, len(historico_palpites) - 5))

pygame.quit()
