# MNK-Game
A flexible and extensible implementation of the (m, n, k)-game — a generalization of Tic-Tac-Toe — written in Python using Pygame. Players can compete against each other or various types of AI bots with adjustable difficulty. 

## 🎮 Features

- 🧑‍🤝‍🧑 **Multiple Game Modes**:
  - Player vs Player (PvP)
  - Player vs Bot
  - Bot vs Bot

- 🤖 **Bot Types**:
  - Random Bot
  - Weak Bot
  - Strong Bot (using custom payoff evaluation)
  - (Planned) Unbeatable Bot

- 🎨 **Graphical Interface (Pygame)**:
  - Button-based game mode selection
  - Visual win detection and draw handling

## 🚀 Starting the Game
To run the game manually in a Python environment (e.g. console, script, Jupyter, or REPL), follow these steps:



# 1. Create a new game instance
game = Game()

# 2. Start the game (select board size and win condition)
game.start()

# 3. Choose player types (e.g. Player vs Bot, Bot vs Bot)
# Example: (0, 1) = human vs human | (1, 1) = human vs soft bot | (1, 2) = human vs strong human

# 4. Launch the game loop
game.game_loop()
