import random
import sys

import pygame


TILE = 24
HUD = 52
FPS = 60
PLAYER_SPEED = 2.5
GHOST_SPEED = 1.8

LEVEL = [
    "####################",
    "#........#.........#",
    "#.##.###.#.###.##..#",
    "#o##.###.#.###.##o.#",
    "#..................#",
    "#.##.#.#####.#.##..#",
    "#....#...#...#.....#",
    "####.### # ###.#####",
    "   #.#       #.#    ",
    "####.# ## ## #.#####",
    "    .  #   #  .     ",
    "####.# ##### #.#####",
    "   #.#       #.#    ",
    "####.# ##### #.#####",
    "#........#.........#",
    "#.##.###.#.###.##..#",
    "#o.#.....P.....#.o.#",
    "##.#.#.#####.#.#.###",
    "#....#...G...#.....#",
    "####################",
]

COLS = len(LEVEL[0])
ROWS = len(LEVEL)
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + HUD
BLACK = (5, 5, 18)
BLUE = (30, 55, 220)
YELLOW = (255, 220, 30)
WHITE = (245, 245, 255)


def center_of(cell):
    return pygame.Vector2(cell[1] * TILE + TILE / 2, cell[0] * TILE + TILE / 2)


def cell_at(pos):
    return int(pos.y // TILE), int(pos.x // TILE)


def wall_at(row, col, walls):
    return row < 0 or row >= ROWS or col < 0 or col >= COLS or (row, col) in walls


def can_move(pos, direction, walls, radius=9):
    test = pos + direction * (radius + 2)
    row, col = cell_at(test)
    return not wall_at(row, col, walls)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 56)

    walls, pellets, power_pellets = set(), set(), set()
    player_start, ghost_starts = None, []
    for r, line in enumerate(LEVEL):
        for c, char in enumerate(line):
            if char == "#":
                walls.add((r, c))
            elif char == ".":
                pellets.add((r, c))
            elif char == "o":
                power_pellets.add((r, c))
            elif char == "P":
                player_start = (r, c)
            elif char == "G":
                ghost_starts.append((r, c))

    player = center_of(player_start)
    direction = pygame.Vector2(0, 0)
    queued_direction = pygame.Vector2(0, 0)
    ghosts = [{"pos": center_of(cell), "dir": pygame.Vector2(0, 0), "color": color}
              for cell, color in zip(ghost_starts, [(255, 70, 80), (255, 150, 210), (70, 230, 255)])]
    score, lives, power_timer = 0, 3, 0
    state = "playing"
    ghost_clock = 0

    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = {pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
                        pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
                        pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
                        pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1)}
                if event.key in keys:
                    queued_direction = pygame.Vector2(keys[event.key])
                if event.key == pygame.K_RETURN and state != "playing":
                    if state == "won":
                        pellets = {(r, c) for r, line in enumerate(LEVEL) for c, ch in enumerate(line) if ch == "."}
                        power_pellets = {(r, c) for r, line in enumerate(LEVEL) for c, ch in enumerate(line) if ch == "o"}
                        score = 0
                    player = center_of(player_start)
                    direction = pygame.Vector2(0, 0)
                    ghosts = [{"pos": center_of(cell), "dir": pygame.Vector2(0, 0), "color": color}
                              for cell, color in zip(ghost_starts, [(255, 70, 80), (255, 150, 210), (70, 230, 255)])]
                    lives, power_timer, state = 3, 0, "playing"

        if state == "playing":
            if can_move(player, queued_direction, walls):
                direction = queued_direction.copy()
            if not can_move(player, direction, walls):
                direction = pygame.Vector2(0, 0)
            player += direction * PLAYER_SPEED

            row, col = cell_at(player)
            if (row, col) in pellets:
                pellets.remove((row, col))
                score += 10
            if (row, col) in power_pellets:
                power_pellets.remove((row, col))
                score += 50
                power_timer = 8
            power_timer = max(0, power_timer - dt)

            ghost_clock -= dt
            for ghost in ghosts:
                pos = ghost["pos"]
                if ghost_clock <= 0 or (pos - center_of(cell_at(pos))).length() < 2:
                    choices = [pygame.Vector2(x, y) for x, y in ((1, 0), (-1, 0), (0, 1), (0, -1))
                               if can_move(pos, pygame.Vector2(x, y), walls)]
                    if len(choices) > 1:
                        reverse = -ghost["dir"]
                        forward = [d for d in choices if d != reverse]
                        if forward:
                            choices = forward
                    if choices:
                        if power_timer > 0 or random.random() < 0.25:
                            ghost["dir"] = random.choice(choices)
                        else:
                            ghost["dir"] = min(choices, key=lambda d: (pos + d * TILE - player).length_squared())
                if not can_move(pos, ghost["dir"], walls):
                    ghost["dir"] = pygame.Vector2(0, 0)
                ghost["pos"] += ghost["dir"] * GHOST_SPEED
            if ghost_clock <= 0:
                ghost_clock = 0.16

            for ghost in ghosts:
                if (ghost["pos"] - player).length() < 17:
                    if power_timer > 0:
                        score += 200
                        ghost["pos"] = center_of(random.choice(ghost_starts))
                        ghost["dir"] = pygame.Vector2(0, 0)
                    else:
                        lives -= 1
                        player = center_of(player_start)
                        direction = pygame.Vector2(0, 0)
                        if lives <= 0:
                            state = "game_over"
                        break
            if not pellets and not power_pellets:
                state = "won"

        screen.fill(BLACK)
        for row, col in walls:
            pygame.draw.rect(screen, BLUE, (col * TILE, row * TILE, TILE, TILE), border_radius=5)
        for row, col in pellets:
            pygame.draw.circle(screen, WHITE, (col * TILE + TILE // 2, row * TILE + TILE // 2), 3)
        for row, col in power_pellets:
            pygame.draw.circle(screen, WHITE, (col * TILE + TILE // 2, row * TILE + TILE // 2), 7)

        pygame.draw.circle(screen, YELLOW, (round(player.x), round(player.y)), 10)
        if direction.length_squared() > 0:
            angle = direction.angle_to(pygame.Vector2(1, 0))
            pygame.draw.arc(screen, BLACK, (player.x - 10, player.y - 10, 20, 20),
                            pygame.math.Vector2(1, 0).angle_to(direction) * 0.0174533 - 0.55,
                            pygame.math.Vector2(1, 0).angle_to(direction) * 0.0174533 + 0.55, 3)
        for ghost in ghosts:
            color = (50, 70, 255) if power_timer > 0 else ghost["color"]
            x, y = round(ghost["pos"].x), round(ghost["pos"].y)
            pygame.draw.circle(screen, color, (x, y - 2), 10)
            pygame.draw.rect(screen, color, (x - 10, y - 2, 20, 11))
            pygame.draw.circle(screen, WHITE, (x - 4, y - 2), 3)
            pygame.draw.circle(screen, WHITE, (x + 4, y - 2), 3)
            pygame.draw.circle(screen, BLACK, (x - 4, y - 2), 1)
            pygame.draw.circle(screen, BLACK, (x + 4, y - 2), 1)

        pygame.draw.rect(screen, BLACK, (0, ROWS * TILE, WIDTH, HUD))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (12, ROWS * TILE + 13))
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 100, ROWS * TILE + 13))
        if state != "playing":
            message = "YOU WIN!" if state == "won" else "GAME OVER"
            text = big_font.render(message, True, YELLOW)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            hint = font.render("Press Enter to play again", True, WHITE)
            screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 38)))
        pygame.display.flip()


if __name__ == "__main__":
    main()