#!/usr/bin/env python3
"""
Dungeons of Eternity - Main Entry Point
"""

import sys
import logging
from pathlib import Path
from flask import Flask, jsonify, request, send_file
import json
from io import BytesIO
from visual_asset_generation import VisualAssetGenerator
from core_mechanics_implementation import Game

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add game directory to Python path
game_dir = Path(__file__).parent
sys.path.append(str(game_dir))

# Initialize Flask app
app = Flask(__name__)

# Initialize game systems
game = Game("Player1", "Player2")
asset_generator = VisualAssetGenerator()

@app.route('/')
def home():
    """Serve the main game page"""
    return """
    <html>
        <head>
            <title>Dungeons of Eternity</title>
            <style>
                body { 
                    margin: 0; 
                    padding: 0; 
                    background: #000; 
                    color: #fff;
                    font-family: 'Arial', sans-serif;
                    overflow: hidden;
                }
                #game-container { 
                    width: 100vw; 
                    height: 100vh; 
                    position: relative;
                    display: flex;
                    flex-direction: column;
                }
                #background { 
                    position: absolute;
                    width: 100%; 
                    height: 100%; 
                    object-fit: cover;
                    z-index: 0;
                }
                #game-ui { 
                    position: relative;
                    width: 100%; 
                    height: 100%;
                    z-index: 1;
                    display: grid;
                    grid-template-rows: auto 1fr auto;
                    padding: 20px;
                    box-sizing: border-box;
                }
                #hud {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px;
                    background: rgba(0, 0, 0, 0.7);
                    border-radius: 10px;
                }
                #game-board {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex: 1;
                    position: relative;
                }
                #player-area {
                    position: absolute;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 20px;
                }
                #hand {
                    display: flex;
                    gap: 10px;
                    padding: 10px;
                    background: rgba(0, 0, 0, 0.7);
                    border-radius: 10px;
                }
                .card { 
                    width: 150px; 
                    height: 200px; 
                    margin: 5px;
                    display: inline-block;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    transition: transform 0.2s;
                    cursor: pointer;
                }
                .card:hover {
                    transform: translateY(-10px);
                }
                .character { 
                    width: 64px; 
                    height: 64px; 
                    margin: 5px;
                    display: inline-block;
                    transition: transform 0.2s;
                }
                .character:hover {
                    transform: scale(1.1);
                }
                .health-bar {
                    width: 200px;
                    height: 20px;
                    background: rgba(255, 0, 0, 0.3);
                    border-radius: 10px;
                    overflow: hidden;
                }
                .health-fill {
                    height: 100%;
                    background: #ff0000;
                    transition: width 0.3s;
                }
                .mana-bar {
                    width: 200px;
                    height: 20px;
                    background: rgba(0, 0, 255, 0.3);
                    border-radius: 10px;
                    overflow: hidden;
                }
                .mana-fill {
                    height: 100%;
                    background: #0000ff;
                    transition: width 0.3s;
                }
                .action-button {
                    padding: 10px 20px;
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    border-radius: 5px;
                    color: white;
                    cursor: pointer;
                    transition: background 0.2s;
                }
                .action-button:hover {
                    background: rgba(255, 255, 255, 0.3);
                }
                #turn-indicator {
                    position: absolute;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: rgba(0, 0, 0, 0.7);
                    padding: 10px 20px;
                    border-radius: 20px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div id="game-container">
                <img id="background" src="/generate_background/dungeon" alt="Background">
                <div id="game-ui">
                    <div id="hud">
                        <div class="health-bar">
                            <div class="health-fill" style="width: 80%"></div>
                        </div>
                        <div class="mana-bar">
                            <div class="mana-fill" style="width: 60%"></div>
                        </div>
                        <div id="turn-indicator">Turn 1</div>
                    </div>
                    <div id="game-board">
                        <div id="player-area">
                            <div id="hand"></div>
                        </div>
                    </div>
                    <div id="controls">
                        <button class="action-button" onclick="drawCard()">Draw Card</button>
                        <button class="action-button" onclick="nextTurn()">Next Turn</button>
                    </div>
                </div>
            </div>
            <script>
                let currentTurn = 1;
                let playerHealth = 80;
                let playerMana = 60;

                // Load game assets
                function loadGameAssets() {
                    // Load background
                    document.getElementById('background').src = '/generate_background/dungeon';
                    
                    // Load initial cards
                    drawCard();
                    drawCard();
                    drawCard();
                }

                // Draw a card
                async function drawCard() {
                    try {
                        const response = await fetch('/draw_card', { method: 'POST' });
                        const data = await response.json();
                        if (data.card) {
                            const card = document.createElement('img');
                            card.src = `/generate_card/${data.card.toLowerCase()}?type=spell`;
                            card.className = 'card';
                            document.getElementById('hand').appendChild(card);
                        }
                    } catch (error) {
                        console.error('Error drawing card:', error);
                    }
                }

                // Advance to next turn
                async function nextTurn() {
                    try {
                        const response = await fetch('/next_turn', { method: 'POST' });
                        const data = await response.json();
                        currentTurn++;
                        document.getElementById('turn-indicator').textContent = `Turn ${currentTurn}`;
                        
                        // Update player stats
                        playerHealth = Math.min(100, playerHealth + 5);
                        playerMana = Math.min(100, playerMana + 10);
                        updateStats();
                    } catch (error) {
                        console.error('Error advancing turn:', error);
                    }
                }

                // Update player stats
                function updateStats() {
                    document.querySelector('.health-fill').style.width = `${playerHealth}%`;
                    document.querySelector('.mana-fill').style.width = `${playerMana}%`;
                }

                // Load assets when page loads
                window.onload = loadGameAssets;
            </script>
        </body>
    </html>
    """

@app.route('/generate_background/<theme>')
def generate_background(theme):
    """Generate and serve a background image"""
    try:
        image = asset_generator.generate_background(theme)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_character/<character_type>')
def generate_character(character_type):
    """Generate and serve a character sprite"""
    try:
        image = asset_generator.generate_character_sprite(character_type)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_card/<card_name>')
def generate_card(card_name):
    """Generate and serve card artwork"""
    try:
        card_type = request.args.get('type', 'spell')
        image = asset_generator.generate_card_art(card_name, card_type)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/draw_card', methods=['POST'])
def draw_card():
    """Draw a card from the deck"""
    card = game.draw_card()
    return jsonify({"card": str(card) if card else "No cards left."})

@app.route('/next_turn', methods=['POST'])
def next_turn():
    """Advance to the next turn"""
    game.next_turn()
    return jsonify({"message": "Turn advanced.", "current_turn": game.current_turn})

@app.route('/game_state', methods=['GET'])
def get_game_state():
    """Get the current game state"""
    return jsonify(json.loads(game.to_json()))

def run_web():
    """Run the web server"""
    app.run(host='0.0.0.0', port=5001, debug=True)

def run_desktop():
    """Run the desktop version"""
    # Initialize game
    game.start_game()
    
    # Main game loop
    while True:
        # Get player input
        action = input("Enter action (draw/next/quit): ")
        
        if action == "draw":
            card = game.draw_card()
            print(f"Drew card: {card}")
        elif action == "next":
            game.next_turn()
            print(f"Turn {game.current_turn}")
        elif action == "quit":
            break
        else:
            print("Invalid action")

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        run_web()
    else:
        run_desktop()

if __name__ == "__main__":
    main()

