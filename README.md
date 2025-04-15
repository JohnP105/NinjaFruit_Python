# 🥷 NinjaFruit Game

A Python implementation of a Fruit Ninja-style game with OS concepts integration.

## 🚀 Features

- Slice falling fruits with mouse swipes
- Avoid bombs (lose points if sliced)
- High score tracking
- Multiprocessing for fruit spawning
- Thread-safe operations
- Signal handling for graceful shutdown

## 🛠️ Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the game:

```bash
python ninja_fruit.py
```

## 🎮 How to Play

- Click and drag to slice fruits
- Fruits give 10 points
- Bombs deduct 20 points
- Press Ctrl+C to quit and save high score

## 🧠 OS Concepts Implemented

- Process Creation & IPC (fruit spawner)
- Threading (game loop, collision detection)
- Synchronization (locks for shared resources)
- Signal Handling (SIGINT for graceful shutdown)
