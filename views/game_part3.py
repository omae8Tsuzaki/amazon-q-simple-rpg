import pygame
import sys
import math

class GamePart3:
    def __init__(self, game):
        self.game = game
        
    def draw_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        self.game.screen.blit(overlay, (0, 0))
        
        # Menu panel
        menu_width, menu_height = 300, 280  # Increased height for new button
        menu_x = (self.game.SCREEN_WIDTH - menu_width) // 2
        menu_y = (self.game.SCREEN_HEIGHT - menu_height) // 2
        
        pygame.draw.rect(self.game.screen, (50, 50, 80), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(self.game.screen, (100, 100, 150), (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Menu title
        title_text = pygame.font.Font(None, 36).render("Menu", True, self.game.WHITE)
        self.game.screen.blit(title_text, (menu_x + (menu_width - title_text.get_width()) // 2, menu_y + 20))
        
        # Status button
        status_button_rect = pygame.Rect(menu_x + 50, menu_y + 80, 200, 40)
        pygame.draw.rect(self.game.screen, (50, 100, 150), status_button_rect)
        pygame.draw.rect(self.game.screen, (100, 150, 200), status_button_rect, 2)
        status_text = pygame.font.Font(None, 28).render("View Status (S)", True, self.game.WHITE)
        self.game.screen.blit(status_text, (menu_x + (menu_width - status_text.get_width()) // 2, menu_y + 90))
        
        # Quit button
        quit_button_rect = pygame.Rect(menu_x + 50, menu_y + 140, 200, 40)
        pygame.draw.rect(self.game.screen, (150, 50, 50), quit_button_rect)
        pygame.draw.rect(self.game.screen, (200, 100, 100), quit_button_rect, 2)
        quit_text = pygame.font.Font(None, 28).render("Quit Game (Q)", True, self.game.WHITE)
        self.game.screen.blit(quit_text, (menu_x + (menu_width - quit_text.get_width()) // 2, menu_y + 150))
        
        # Close button
        close_button_rect = pygame.Rect(menu_x + 50, menu_y + 200, 200, 40)
        pygame.draw.rect(self.game.screen, (80, 80, 120), close_button_rect)
        pygame.draw.rect(self.game.screen, (120, 120, 180), close_button_rect, 2)
        close_text = pygame.font.Font(None, 28).render("Close Menu (ESC/C)", True, self.game.WHITE)
        self.game.screen.blit(close_text, (menu_x + (menu_width - close_text.get_width()) // 2, menu_y + 210))
    
    def draw_status_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        self.game.screen.blit(overlay, (0, 0))
        
        # Status panel
        status_width, status_height = 450, 400  # Increased size to prevent text overlap
        status_x = (self.game.SCREEN_WIDTH - status_width) // 2
        status_y = (self.game.SCREEN_HEIGHT - status_height) // 2
        
        pygame.draw.rect(self.game.screen, (50, 50, 80), (status_x, status_y, status_width, status_height))
        pygame.draw.rect(self.game.screen, (100, 100, 150), (status_x, status_y, status_width, status_height), 3)
        
        # Status title
        title_text = pygame.font.Font(None, 36).render("Character Status", True, self.game.WHITE)
        self.game.screen.blit(title_text, (status_x + (status_width - title_text.get_width()) // 2, status_y + 20))
        
        # Player icon
        pygame.draw.rect(self.game.screen, self.game.BLUE, (status_x + 50, status_y + 70, 40, 60))
        
        # Basic stats
        font = pygame.font.Font(None, 28)
        
        # Left column stats
        left_stats = [
            f"Level: {self.game.player.level}",
            f"Attack: {self.game.player.attack}",
            f"Defense: {self.game.player.defense}",
            f"Speed: {self.game.player.speed}",
        ]
        
        # Draw left column stats
        for i, stat in enumerate(left_stats):
            stat_text = font.render(stat, True, self.game.WHITE)
            self.game.screen.blit(stat_text, (status_x + 50, status_y + 150 + i * 30))
        
        # HP section
        hp_text = font.render(f"HP: {self.game.player.hp}/{self.game.player.max_hp}", True, self.game.WHITE)
        self.game.screen.blit(hp_text, (status_x + 230, status_y + 70))
        
        # HP bar
        hp_ratio = self.game.player.hp / self.game.player.max_hp
        pygame.draw.rect(self.game.screen, self.game.WHITE, (status_x + 230, status_y + 100, 180, 15), 1)
        pygame.draw.rect(self.game.screen, self.game.GREEN, (status_x + 230, status_y + 100, int(180 * hp_ratio), 15))
        
        # MP section
        mp_text = font.render(f"MP: {self.game.player.mp}/{self.game.player.max_mp}", True, self.game.WHITE)
        self.game.screen.blit(mp_text, (status_x + 230, status_y + 130))
        
        # MP bar
        mp_ratio = self.game.player.mp / self.game.player.max_mp
        pygame.draw.rect(self.game.screen, self.game.WHITE, (status_x + 230, status_y + 160, 180, 15), 1)
        pygame.draw.rect(self.game.screen, (50, 50, 255), (status_x + 230, status_y + 160, int(180 * mp_ratio), 15))
        
        # EXP section
        exp_text = font.render(f"EXP: {self.game.player.exp}/{self.game.player.max_exp}", True, self.game.WHITE)
        self.game.screen.blit(exp_text, (status_x + 230, status_y + 190))
        
        # EXP bar
        exp_ratio = self.game.player.exp / self.game.player.max_exp
        pygame.draw.rect(self.game.screen, self.game.WHITE, (status_x + 230, status_y + 220, 180, 15), 1)
        pygame.draw.rect(self.game.screen, self.game.YELLOW, (status_x + 230, status_y + 220, int(180 * exp_ratio), 15))
        
        # Additional stats
        steps_text = font.render(f"Steps: {self.game.player.steps}", True, self.game.WHITE)
        self.game.screen.blit(steps_text, (status_x + 50, status_y + 280))
        
        # Next level info
        next_level_text = font.render(f"Next Level: {self.game.player.level + 1}", True, self.game.WHITE)
        self.game.screen.blit(next_level_text, (status_x + 230, status_y + 250))
        
        # EXP needed
        exp_needed = self.game.player.max_exp - self.game.player.exp
        exp_needed_text = font.render(f"EXP needed: {exp_needed}", True, self.game.WHITE)
        self.game.screen.blit(exp_needed_text, (status_x + 230, status_y + 280))
        
        # Close button
        close_button_rect = pygame.Rect(status_x + 125, status_y + 330, 200, 40)
        pygame.draw.rect(self.game.screen, (80, 80, 120), close_button_rect)
        pygame.draw.rect(self.game.screen, (120, 120, 180), close_button_rect, 2)
        close_text = pygame.font.Font(None, 28).render("Close (Enter/Space)", True, self.game.WHITE)
        self.game.screen.blit(close_text, (status_x + (status_width - close_text.get_width()) // 2, status_y + 340))
