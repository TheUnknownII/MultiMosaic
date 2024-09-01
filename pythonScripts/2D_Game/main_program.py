import pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple 2D Game")

# Player character
player = pygame.Rect(50, 50, 30, 30)
player_color = (0, 128, 255)

# Items
item1 = pygame.Rect(200, 200, 20, 20)
item1_color = (255, 0, 0)

item2 = pygame.Rect(400, 300, 20, 20)
item2_color = (0, 255, 0)

item3 = pygame.Rect(400, 400, 20, 20)
item3_color = (0, 255, 0)

item4 = pygame.Rect(700, 100, 50, 50)
item4_color = (0, 255, 0)

items = [item1, item2, item3, item4]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_UP]:
        player.y -= 5
    if keys[pygame.K_DOWN]:
        player.y += 5

    for item in items:
        if player.colliderect(item):
            items.remove(item)

    screen.fill(WHITE)

    pygame.draw.rect(screen, player_color, player)
    for item in items:
        pygame.draw.rect(screen, item1_color, item)

    pygame.display.update()

    if len(items) == 0:
        running = False

pygame.quit()
