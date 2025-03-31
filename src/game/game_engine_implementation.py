import pygame
import random
import json

class Game:
    def __init__(self, player1_name, player2_name):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dungeons of Eternity")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.players = []
        self.resources = {}
        self.current_turn = 0
        
        # Initialize players
        self.players.append({"name": player1_name, "health": 100, "position": (100, 100)})
        self.players.append({"name": player2_name, "health": 100, "position": (200, 200)})

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass  # Add game logic updates here

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw players
        for player in self.players:
            pygame.draw.circle(self.screen, (255, 255, 255), player["position"], 20)
        
        # Update display
        pygame.display.flip()
        self.clock.tick(60)

    def start_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        
        pygame.quit()

    def to_json(self):
        return json.dumps({
            "players": self.players,
            "resources": self.resources,
            "current_turn": self.current_turn
        })