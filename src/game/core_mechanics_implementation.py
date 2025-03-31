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
class Game:
    def __init__(self, player1_name, player2_name):
        self.players = []
        self.resources = {}
        self.current_turn = 0
        self.deck = Deck()
        
        # Initialize players
        self.players.append(Player(player1_name))
        self.players.append(Player(player2_name))
        
        # Initialize deck with some cards
        self.deck.add_card(Card("Fireball", 5, "Deal 10 damage"))
        self.deck.add_card(Card("Heal", 3, "Restore 10 health"))

    def add_player(self, player):
        self.players.append(player)

    def add_resource(self, resource):
        self.resources[resource.name] = resource

    def next_turn(self):
        self.current_turn += 1

    def draw_card(self):
        return self.deck.draw_card()

    def to_json(self):
        return json.dumps({
            "players": [{"name": player.name, "position": player.position, "health": player.health} for player in self.players],
            "resources": {name: resource.amount for name, resource in self.resources.items()},
            "current_turn": self.current_turn
        })

    def start_game(self):
        """Initialize and start the game"""
        # Add initial resources
        self.add_resource(Resource("Gold", 50))
        self.add_resource(Resource("Mana", 10))
        return self.to_json()