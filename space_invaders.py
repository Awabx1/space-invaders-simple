
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders (Example)")

# Clock to control the game's frame rate
clock = pygame.time.Clock()

# Load images (You can replace these placeholders with your own images)
# For simplicity, we'll create colored rectangles using Surface if no images are available.
player_image = pygame.Surface((40, 40))
player_image.fill((0, 255, 0))  # Green square as a placeholder for the player
enemy_image = pygame.Surface((40, 40))
enemy_image.fill((255, 0, 0))   # Red square as a placeholder for the enemies
bullet_image = pygame.Surface((5, 20))
bullet_image.fill((255, 255, 0))  # Yellow rectangle as a placeholder for bullets

# Game constants
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2
ENEMY_DROP = 40  # How far enemies move down when they switch directions
NUM_ENEMIES = 6

# Player class
class Player:
    def __init__(self):
        self.image = player_image
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.speed = PLAYER_SPEED
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
    
    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.image.get_width():
            self.x = SCREEN_WIDTH - self.image.get_width()

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.image = enemy_image
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.move_direction = 1  # 1 = move right, -1 = move left

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def update(self):
        self.x += self.speed * self.move_direction

    def drop_down(self):
        self.y += ENEMY_DROP
        self.move_direction *= -1  # Reverse direction

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.image = bullet_image
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.active = True  # If False, remove the bullet
    
    def draw(self, surface):
        if self.active:
            surface.blit(self.image, (self.x, self.y))
    
    def update(self):
        if self.active:
            self.y -= self.speed
            if self.y < 0:
                self.active = False

# Helper function: collision detection
def is_collision(obj1_x, obj1_y, obj2_x, obj2_y, distance_threshold=27):
    # Simple distance-based collision
    distance = math.sqrt((obj1_x - obj2_x)**2 + (obj1_y - obj2_y)**2)
    return distance < distance_threshold

# Initialize player
player = Player()

# Create enemies in a row
enemies = []
for i in range(NUM_ENEMIES):
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_image.get_width())
    enemy_y = random.randint(20, 120)
    enemies.append(Enemy(enemy_x, enemy_y))

# List to hold bullets
bullets = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
while running:
    clock.tick(60)  # Limit to 60 FPS
    screen.fill(BLACK)

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE:
                # Fire bullet
                bullet_x = player.x + player_image.get_width() // 2 - bullet_image.get_width() // 2
                bullet_y = player.y
                bullets.append(Bullet(bullet_x, bullet_y))

    # Continuous movement checks (for holding down keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Update and draw player
    player.draw(screen)

    # Update bullets
    for bullet in bullets:
        bullet.update()
        bullet.draw(screen)
    
    # Remove inactive bullets
    bullets = [b for b in bullets if b.active]

    # Update enemies
    for enemy in enemies:
        enemy.update()
        # Check if enemy hits screen boundary
        if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy_image.get_width():
            # Move all enemies down
            for e in enemies:
                e.drop_down()
            break

    # Check collisions
    for enemy in enemies:
        for bullet in bullets:
            if bullet.active and is_collision(
                enemy.x + enemy_image.get_width() / 2,
                enemy.y + enemy_image.get_height() / 2,
                bullet.x + bullet_image.get_width() / 2,
                bullet.y + bullet_image.get_height() / 2
            ):
                # Reset enemy and deactivate bullet
                bullet.active = False
                score += 1
                enemy.x = random.randint(0, SCREEN_WIDTH - enemy_image.get_width())
                enemy.y = random.randint(20, 120)
                break

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Check if any enemy has reached the bottom (game over condition)
    for enemy in enemies:
        if enemy.y > SCREEN_HEIGHT - 60:
            running = False
            break

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()