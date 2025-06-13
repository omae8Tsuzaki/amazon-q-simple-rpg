import pygame
import random
import math
from models.player import Player
from models.enemy import Enemy
from models.battle import Battle

class Game:
    def __init__(self, screen, font, screen_width, screen_height, tile_size, map_width, map_height, exp_table):
        self.screen = screen
        self.FONT = font
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.TILE_SIZE = tile_size
        self.MAP_WIDTH = map_width
        self.MAP_HEIGHT = map_height
        self.VISIBLE_TILES_X = screen_width // tile_size
        self.VISIBLE_TILES_Y = screen_height // tile_size
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.BROWN = (139, 69, 19)
        self.YELLOW = (255, 255, 0)
        self.LIGHT_BLUE = (173, 216, 230)
        self.SAND_COLOR = (194, 178, 128)
        self.DARK_GREEN = (0, 100, 0)
        self.GRAY = (128, 128, 128)
        
        # Tile types
        self.GRASS = 0
        self.WALL = 1
        self.FOREST = 2
        self.WATER = 3
        self.SAND = 4
        self.MOUNTAIN = 5
        
        self.player = Player(exp_table, map_width, map_height)
        self.map = self.generate_map()
        self.camera_x = 0
        self.camera_y = 0
        self.battle = None
        self.game_state = "map"  # map, battle, menu
        self.battle_background = self.generate_battle_background()
        self.show_menu = False  # Flag to show/hide menu
        self.show_status = False  # Flag to show/hide status screen
        
    def generate_battle_background(self):
        # Create a simple battle background with grass and sky
        bg = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Sky gradient
        for y in range(self.SCREEN_HEIGHT // 2):
            color_value = 100 + (y * 100 // (self.SCREEN_HEIGHT // 2))
            color = (50, 50, min(color_value, 150))
            pygame.draw.line(bg, color, (0, y), (self.SCREEN_WIDTH, y))
        
        # Ground
        pygame.draw.rect(bg, (100, 120, 80), (0, self.SCREEN_HEIGHT // 2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT // 2))
        
        # Add some random grass tufts
        for _ in range(50):
            x = random.randint(0, self.SCREEN_WIDTH)
            y = random.randint(self.SCREEN_HEIGHT // 2, self.SCREEN_HEIGHT)
            height = random.randint(5, 15)
            width = random.randint(2, 6)
            pygame.draw.rect(bg, (50, 150, 50), (x, y - height, width, height))
        
        return bg
        
    def generate_map(self):
        # Improved map generation
        game_map = [[self.GRASS for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        
        # Surround the map with mountains
        for x in range(self.MAP_WIDTH):
            game_map[0][x] = self.MOUNTAIN
            game_map[self.MAP_HEIGHT-1][x] = self.MOUNTAIN
        for y in range(self.MAP_HEIGHT):
            game_map[y][0] = self.MOUNTAIN
            game_map[y][self.MAP_WIDTH-1] = self.MOUNTAIN
        
        # Generate a river (random winding river)
        river_start_x = random.randint(5, self.MAP_WIDTH - 5)
        x, y = river_start_x, 0
        while y < self.MAP_HEIGHT:
            if 0 < x < self.MAP_WIDTH - 1 and 0 < y < self.MAP_HEIGHT - 1:
                game_map[y][x] = self.WATER
                # Place beach around the river
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 < nx < self.MAP_WIDTH - 1 and 0 < ny < self.MAP_HEIGHT - 1:
                            if game_map[ny][nx] == self.GRASS:
                                game_map[ny][nx] = self.SAND
            
            # Determine river flow
            direction = random.choice(["down", "left", "right"])
            if direction == "down":
                y += 1
            elif direction == "left" and x > 2:
                x -= 1
            elif direction == "right" and x < self.MAP_WIDTH - 3:
                x += 1
            else:
                y += 1
        
        # Generate forests (clustering)
        forest_clusters = 5
        for _ in range(forest_clusters):
            center_x = random.randint(5, self.MAP_WIDTH - 5)
            center_y = random.randint(5, self.MAP_HEIGHT - 5)
            cluster_size = random.randint(10, 20)
            
            for _ in range(cluster_size):
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-3, 3)
                forest_x = center_x + offset_x
                forest_y = center_y + offset_y
                
                if (0 < forest_x < self.MAP_WIDTH - 1 and 0 < forest_y < self.MAP_HEIGHT - 1 and
                    game_map[forest_y][forest_x] == self.GRASS):
                    game_map[forest_y][forest_x] = self.FOREST
        
        # Place walls (rocks) randomly
        for _ in range(30):
            wall_x = random.randint(5, self.MAP_WIDTH - 5)
            wall_y = random.randint(5, self.MAP_HEIGHT - 5)
            
            if game_map[wall_y][wall_x] == self.GRASS:
                game_map[wall_y][wall_x] = self.WALL
                
                # Create rock clusters
                for _ in range(random.randint(3, 8)):
                    dx = random.randint(-2, 2)
                    dy = random.randint(-2, 2)
                    nx, ny = wall_x + dx, wall_y + dy
                    if (0 < nx < self.MAP_WIDTH - 1 and 0 < ny < self.MAP_HEIGHT - 1 and
                        game_map[ny][nx] == self.GRASS):
                        game_map[ny][nx] = self.WALL
        
        # Add mountains
        for _ in range(3):
            mountain_x = random.randint(5, self.MAP_WIDTH - 5)
            mountain_y = random.randint(5, self.MAP_HEIGHT - 5)
            
            # Create mountain shape
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if dx*dx + dy*dy <= 9:  # Circular mountain
                        nx, ny = mountain_x + dx, mountain_y + dy
                        if (0 < nx < self.MAP_WIDTH - 1 and 0 < ny < self.MAP_HEIGHT - 1):
                            game_map[ny][nx] = self.MOUNTAIN
        
        # Ensure player's starting position is on a passable tile
        while game_map[self.player.y][self.player.x] in [self.WALL, self.MOUNTAIN, self.WATER]:
            self.player.x = random.randint(5, self.MAP_WIDTH - 5)
            self.player.y = random.randint(5, self.MAP_HEIGHT - 5)
        
        return game_map
