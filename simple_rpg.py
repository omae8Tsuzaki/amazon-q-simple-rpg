import pygame
import random
import sys
import math
from models import Player, Enemy, Battle
from controllers import Game, GamePart5
from views import GamePart2, GamePart3, GamePart4

# Initialize
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
MAP_WIDTH = 50  # Changed map size to 50x50
MAP_HEIGHT = 50  # Changed map size to 50x50

# Font settings
FONT = pygame.font.Font(None, 24)

# Game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dragon Quest Style RPG")

# Experience table (required exp for each level)
def calculate_exp_for_level(level):
    # Experience curve proportional to level cubed, reduced by 20% for level 2+
    base_exp = 100 * (level ** 3) / 3
    if level >= 2:
        base_exp = base_exp * 0.8  # 20% reduction for level 2 and above
    return int(base_exp)

EXP_TABLE = [calculate_exp_for_level(level) for level in range(101)]

def main():
    # Create the main game object
    game = Game(screen, FONT, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, EXP_TABLE)
    
    # Create the game part objects
    game.game_part2 = GamePart2(game)
    game.game_part3 = GamePart3(game)
    game.game_part4 = GamePart4(game)
    game.game_part5 = GamePart5(game)
    
    clock = pygame.time.Clock()
    running = True
    
    # Display keyboard controls at startup
    print("Keyboard Controls:")
    print("- Arrow Keys: Move character")
    print("- M or ESC: Open/close menu")
    print("- S: Open status screen")
    print("- In Menu:")
    print("  - S: View status")
    print("  - Q: Quit game")
    print("  - C or ESC: Close menu")
    print("- In Battle:")
    print("  - A: Attack")
    print("  - S: Strong attack (costs 3 MP)")
    print("  - R: Run away")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game.game_state == "map":
                if event.type == pygame.KEYDOWN:
                    game.game_part5.handle_map_input(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game.game_part5.handle_map_mouse(event.pos)
            elif game.game_state == "battle":
                if event.type == pygame.KEYDOWN:
                    game.game_part5.handle_battle_keyboard(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game.game_part5.handle_battle_input(event.pos)
        
        # Update game logic
        game.game_part5.update()
        
        # Draw everything
        screen.fill((0, 0, 0))  # BLACK
        
        if game.game_state == "map":
            game.game_part2.draw_map()
        elif game.game_state == "battle":
            game.game_part4.draw_battle()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
