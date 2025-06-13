from models.enemy import Enemy
from models.battle import Battle
import pygame
import math
import random

class GamePart2:
    def __init__(self, game):
        self.game = game
        
    def update_camera(self):
        # Adjust camera position to center on player
        self.game.camera_x = self.game.player.x - self.game.VISIBLE_TILES_X // 2
        self.game.camera_y = self.game.player.y - self.game.VISIBLE_TILES_Y // 2
        
        # Ensure camera doesn't show outside the map
        self.game.camera_x = max(0, min(self.game.camera_x, self.game.MAP_WIDTH - self.game.VISIBLE_TILES_X))
        self.game.camera_y = max(0, min(self.game.camera_y, self.game.MAP_HEIGHT - self.game.VISIBLE_TILES_Y))
    
    def check_enemy_encounter(self):
        # Increase encounter rate by 20%
        base_chance = 0.3  # 25% increased by 20% = 30%
        if self.game.map[self.game.player.y][self.game.player.x] == self.game.FOREST:
            base_chance = 0.48  # 40% increased by 20% = 48%
        
        if self.game.player.steps % 10 == 0 and random.random() < base_chance:
            enemy = Enemy(self.game.player.level)
            self.game.battle = Battle(self.game.player, enemy, self.game.SCREEN_WIDTH)
            self.game.game_state = "battle"
    
    def draw_map(self):
        self.update_camera()
        
        # Draw the map
        for y in range(self.game.VISIBLE_TILES_Y + 1):
            for x in range(self.game.VISIBLE_TILES_X + 1):
                map_x = x + self.game.camera_x
                map_y = y + self.game.camera_y
                
                if 0 <= map_x < self.game.MAP_WIDTH and 0 <= map_y < self.game.MAP_HEIGHT:
                    tile_type = self.game.map[map_y][map_x]
                    if tile_type == self.game.GRASS:  # Grassland
                        color = self.game.GREEN
                    elif tile_type == self.game.WALL:  # Wall (rock)
                        color = self.game.BROWN
                    elif tile_type == self.game.FOREST:  # Forest
                        color = self.game.DARK_GREEN
                    elif tile_type == self.game.WATER:  # Water
                        color = self.game.LIGHT_BLUE
                    elif tile_type == self.game.SAND:  # Beach
                        color = self.game.SAND_COLOR
                    elif tile_type == self.game.MOUNTAIN:  # Mountain
                        color = self.game.GRAY
                    
                    pygame.draw.rect(self.game.screen, color, (x * self.game.TILE_SIZE, y * self.game.TILE_SIZE, self.game.TILE_SIZE, self.game.TILE_SIZE))
                    
                    # Add simple visual elements based on tile type
                    if tile_type == self.game.FOREST:
                        # Draw small tree symbol in forest
                        pygame.draw.polygon(self.game.screen, (0, 50, 0), 
                                           [(x * self.game.TILE_SIZE + self.game.TILE_SIZE//2, y * self.game.TILE_SIZE + 5),
                                            (x * self.game.TILE_SIZE + 5, y * self.game.TILE_SIZE + self.game.TILE_SIZE - 5),
                                            (x * self.game.TILE_SIZE + self.game.TILE_SIZE - 5, y * self.game.TILE_SIZE + self.game.TILE_SIZE - 5)])
                    elif tile_type == self.game.MOUNTAIN:
                        # Draw mountain symbol
                        pygame.draw.polygon(self.game.screen, (100, 100, 100), 
                                           [(x * self.game.TILE_SIZE + self.game.TILE_SIZE//2, y * self.game.TILE_SIZE + 5),
                                            (x * self.game.TILE_SIZE + 5, y * self.game.TILE_SIZE + self.game.TILE_SIZE - 5),
                                            (x * self.game.TILE_SIZE + self.game.TILE_SIZE - 5, y * self.game.TILE_SIZE + self.game.TILE_SIZE - 5)])
                    elif tile_type == self.game.WATER:
                        # Draw water ripples
                        pygame.draw.line(self.game.screen, (100, 200, 255), 
                                        (x * self.game.TILE_SIZE + 5, y * self.game.TILE_SIZE + self.game.TILE_SIZE//2),
                                        (x * self.game.TILE_SIZE + self.game.TILE_SIZE - 5, y * self.game.TILE_SIZE + self.game.TILE_SIZE//2), 2)
        
        # Draw the player
        player_screen_x = (self.game.player.x - self.game.camera_x) * self.game.TILE_SIZE
        player_screen_y = (self.game.player.y - self.game.camera_y) * self.game.TILE_SIZE
        pygame.draw.rect(self.game.screen, self.game.BLUE, (player_screen_x, player_screen_y, self.game.TILE_SIZE, self.game.TILE_SIZE))
        
        # Display status
        status_text = f"Lv: {self.game.player.level}  HP: {self.game.player.hp}/{self.game.player.max_hp}  MP: {self.game.player.mp}/{self.game.player.max_mp}  EXP: {self.game.player.exp}/{self.game.player.max_exp}"
        status_surface = self.game.FONT.render(status_text, True, self.game.WHITE)
        self.game.screen.blit(status_surface, (10, 10))
        
        # Draw menu button in top-right corner
        menu_button_rect = pygame.Rect(self.game.SCREEN_WIDTH - 100, 10, 90, 30)
        pygame.draw.rect(self.game.screen, (80, 80, 120), menu_button_rect)
        pygame.draw.rect(self.game.screen, (120, 120, 180), menu_button_rect, 2)
        menu_text = self.game.FONT.render("Menu", True, self.game.WHITE)
        self.game.screen.blit(menu_text, (self.game.SCREEN_WIDTH - 65, 15))
        
        # Draw menu if it's open
        if self.game.show_menu:
            self.game.game_part3.draw_menu()
        
        # Draw status screen if it's open
        if self.game.show_status:
            self.game.game_part3.draw_status_screen()
            
        # Draw enemy stats screen if it's open
        if self.game.game_part3.show_enemy_stats:
            self.game.game_part3.draw_enemy_stats_screen()
        
        # Controls
        controls_text = "Arrow Keys: Move"
        controls_surface = self.game.FONT.render(controls_text, True, self.game.WHITE)
        self.game.screen.blit(controls_surface, (10, self.game.SCREEN_HEIGHT - 30))
