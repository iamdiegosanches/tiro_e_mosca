import pygame
import os
import subprocess

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Principal")

# Cores
BACKGROUND_COLOR = (195, 219, 230)
TEXT_COLOR = (0, 0, 0)
HOVER_COLOR = (40, 76, 99)

# Fontes
font_title = pygame.font.Font(pygame.font.match_font('arial'), 50)
font_option = pygame.font.Font(pygame.font.match_font('arial'), 40)

# Função para desenhar texto centralizado
def draw_text_centered(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Função para o menu principal
def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Título
        draw_text_centered("Escolha o modo de jogo", font_title, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)

        # Opção 1: Jogar com dois jogadores
        left_rect = pygame.Rect(50, 200, SCREEN_WIDTH // 2 - 100, 200)
        pygame.draw.rect(screen, HOVER_COLOR if left_rect.collidepoint(pygame.mouse.get_pos()) else TEXT_COLOR, left_rect, border_radius=10)
        draw_text_centered("2 Jogadores", font_option, BACKGROUND_COLOR, screen, left_rect.centerx, left_rect.centery)

        # Opção 2: Jogar contra o computador
        right_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, 200, SCREEN_WIDTH // 2 - 100, 200)
        pygame.draw.rect(screen, HOVER_COLOR if right_rect.collidepoint(pygame.mouse.get_pos()) else TEXT_COLOR, right_rect, border_radius=10)
        draw_text_centered("Computador", font_option, BACKGROUND_COLOR, screen, right_rect.centerx, right_rect.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if left_rect.collidepoint(mouse_pos):
                    print("Modo 2 jogadores selecionado!")
                    # Aqui você pode chamar o arquivo ou lógica de dois jogadores

                if right_rect.collidepoint(mouse_pos):
                    print("Modo contra o computador selecionado!")
                    subprocess.Popen(["python3", "computadorTEMUI.py"])
    pygame.quit()

if __name__ == "__main__":
    main_menu()
