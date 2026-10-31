# Game Collection Repository

This repository contains a small collection of playful game prototypes and experiments built in Python, plus a Roblox scripting example and a Minecraft-inspired world generator.

## Included projects

### 1. Pac-Man clone
- File: `pacman_main.py`
- Description: a classic top-down Pac-Man style arcade game built with Pygame.
- Run:

```pwsh
cd "C:\Users\Admin\Desktop\PACMAN\pacman"
python .\pacman_main.py
```

### 2. Scary ghost survival game
- File: `ghost_main.py`
- Description: a standalone spooky survival game where the player avoids chasing ghosts and collects crystals.
- Run:

```pwsh
cd "C:\Users\Admin\Desktop\PACMAN\pacman"
python .\ghost_main.py
```

### 3. Roblox sword arena prototype
- File: `roblox.py`
- File: `ROBLOX_DEPLOYMENT.md`
- Description: contains Roblox Lua for a sword-fighting arena game. Paste the Lua script into a Script under `ServerScriptService` in Roblox Studio.
- Quick steps:
  1. Open Roblox Studio.
  2. Insert a Script into `ServerScriptService`.
  3. Paste the Lua code from `roblox.py`.
  4. Press Play to test.
  5. Publish the experience to Roblox.

### 4. Minecraft-inspired rocket world generator
- Folder: `minecraft/`
- Files:
  - `minecraft/minecraft_rocket_world.py`
  - `minecraft/rocket_world.txt`
  - `minecraft/README.md`
- Description: a lightweight procedural generator that creates a small Minecraft-style world with trees, lava, and rocket structures.
- Run:

```pwsh
cd "C:\Users\Admin\Desktop\PACMAN\pacman"
python .\minecraft\minecraft_rocket_world.py
```

## Setup

### Python and Pygame
If you do not already have Pygame installed, run:

```pwsh
py -m pip install pygame
```

### Docker / Nginx static setup
This repository also includes a basic Nginx static-site container setup for hosting a web page version of the project.

Files:
- `Dockerfile`
- `docker-compose.yml`
- `nginx.conf`
- `index.html`

Run:

```pwsh
cd "C:\Users\Admin\Desktop\PACMAN\pacman"
docker compose up --build
```

Then open:

```text
http://localhost:8080
```

## Great Bharat: culture, diversity, and greatness

Great Bharat is one of the oldest and richest civilizations in the world. It has shaped ideas in philosophy, science, mathematics, art, literature, and spirituality for thousands of years. From the ancient Indus Valley culture to later empires like the Mauryas and Guptas, Bharat has always been a land of wisdom, creativity, and resilience.

Its culture is deeply diverse. Bharat has many languages, traditions, religions, foods, clothing styles, music forms, and festivals. Yet despite this diversity, there is a strong spirit of unity, tolerance, and coexistence. Festivals such as Diwali, Holi, Navratri, Eid, Christmas, and many regional celebrations show how different communities live together with respect and harmony.

Bharat is also rich in values. It has long emphasized family, respect for elders, discipline, hospitality, and spiritual growth. Its literature, such as the Ramayana and Mahabharata, and its classical arts continue to inspire generations.

In science and knowledge, Bharat has made remarkable contributions. Ancient scholars advanced ideas in mathematics, astronomy, medicine, architecture, and philosophy. The concept of zero, Ayurveda, and major astronomical discoveries are just a few examples of Bharat’s intellectual greatness.

In simple words, Bharat is great because it combines ancient wisdom with modern progress, tradition with innovation, and diversity with unity. It is a living example of cultural richness and human greatness.

## Repository notes
- The Python games are desktop prototypes and are meant to run locally.
- The Roblox content is a script for Roblox Studio and is not a standalone executable.
- The Minecraft project is a prototype generator and is not a real Java Edition save file.
- The project is intended for experimentation, learning, and game prototyping.

## GitHub
This repository is set up for version control and can be pushed to GitHub using standard git commands.

Example:

```bash
git add .
git commit -m "Update game collection"
git push origin main
```

## License
This repository is a personal project and may include third-party code references. Please check the included license files if you plan to redistribute or commercialize the project.
