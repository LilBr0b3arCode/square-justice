import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chase Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Define square sizes and initial positions
player_size = 30
enemy_size = 30
enemy_speed = 2
player_speed = 5
player_x, player_y = WIDTH // 2, HEIGHT // 2
enemies = [(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), BLUE) for _ in range(5)]
orange_enemies = [(random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size), ORANGE)]

# Define projectile variables
projectile_size = 10
projectiles = []

# Main game loop
while True:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    
    # Keep the player inside the screen
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))
    
    # Enemy (blue square) movement
    for i, (enemy_x, enemy_y, _) in enumerate(enemies):
        if enemy_x < player_x:
            enemy_x += enemy_speed
        elif enemy_x > player_x:
            enemy_x -= enemy_speed
        if enemy_y < player_y:
            enemy_y += enemy_speed
        elif enemy_y > player_y:
            enemy_y -= enemy_speed
        enemies[i] = (enemy_x, enemy_y, BLUE)

        # Check if enemy collides with player
        if enemy_x < player_x + player_size and enemy_x + enemy_size > player_x and \
                enemy_y < player_y + player_size and enemy_y + enemy_size > player_y:
            print("You collided with a blue enemy!")
            player_x, player_y = WIDTH // 2, HEIGHT // 2  # Reset player position
    
    # Orange enemy (slower and bigger)
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
        
        # Check if orange enemy collides with player
        if orange_x < player_x + player_size and orange_x + enemy_size * 2 > player_x and \
                orange_y < player_y + player_size and orange_y + enemy_size * 2 > player_y:
            print("You collided with an orange enemy!")
            player_x, player_y = WIDTH // 2, HEIGHT // 2  # Reset player position
    
    # Projectile movement
    for i, (projectile_x, projectile_y, _, direction) in enumerate(projectiles):
        if direction == "left":
            projectile_x -= enemy_speed * 2
        elif direction == "right":
            projectile_x += enemy_speed * 2
        elif direction == "up":
            projectile_y -= enemy_speed * 2
        elif direction == "down":
            projectile_y += enemy_speed * 2
        projectiles[i] = (projectile_x, projectile_y, YELLOW, direction)

        # Check if projectile collides with player
        if projectile_x < player_x + player_size and projectile_x + projectile_size > player_x and \
                projectile_y < player_y + player_size and projectile_y + projectile_size > player_y:
            print("You got hit by a projectile!")
            player_x, player_y = WIDTH // 2, HEIGHT // 2  # Reset player position
            projectiles.pop(i)  # Remove projectile
    
    # Draw player (red square)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    
    # Draw enemies (blue squares)
    for enemy_x, enemy_y, color in enemies:
        pygame.draw.rect(screen, color, (enemy_x, enemy_y, enemy_size, enemy_size))
    
    # Draw orange enemies (orange squares)
    for orange_x, orange_y, color in orange_enemies:
        pygame.draw.rect(screen, color, (orange_x, orange_y, enemy_size * 2, enemy_size * 2))
    
    # Draw projectiles (yellow squares)
    for projectile_x, projectile_y, color, _ in projectiles:
        pygame.draw.rect(screen, color, (projectile_x, projectile_y, projectile_size, projectile_size))
    
    # Update the display
    pygame.display.flip()
    
    # Generate projectiles
    if random.randint(0, 100) < 2:
        enemy_x, enemy_y, _ = random.choice(enemies)
        direction = random.choice(["left", "right", "up", "down"])
        projectiles.append((enemy_x, enemy_y, YELLOW, direction))
    
    pygame.time.delay(30)  # Add a short delay to slow down the game
