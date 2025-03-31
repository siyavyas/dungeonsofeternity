from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import random
from pathlib import Path

app = Flask(__name__)

# Get the assets directory path
ASSETS_DIR = Path(__file__).parent.parent / 'assets'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assets/<path:filename>')
def serve_asset(filename):
    """Serve assets from the assets directory"""
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    return jsonify({
        'playerHealth': 100,
        'playerMana': 100,
        'enemyHealth': 100,
        'currentTurn': 'player'
    })

@app.route('/api/play-card', methods=['POST'])
def play_card():
    """Handle card being played"""
    data = request.json
    return jsonify({
        'success': True,
        'message': f"Card {data.get('cardId')} played successfully",
        'effects': {
            'damage': random.randint(10, 30) if data.get('type') == 'attack' else 0,
            'healing': random.randint(10, 20) if data.get('type') == 'heal' else 0
        }
    })

@app.route('/api/end-turn', methods=['POST'])
def end_turn():
    """Handle end of turn"""
    return jsonify({
        'success': True,
        'enemyAction': {
            'type': 'attack',
            'damage': random.randint(5, 15)
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True) 