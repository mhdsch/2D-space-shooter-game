import pygame
import random


pygame.init()


screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")


background_img = pygame.image.load("background.png")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")   
bullet_img = pygame.image.load("bullet.png")


font = pygame.font.SysFont("Arial", 30)


clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 50
        self.bullets = []

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def draw(self):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw()


class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 4)

    def draw(self):
        screen.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


player = Player()
enemies = []
score = 0
game_over = False
while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE:
                player.shoot()

    
    player.update()
    for enemy in enemies:
        enemy.update()
        if enemy.rect.colliderect(player.rect):
            game_over = True
        for bullet in player.bullets:
            if bullet.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                player.bullets.remove(bullet)
                score += 10

    
    if len(enemies) < 10 and random.randint(0, 100) < 5:
        enemy = Enemy()
        enemies.append(enemy)

    
    screen.blit(background_img, (0, 0))
    player.draw()
    for enemy in enemies:
        enemy.draw()
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    
    clock.tick(60)


pygame.quit()