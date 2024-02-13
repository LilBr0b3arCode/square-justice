import pygame
import random
import sys
from math import atan2, cos, sin, pi

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Justice")

# Define colors
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
BLOOD_RED = (150, 0, 0)

# Define square sizes and initial positions
player_size = 30
enemy_size = 30
enemy_speed = 2
player_speed = 5
player_x, player_y = WIDTH // 2, HEIGHT // 2
enemies = [(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), BLUE) for _ in range(5)]
orange_enemies = [(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), ORANGE) for _ in range(5)]

# Define projectile variables
projectile_size = 10
projectile_speed = 10
projectile_cooldown = 0.5
last_shot_time = 0
projectiles = []

# Define debug menu variables
show_debug_menu = False
player_speed_debug = player_speed
projectile_speed_debug = projectile_speed
show_black_outline = True
show_background = True
show_blood = True
show_tracer_lines = False

# Function to restart the game
def restart_game():
    global player_x, player_y, enemies, orange_enemies
    player_x, player_y = WIDTH // 2, HEIGHT // 2
    enemies.clear()
    orange_enemies.clear()

# Function to draw debug menu
def draw_debug_menu():
    pygame.draw.rect(screen, (0, 0, 0, 128), (10, 10, 300, 250))
    font = pygame.font.SysFont(None, 24)
    text_speed = font.render("Player Speed: " + str(player_speed_debug), True, WHITE)
    text_projectile = font.render("Projectile Speed: " + str(projectile_speed_debug), True, WHITE)
    text_toggle_outline = font.render("Black Outline: " + ("On" if show_black_outline else "Off"), True, WHITE)
    text_toggle_background = font.render("Background: " + ("On" if show_background else "Off"), True, WHITE)
    text_toggle_blood = font.render("Blood: " + ("On" if show_blood else "Off"), True, WHITE)
    text_toggle_tracer = font.render("Tracer Lines: " + ("On" if show_tracer_lines else "Off"), True, WHITE)
    screen.blit(text_speed, (20, 20))
    screen.blit(text_projectile, (20, 50))
    screen.blit(text_toggle_outline, (20, 80))
    screen.blit(text_toggle_background, (20, 110))
    screen.blit(text_toggle_blood, (20, 140))
    screen.blit(text_toggle_tracer, (20, 170))

# Main game loop
while True:
    screen.fill(GRAY)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                show_debug_menu = not show_debug_menu
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if not show_debug_menu:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = atan2(mouse_y - player_y, mouse_x - player_x)
                    projectiles.append((player_x + player_size // 2, player_y + player_size // 2, angle))
            elif event.button == 4:  # Scroll up
                if show_debug_menu:
                    player_speed_debug += 1
            elif event.button == 5:  # Scroll down
                if show_debug_menu:
                    player_speed_debug = max(1, player_speed_debug - 1)
            elif event.button == 3:  # Right mouse button
                if show_debug_menu:
                    projectile_speed_debug += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if show_debug_menu:
                    projectile_speed_debug -= 1
            elif event.key == pygame.K_t:
                if show_debug_menu:
                    projectile_speed_debug += 1
            elif event.key == pygame.K_u and pygame.key.get_mods() & pygame.KMOD_CTRL:
                show_debug_menu = not show_debug_menu
            elif event.key == pygame.K_b:
                show_black_outline = not show_black_outline
            elif event.key == pygame.K_v:
                show_background = not show_background
            elif event.key == pygame.K_n:
                show_blood = not show_blood
            elif event.key == pygame.K_m:
                show_tracer_lines = not show_tracer_lines
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed_debug
    if keys[pygame.K_d]:
        player_x += player_speed_debug
    if keys[pygame.K_w]:
        player_y -= player_speed_debug
    if keys[pygame.K_s]:
        player_y += player_speed_debug
    
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))
    
    for i, (enemy_x, enemy_y, _) in enumerate(enemies):
        if enemy_x < player_x:
            enemy_x += enemy_speed
        elif enemy_x > player_x:
            enemy_x -= enemy_speed
        if enemy_y < player_y:
            enemy_y += enemy_speed
        elif enemy_y > player_y:
            enemy_y -= enemy_speed
        
        dist_to_player = ((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2) ** 0.5
        if dist_to_player < 100:
            enemy_speed = 4
        else:
            enemy_speed = 2
        
        enemies[i] = (enemy_x, enemy_y, BLUE)
        
        if enemy_x < player_x + player_size and enemy_x + enemy_size > player_x and \
                enemy_y < player_y + player_size and enemy_y + enemy_size > player_y:
            restart_game()  # Reset game
    
    for i, (orange_x, orange_y, _) in enumerate(orange_enemies):
        if orange_x < player_x:
            orange_x += enemy_speed // 2
        elif orange_x > player_x:
            orange_x -= enemy_speed // 2
        if orange_y < player_y:
            orange_y += enemy_speed // 2
        elif orange_y > player_y:
            orange_y -= enemy_speed // 2
        
        orange_enemies[i] = (orange_x, orange_y, ORANGE)
        
        if orange_x < player_x + player_size and orange_x + enemy_size * 2 > player_x and \
                orange_y < player_y + player_size and orange_y + enemy_size * 2 > player_y:
            restart_game()  # Reset game
    
    for projectile in projectiles:
        projectile_x, projectile_y, angle = projectile
        projectile_x += cos(angle) * projectile_speed_debug
        projectile_y += sin(angle) * projectile_speed_debug
        projectiles.remove(projectile)
        projectiles.append((projectile_x, projectile_y, angle))
        
        for i, (enemy_x, enemy_y, _) in enumerate(enemies):
            if enemy_x < projectile_x < enemy_x + enemy_size and enemy_y < projectile_y < enemy_y + enemy_size:
                enemies.pop(i)
                if show_blood:
                    pygame.draw.circle(screen, BLOOD_RED, (int(projectile_x), int(projectile_y)), 5)
                break
        for i, (orange_x, orange_y, _) in enumerate(orange_enemies):
            if orange_x < projectile_x < orange_x + enemy_size * 2 and orange_y < projectile_y < orange_y + enemy_size * 2:
                orange_enemies.pop(i)
                if show_blood:
                    pygame.draw.circle(screen, BLOOD_RED, (int(projectile_x), int(projectile_y)), 5)
                break

    for enemy_x, enemy_y, _ in enemies:
        pygame.draw.rect(screen, BLUE, (enemy_x, enemy_y, enemy_size, enemy_size))
        if show_tracer_lines:
            pygame.draw.line(screen, WHITE, (enemy_x + enemy_size // 2, enemy_y + enemy_size // 2), (player_x + player_size // 2, player_y + player_size // 2))
    
    for orange_x, orange_y, _ in orange_enemies:
        pygame.draw.rect(screen, ORANGE, (orange_x, orange_y, enemy_size * 2, enemy_size * 2))
        if show_tracer_lines:
            pygame.draw.line(screen, WHITE, (orange_x + enemy_size, orange_y + enemy_size), (player_x + player_size // 2, player_y + player_size // 2))
    
    for projectile in projectiles:
        pygame.draw.circle(screen, PURPLE, (int(projectile[0]), int(projectile[1])), projectile_size // 2)
    
    if show_black_outline:
        pygame.draw.rect(screen, BLACK, (player_x - 2, player_y - 2, player_size + 4, player_size + 4), 2)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    
    # Draw debug menu
    if show_debug_menu:
        draw_debug_menu()
    
    pygame.display.flip()
    
    if not enemies and not orange_enemies:
        num_enemies = len(enemies) + 5
        enemies = [(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), BLUE) for _ in range(num_enemies)]
        orange_enemies = [(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), ORANGE) for _ in range(num_enemies)]
    
    pygame.time.delay(30)
