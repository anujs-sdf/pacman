"""Generate a simple Minecraft-style world with rockets.

This is a lightweight procedural world script intended for experimentation or
local world-generation prototyping. It does not create a real Minecraft Java
world file, but it produces a structured world map you can adapt for plugins,
modding tools, or custom generators.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

WORLD_WIDTH = 32
WORLD_HEIGHT = 16
WORLD_DEPTH = 32


class Block:
    def __init__(self, x: int, y: int, z: int, block_type: str):
        self.x = x
        self.y = y
        self.z = z
        self.block_type = block_type

    def __repr__(self) -> str:
        return f"Block({self.x}, {self.y}, {self.z}, {self.block_type})"


class World:
    def __init__(self, width: int, height: int, depth: int):
        self.width = width
        self.height = height
        self.depth = depth
        self.grid = [[["air" for _ in range(depth)] for _ in range(width)] for _ in range(height)]

    def set_block(self, x: int, y: int, z: int, block_type: str):
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            self.grid[y][x][z] = block_type

    def get_block(self, x: int, y: int, z: int) -> str:
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            return self.grid[y][x][z]
        return "out_of_bounds"

    def save_to_file(self, filename: str):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            f.write("# Minecraft-inspired world export\n")
            f.write(f"width={self.width} height={self.height} depth={self.depth}\n")
            for y in range(self.height):
                for x in range(self.width):
                    for z in range(self.depth):
                        block = self.get_block(x, y, z)
                        if block != "air":
                            f.write(f"{x},{y},{z},{block}\n")

    def add_ground(self):
        for x in range(self.width):
            for z in range(self.depth):
                self.set_block(x, 0, z, "grass")
                for y in range(1, 3):
                    self.set_block(x, y, z, "dirt")

    def add_trees(self, count: int):
        for _ in range(count):
            x = random.randint(2, self.width - 3)
            z = random.randint(2, self.depth - 3)
            y = 3
            trunk_height = random.randint(3, 5)
            for i in range(trunk_height):
                self.set_block(x, y + i, z, "log")
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    for dy in range(0, 3):
                        if abs(dx) + abs(dz) + dy <= 4:
                            self.set_block(x + dx, y + trunk_height + dy - 1, z + dz, "leaves")

    def add_rocket(self, x: int, z: int):
        base_y = 3
        body = [(0, base_y, 0), (0, base_y + 1, 0), (0, base_y + 2, 0), (0, base_y + 3, 0)]
        for bx, by, bz in body:
            self.set_block(x + bx, by, z + bz, "stone")

        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if abs(dx) + abs(dz) == 0:
                    continue
                self.set_block(x + dx, base_y + 1, z + dz, "iron")

        for dx in range(-1, 2):
            self.set_block(x + dx, base_y + 4, z, "redstone")

        self.set_block(x, base_y + 5, z, "glass")

        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if abs(dx) + abs(dz) == 2:
                    self.set_block(x + dx, base_y + 1, z + dz, "gold")

        self.set_block(x, base_y - 1, z, "obsidian")

    def add_rocket_field(self, rocket_count: int):
        for _ in range(rocket_count):
            x = random.randint(4, self.width - 5)
            z = random.randint(4, self.depth - 5)
            self.add_rocket(x, z)

    def add_lava_pool(self, x: int, z: int, radius: int = 3):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if dx * dx + dz * dz <= radius * radius:
                    self.set_block(x + dx, 3, z + dz, "lava")



def generate_world(filename: str = "minecraft/rocket_world.txt"):
    world = World(WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH)
    world.add_ground()
    world.add_trees(10)
    world.add_rocket_field(4)
    world.add_lava_pool(20, 20, radius=4)
    world.save_to_file(filename)
    print(f"World saved to {filename}")


if __name__ == "__main__":
    generate_world()
