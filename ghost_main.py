import math
import random
import sys

import pygame


WIDTH, HEIGHT = 900, 620
FPS = 60
PLAYER_SPEED = 230
GHOST_SPEED = 120
GHOST_SPAWN_COUNT = 6
CRYSTAL_TARGET = 6

BLACK = (10, 10, 18)
DARK = (24, 28, 38)
BLUE = (96, 168, 255)
CYAN = (98, 236, 255)
WHITE = (245, 245, 245)
RED = (248, 85, 85)
PURPLE = (182, 126, 255)
GREEN = (113, 220, 120)
GOLD = (255, 215, 93)


class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.radius = 16
        self.speed = PLAYER_SPEED
        self.flash = 0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1

        if move.length_squared() > 0:
            move = move.normalize()
            self.pos += move * self.speed * dt

        self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(screen, BLUE, (int(self.pos.x), int(self.pos.y)), self.radius - 5)


class Ghost:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.radius = 18
        self.speed = random.uniform(GHOST_SPEED, GHOST_SPEED + 40)
        self.dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.pulse = random.random() * math.tau

    def update(self, dt, player):
        to_player = player.pos - self.pos
        if to_player.length_squared() > 0:
            self.dir = to_player.normalize()

        self.pos += self.dir * self.speed * dt

        if self.pos.x < self.radius or self.pos.x > WIDTH - self.radius:
            self.dir.x *= -1
            self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        if self.pos.y < self.radius or self.pos.y > HEIGHT - self.radius:
            self.dir.y *= -1
            self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

        self.pulse += dt * 9

    def draw(self, screen):
        body = (int(self.pos.x), int(self.pos.y))
        glow = max(0, 160 + math.sin(self.pulse) * 40)
        color = (*self.color[:3], 255)
        eye_offset = 6
        pygame.draw.circle(screen, self.color, body, self.radius)
        pygame.draw.circle(screen, (glow, glow, glow), body, self.radius - 4)
        pygame.draw.circle(screen, BLACK, (body[0] - eye_offset, body[1] - 4), 3)
        pygame.draw.circle(screen, BLACK, (body[0] + eye_offset, body[1] - 4), 3)
        pygame.draw.arc(screen, BLACK, (body[0] - 10, body[1] - 2, 20, 16), math.pi, 2 * math.pi, 2)


class Crystal:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.radius = 9
        self.angle = random.random() * math.tau

    def update(self, dt):
        self.angle += dt * 4

    def draw(self, screen):
        x = int(self.pos.x)
        y = int(self.pos.y)
        radius = int(self.radius + math.sin(self.angle) * 2)
        pygame.draw.circle(screen, GOLD, (x, y), radius)
        pygame.draw.circle(screen, WHITE, (x, y), radius - 3)


def spawn_crystals(count):
    crystals = []
    for _ in range(count):
        while True:
            x = random.randint(40, WIDTH - 40)
            y = random.randint(40, HEIGHT - 40)
            if (x, y) not in [(int(c.pos.x), int(c.pos.y)) for c in crystals]:
                crystals.append(Crystal(x, y))
                break
    return crystals


def draw_veil(screen, player):
    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 200))
    light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(light, (255, 255, 255, 120), (int(player.pos.x), int(player.pos.y)), 170)
    darkness.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    screen.blit(darkness, (0, 0))


def show_message(screen, message, submessage, color=WHITE, accent=GOLD):
    font = pygame.font.Font(None, 72)
    subfont = pygame.font.Font(None, 30)
    title = font.render(message, True, color)
    subtitle = subfont.render(submessage, True, accent)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 42)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Scary Ghost")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    player = Player()
    ghosts = [Ghost(random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40), (random.randint(180, 255), random.randint(80, 140), random.randint(80, 140))) for _ in range(GHOST_SPAWN_COUNT)]
    crystals = spawn_crystals(CRYSTAL_TARGET)
    score = 0
    game_state = "playing"
    message_timer = 0

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_state != "playing":
                player = Player()
                ghosts = [Ghost(random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40), (random.randint(180, 255), random.randint(80, 140), random.randint(80, 140))) for _ in range(GHOST_SPAWN_COUNT)]
                crystals = spawn_crystals(CRYSTAL_TARGET)
                score = 0
                game_state = "playing"

        if game_state == "playing":
            player.handle_input(dt)
            for ghost in ghosts:
                ghost.update(dt, player)

            for crystal in crystals[:]:
                crystal.update(dt)
                if player.pos.distance_to(crystal.pos) < player.radius + crystal.radius + 4:
                    crystals.remove(crystal)
                    score += 1

            for ghost in ghosts:
                if player.pos.distance_to(ghost.pos) < player.radius + ghost.radius - 2:
                    game_state = "lost"
                    message_timer = 3

            if not crystals:
                game_state = "won"
                message_timer = 5

        screen.fill(DARK)

        for i in range(0, WIDTH, 80):
            for j in range(0, HEIGHT, 80):
                pygame.draw.rect(screen, (18, 22, 30), (i, j, 80, 80), 1)

        for crystal in crystals:
            crystal.draw(screen)

        for ghost in ghosts:
            ghost.draw(screen)

        player.draw(screen)
        draw_veil(screen, player)

        screen.blit(font.render(f"Crystals: {score}/{CRYSTAL_TARGET}", True, WHITE), (20, 20))
        screen.blit(font.render("Stay alive and collect every crystal", True, CYAN), (20, HEIGHT - 38))

        if game_state != "playing":
            if game_state == "won":
                show_message(screen, "YOU SURVIVED!", "Press Enter to play again", color=GREEN, accent=WHITE)
            else:
                show_message(screen, "THE GHOSTS CAUGHT YOU", "Press Enter to try again", color=RED, accent=WHITE)

        pygame.display.flip()


if __name__ == "__main__":
    main()
