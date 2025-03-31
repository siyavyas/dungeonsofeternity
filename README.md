# Dungeons of Eternity

A web-based card game where players battle against an AI opponent using a deck of cards with various effects.

## Features

- Modern, responsive web interface
- Card-based gameplay mechanics
- Health and mana management system
- AI opponent with basic decision-making
- Menu system with instructions and game controls
- Smooth animations and transitions

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Start the Flask server:
```bash
python src/game/web/app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

## How to Play

1. You start with 100 health and 100 mana
2. Each turn, you can play one card from your hand
3. Cards cost mana to play
4. At the end of your turn, you draw a new card and gain 20 mana
5. Defeat your opponent by reducing their health to 0

## Game Controls

- Click the menu button (☰) to access game options
- Click on cards in your hand to play them
- Use the restart button to start a new game
- View instructions at any time through the menu

## Development

The game is built using:
- Flask for the web server
- HTML5 and CSS3 for the interface
- JavaScript for game logic and interactions
- SVG for card graphics

## Directory Structure

```
src/
  game/
    web/
      static/
        css/
          style.css
        js/
          game.js
        images/
          cards/
      templates/
        index.html
      app.py
requirements.txt
README.md
```
