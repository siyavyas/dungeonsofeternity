```python
from flask import Flask, jsonify, request
import random
import json

app = Flask(__name__)

# Card System
class Card:
    def __init__(self, name, cost, effect):
        self.name = name
        self.cost = cost
        self.effect = effect

    def __repr__(self):
        return f"{self.name} (Cost: {self.cost})"

class Deck:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(random.randint(0, len(self.cards) - 1))
        return None

# Movement System
class Player:
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.position = position
        self.health = 100

    def move(self, direction):
        if direction == "up":
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == "down":
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == "left":
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + 1, self.position[1])

# Combat System
class Combat:
    @staticmethod
    def attack(attacker, defender, damage):
        defender.health -= damage
        if defender.health < 0:
            defender.health = 0

# Resource Management
class Resource:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def gather(self, amount):
        self.amount += amount

    def spend(self, amount):
        if self.amount >= amount:
            self.amount -= amount
            return True
        return False

# Game State Management
class GameState:
    def __init__(self):
        self.players = []
        self.resources = {}
        self.current_turn = 0

    def add_player(self, player):
        self.players.append(player)

    def add_resource(self, resource):
        self.resources[resource.name] = resource

    def next_turn(self):
        self.current_turn += 1

    def to_json(self):
        return json.dumps({
            "players": [{"name": player.name, "position": player.position, "health": player.health} for player in self.players],
            "resources": {name: resource.amount for name, resource in self.resources.items()},
            "current_turn": self.current_turn
        })

# Initialize game state
game_state = GameState()

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    player = Player(data['name'])
    game_state.add_player(player)
    return jsonify({"message": f"Player {player.name} added."})

@app.route('/move_player', methods=['POST'])
def move_player():
    data = request.json
    player = next((p for p in game_state.players if p.name == data['name']), None)
    if player:
        player.move(data['direction'])
        return jsonify({"message": f"{player.name} moved {data['direction']}.", "position": player.position})
    return jsonify({"error": "Player not found."}), 404

@app.route('/draw_card', methods=['POST'])
def draw_card():
    card = deck.draw_card()
    return jsonify({"card": str(card) if card else "No cards left."})

@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    attacker = next((p for p in game_state.players if p.name == data['attacker']), None)
    defender = next((p for p in game_state.players if p.name == data['defender']), None)
    if attacker and defender:
        Combat.attack(attacker, defender, data['damage'])
        return jsonify({"message": f"{attacker.name} attacked {defender.name}.", "defender_health": defender.health})
    return jsonify({"error": "Attacker or defender not found."}), 404

@app.route('/next_turn', methods=['POST'])
def next_turn():
    game_state.next_turn()
    return jsonify({"message": "Turn advanced.", "current_turn": game_state.current_turn})

@app.route('/game_state', methods=['GET'])
def get_game_state():
    return jsonify(json.loads(game_state.to_json()))

# Example Usage
if __name__ == "__main__":
    # Create cards
    fireball = Card("Fireball", 5, "Deal 10 damage")
    heal = Card("Heal", 3, "Restore 10 health")

    # Create a deck and add cards
    deck = Deck()
    deck.add_card(fireball)
    deck.add_card(heal)

    # Run the Flask app
    app.run(debug=True)
```

This code provides a web-compatible game interface using Flask, allowing players to be added, moved, and attacked through HTTP requests. The game state can be queried, and card drawing is handled via API endpoints. This structure is designed to be intuitive and engaging for users, facilitating interaction with the game through a web browser.