```python
import random
import json

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

# Example Usage
if __name__ == "__main__":
    # Create cards
    fireball = Card("Fireball", 5, "Deal 10 damage")
    heal = Card("Heal", 3, "Restore 10 health")

    # Create a deck and add cards
    deck = Deck()
    deck.add_card(fireball)
    deck.add_card(heal)

    # Create players
    player1 = Player("Hero")
    player2 = Player("Villain")

    # Create game state
    game_state = GameState()
    game_state.add_player(player1)
    game_state.add_player(player2)
    game_state.add_resource(Resource("Gold", 50))

    # Simulate game actions
    player1.move("up")
    card_drawn = deck.draw_card()
    print(f"{player1.name} drew {card_drawn}")

    Combat.attack(player1, player2, 10)
    print(f"{player2.name} health: {player2.health}")

    game_state.next_turn()
    print(game_state.to_json())
```

This code provides a foundational structure for a tactical card-based game, including a card system, player movement, combat mechanics, resource management, and game state management. It is designed to be executed in a Python environment and can be adapted for web platforms using frameworks like Flask or Django for backend integration.