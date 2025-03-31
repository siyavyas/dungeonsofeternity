import pygame
import json

class Game:
    def __init__(self, player1_name, player2_name):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dungeons of Eternity")
        
        # UI colors
        self.colors = {
            "background": (40, 44, 52),
            "text": (255, 255, 255),
            "button": (61, 90, 128),
            "button_hover": (75, 110, 156),
            "health_bar": (235, 64, 52),
            "mana_bar": (52, 152, 235)
        }
        
        # UI fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        
        # Game state
        self.players = [
            {"name": player1_name, "health": 100, "mana": 10, "position": (100, 100)},
            {"name": player2_name, "health": 100, "mana": 10, "position": (200, 200)}
        ]
        self.current_turn = 0
        self.running = True
        self.clock = pygame.time.Clock()

    def draw_text(self, text, position, color=None):
        if color is None:
            color = self.colors["text"]
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_button(self, text, rect, action=None):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.colors["button_hover"], rect)
            if clicked and action:
                action()
        else:
            pygame.draw.rect(self.screen, self.colors["button"], rect)
        
        # Center text in button
        text_surface = self.font.render(text, True, self.colors["text"])
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_health_bar(self, player, position):
        bar_width = 200
        bar_height = 20
        health_percentage = player["health"] / 100
        
        # Background (empty health)
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (position[0], position[1], bar_width, bar_height))
        
        # Foreground (current health)
        pygame.draw.rect(self.screen, self.colors["health_bar"],
                        (position[0], position[1], bar_width * health_percentage, bar_height))
        
        # Health text
        health_text = f"{player['name']}: {player['health']}/100"
        self.draw_text(health_text, (position[0], position[1] - 25))

    def draw_mana_bar(self, player, position):
        bar_width = 200
        bar_height = 20
        mana_percentage = player["mana"] / 10
        
        # Background (empty mana)
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (position[0], position[1], bar_width, bar_height))
        
        # Foreground (current mana)
        pygame.draw.rect(self.screen, self.colors["mana_bar"],
                        (position[0], position[1], bar_width * mana_percentage, bar_height))
        
        # Mana text
        mana_text = f"Mana: {player['mana']}/10"
        self.draw_text(mana_text, (position[0], position[1] - 25))

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
        self.screen.fill(self.colors["background"])
        
        # Draw player health bars
        self.draw_health_bar(self.players[0], (50, 50))
        self.draw_health_bar(self.players[1], (50, 150))
        
        # Draw player mana bars
        self.draw_mana_bar(self.players[0], (300, 50))
        self.draw_mana_bar(self.players[1], (300, 150))
        
        # Draw turn indicator
        turn_text = f"Turn: {self.current_turn}"
        self.draw_text(turn_text, (self.screen_width - 200, 50))
        
        # Draw buttons
        draw_button = pygame.Rect(50, self.screen_height - 100, 200, 50)
        end_turn_button = pygame.Rect(300, self.screen_height - 100, 200, 50)
        self.draw_button("Draw Card", draw_button)
        self.draw_button("End Turn", end_turn_button)
        
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
            "current_turn": self.current_turn
        })