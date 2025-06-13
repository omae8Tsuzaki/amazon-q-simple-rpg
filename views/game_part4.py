import pygame
import sys
import random
import math

class GamePart4:
    def __init__(self, game):
        self.game = game
        
    def draw_battle(self):
        # Draw battle background
        self.game.screen.blit(self.game.battle_background, (0, 0))
        
        # Battle interface background
        pygame.draw.rect(self.game.screen, (30, 30, 50), (0, 380, self.game.SCREEN_WIDTH, 220))
        pygame.draw.rect(self.game.screen, (50, 50, 70), (10, 390, self.game.SCREEN_WIDTH - 20, 200), 2)
        
        # Draw enemy platform
        pygame.draw.ellipse(self.game.screen, (80, 80, 100), (self.game.SCREEN_WIDTH // 2 - 80, 200, 160, 40))
        
        # Draw enemy based on type
        enemy_color = self.game.RED
        if self.game.battle.damage_target == "enemy" and self.game.battle.damage_timer > 30:
            # Flash enemy when hit
            enemy_color = self.game.WHITE if (self.game.battle.damage_timer // 5) % 2 == 0 else self.game.RED
        
        # Draw different enemy types
        enemy_x = self.game.SCREEN_WIDTH // 2 - 50
        enemy_y = 100
        
        if self.game.battle.enemy.name == "Slime":
            # Draw slime (blue blob with eyes)
            pygame.draw.ellipse(self.game.screen, (0, 100, 200) if enemy_color != self.game.WHITE else self.game.WHITE, 
                              (enemy_x, enemy_y + 50, 100, 50))  # Body
            pygame.draw.ellipse(self.game.screen, (0, 80, 180) if enemy_color != self.game.WHITE else self.game.WHITE, 
                              (enemy_x + 10, enemy_y + 30, 80, 60))  # Top
            # Eyes
            pygame.draw.circle(self.game.screen, self.game.WHITE, (enemy_x + 30, enemy_y + 50), 10)
            pygame.draw.circle(self.game.screen, self.game.WHITE, (enemy_x + 70, enemy_y + 50), 10)
            pygame.draw.circle(self.game.screen, self.game.BLACK, (enemy_x + 30, enemy_y + 50), 5)
            pygame.draw.circle(self.game.screen, self.game.BLACK, (enemy_x + 70, enemy_y + 50), 5)
            
        elif self.game.battle.enemy.name == "Goblin":
            # Draw goblin (green humanoid)
            pygame.draw.rect(self.game.screen, (0, 150, 0) if enemy_color != self.game.WHITE else self.game.WHITE, 
                           (enemy_x + 25, enemy_y + 20, 50, 60))  # Body
            pygame.draw.circle(self.game.screen, (0, 150, 0) if enemy_color != self.game.WHITE else self.game.WHITE, 
                             (enemy_x + 50, enemy_y + 20), 25)  # Head
            # Eyes
            pygame.draw.circle(self.game.screen, self.game.RED, (enemy_x + 40, enemy_y + 15), 5)
            pygame.draw.circle(self.game.screen, self.game.RED, (enemy_x + 60, enemy_y + 15), 5)
            # Arms
            pygame.draw.rect(self.game.screen, (0, 150, 0) if enemy_color != self.game.WHITE else self.game.WHITE, 
                           (enemy_x + 10, enemy_y + 40, 15, 30))
            pygame.draw.rect(self.game.screen, (0, 150, 0) if enemy_color != self.game.WHITE else self.game.WHITE, 
                           (enemy_x + 75, enemy_y + 40, 15, 30))
            
        elif self.game.battle.enemy.name == "Bat":
            # Draw bat (black with wings)
            pygame.draw.circle(self.game.screen, (50, 50, 50) if enemy_color != self.game.WHITE else self.game.WHITE, 
                             (enemy_x + 50, enemy_y + 50), 20)  # Body
            # Wings
            pygame.draw.arc(self.game.screen, (50, 50, 50) if enemy_color != self.game.WHITE else self.game.WHITE, 
                          (enemy_x, enemy_y + 20, 50, 60), 0, 3.14, 5)
            pygame.draw.arc(self.game.screen, (50, 50, 50) if enemy_color != self.game.WHITE else self.game.WHITE, 
                          (enemy_x + 50, enemy_y + 20, 50, 60), 0, 3.14, 5)
            # Eyes
            pygame.draw.circle(self.game.screen, self.game.RED, (enemy_x + 40, enemy_y + 45), 5)
            pygame.draw.circle(self.game.screen, self.game.RED, (enemy_x + 60, enemy_y + 45), 5)
            
        elif self.game.battle.enemy.name == "Zombie":
            # Draw zombie (gray-green humanoid)
            pygame.draw.rect(self.game.screen, (100, 150, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                           (enemy_x + 25, enemy_y + 20, 50, 70))  # Body
            pygame.draw.circle(self.game.screen, (100, 150, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                             (enemy_x + 50, enemy_y + 20), 25)  # Head
            # Arms (one raised)
            pygame.draw.rect(self.game.screen, (100, 150, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                           (enemy_x + 10, enemy_y + 30, 15, 40))
            pygame.draw.rect(self.game.screen, (100, 150, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                           (enemy_x + 75, enemy_y + 40, 15, 30))
            # Eyes
            pygame.draw.circle(self.game.screen, (255, 255, 0), (enemy_x + 40, enemy_y + 15), 5)
            pygame.draw.circle(self.game.screen, (255, 255, 0), (enemy_x + 60, enemy_y + 15), 5)
            
        elif self.game.battle.enemy.name == "Wolf":
            # Draw wolf (gray with pointed ears)
            pygame.draw.ellipse(self.game.screen, (100, 100, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                              (enemy_x + 10, enemy_y + 40, 80, 40))  # Body
            pygame.draw.circle(self.game.screen, (100, 100, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                             (enemy_x + 80, enemy_y + 40), 20)  # Head
            # Ears
            pygame.draw.polygon(self.game.screen, (100, 100, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                              [(enemy_x + 70, enemy_y + 25), (enemy_x + 80, enemy_y + 10), (enemy_x + 90, enemy_y + 25)])
            pygame.draw.polygon(self.game.screen, (100, 100, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                              [(enemy_x + 90, enemy_y + 25), (enemy_x + 100, enemy_y + 10), (enemy_x + 110, enemy_y + 25)])
            # Eyes
            pygame.draw.circle(self.game.screen, self.game.YELLOW, (enemy_x + 90, enemy_y + 35), 5)
            # Tail
            pygame.draw.ellipse(self.game.screen, (100, 100, 100) if enemy_color != self.game.WHITE else self.game.WHITE, 
                              (enemy_x, enemy_y + 50, 20, 10))
        else:
            # Default enemy shape if type not recognized
            pygame.draw.rect(self.game.screen, enemy_color, (enemy_x, enemy_y, 100, 100))
        
        # Enemy name
        enemy_name_surface = self.game.FONT.render(f"{self.game.battle.enemy.name} Lv.{self.game.battle.enemy.level}", True, self.game.WHITE)
        self.game.screen.blit(enemy_name_surface, (self.game.SCREEN_WIDTH // 2 - enemy_name_surface.get_width() // 2, 70))
        
        # HP bar (enemy)
        hp_ratio = self.game.battle.enemy.hp / self.game.battle.enemy.max_hp
        pygame.draw.rect(self.game.screen, self.game.WHITE, (self.game.SCREEN_WIDTH // 2 - 75, 220, 150, 20), 1)
        pygame.draw.rect(self.game.screen, self.game.RED, (self.game.SCREEN_WIDTH // 2 - 75, 220, int(150 * hp_ratio), 20))
        
        enemy_status = f"HP:{self.game.battle.enemy.hp}/{self.game.battle.enemy.max_hp}"
        enemy_status_surface = self.game.FONT.render(enemy_status, True, self.game.WHITE)
        self.game.screen.blit(enemy_status_surface, (self.game.SCREEN_WIDTH // 2 - enemy_status_surface.get_width() // 2, 250))
        
        # Draw player platform
        pygame.draw.ellipse(self.game.screen, (80, 80, 100), (self.game.SCREEN_WIDTH // 2 - 60, 350, 120, 30))
        
        # Player character (simple representation)
        player_color = self.game.BLUE
        if self.game.battle.damage_target == "player" and self.game.battle.damage_timer > 30:
            # Flash player when hit
            player_color = self.game.WHITE if (self.game.battle.damage_timer // 5) % 2 == 0 else self.game.BLUE
            
        pygame.draw.rect(self.game.screen, player_color, (self.game.SCREEN_WIDTH // 2 - 15, 300, 30, 50))
        
        # Player status
        player_status = f"You Lv.{self.game.player.level} HP:{self.game.player.hp}/{self.game.player.max_hp} MP:{self.game.player.mp}/{self.game.player.max_mp}"
        player_status_surface = self.game.FONT.render(player_status, True, self.game.WHITE)
        self.game.screen.blit(player_status_surface, (20, 410))
        
        # HP bar (player)
        hp_ratio = self.game.player.hp / self.game.player.max_hp
        pygame.draw.rect(self.game.screen, self.game.WHITE, (20, 440, 150, 15), 1)
        pygame.draw.rect(self.game.screen, self.game.GREEN, (20, 440, int(150 * hp_ratio), 15))
        
        # MP bar (player)
        mp_ratio = self.game.player.mp / self.game.player.max_mp
        pygame.draw.rect(self.game.screen, self.game.WHITE, (180, 440, 150, 15), 1)
        pygame.draw.rect(self.game.screen, (50, 50, 255), (180, 440, int(150 * mp_ratio), 15))
        
        # Display damage numbers if active
        if self.game.battle.damage_timer > 0:
            damage_text = str(self.game.battle.damage_to_show)
            damage_surface = pygame.font.Font(None, 36).render(damage_text, True, (255, 255, 100))
            offset_y = 10 * math.sin(self.game.battle.damage_timer / 10)  # Make damage number float up
            self.game.screen.blit(damage_surface, 
                       (self.game.battle.damage_position[0] - damage_surface.get_width() // 2, 
                        self.game.battle.damage_position[1] - damage_surface.get_height() // 2 - offset_y))
        
        # Display turn indicator
        if self.game.battle.state == "choosing":
            if self.game.battle.turn == 0:
                turn_text = "YOUR TURN"
                turn_color = self.game.BLUE
            else:
                turn_text = f"{self.game.battle.enemy.name}'S TURN"
                turn_color = self.game.RED
                
            turn_surface = pygame.font.Font(None, 28).render(turn_text, True, turn_color)
            self.game.screen.blit(turn_surface, (self.game.SCREEN_WIDTH - turn_surface.get_width() - 20, 410))
        
        # Display messages
        message_lines = self.game.battle.message.split('\n')
        for i, line in enumerate(message_lines):
            message_surface = self.game.FONT.render(line, True, self.game.WHITE)
            self.game.screen.blit(message_surface, (20, 470 + i * 30))
        
        # Display commands (if player's turn and not in middle of action)
        if self.game.battle.turn == 0 and self.game.battle.state == "choosing" and not self.game.battle.action_in_progress:
            commands = ["Attack (A)", "Strong Atk (S)", "Run (R)"]
            for i, cmd in enumerate(commands):
                cmd_color = self.game.YELLOW
                # Gray out Strong Attack if not enough MP
                if cmd == "Strong Atk (S)" and self.game.player.mp < 3:
                    cmd_color = (100, 100, 100)  # Gray color
                    
                cmd_surface = self.game.FONT.render(cmd, True, cmd_color)
                pygame.draw.rect(self.game.screen, (60, 60, 80), (20 + i * 120, 530 - 5, 110, 30))
                pygame.draw.rect(self.game.screen, (100, 100, 120), (20 + i * 120, 530 - 5, 110, 30), 2)
                self.game.screen.blit(cmd_surface, (25 + i * 120, 530))
                
                # Show MP cost for Strong Attack
                if cmd == "Strong Atk (S)":
                    mp_text = "(3 MP)"
                    mp_surface = pygame.font.Font(None, 18).render(mp_text, True, (100, 100, 255))
                    self.game.screen.blit(mp_surface, (25 + i * 120, 550))
        
        # Draw level up popup if active
        if hasattr(self.game.battle, 'show_level_up_popup') and self.game.battle.show_level_up_popup and self.game.battle.level_up_stats:
            self.draw_level_up_popup()
            
    def draw_level_up_popup(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha
        self.game.screen.blit(overlay, (0, 0))
        
        # Popup panel
        popup_width, popup_height = 400, 350
        popup_x = (self.game.SCREEN_WIDTH - popup_width) // 2
        popup_y = (self.game.SCREEN_HEIGHT - popup_height) // 2
        
        # Draw panel background with golden border for level up
        pygame.draw.rect(self.game.screen, (50, 50, 80), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.game.screen, (255, 215, 0), (popup_x, popup_y, popup_width, popup_height), 4)  # Golden border
        
        # Level up title with animation effect
        pulse = math.sin(pygame.time.get_ticks() / 200) * 10 + 40  # Pulsing effect
        title_font = pygame.font.Font(None, int(36 + pulse/10))
        title_text = title_font.render(f"LEVEL UP! → {self.game.battle.level_up_stats['level']}", True, (255, 255, 0))
        self.game.screen.blit(title_text, (popup_x + (popup_width - title_text.get_width()) // 2, popup_y + 30))
        
        # Stats changes
        font = pygame.font.Font(None, 28)
        y_offset = 90
        
        # Draw stat changes with arrows and colors
        stats = [
            ("HP", "hp", self.game.GREEN),
            ("MP", "mp", (50, 50, 255)),
            ("Attack", "attack", (255, 100, 100)),
            ("Defense", "defense", (100, 100, 255)),
            ("Speed", "speed", (255, 255, 100))
        ]
        
        for label, key, color in stats:
            stat = self.game.battle.level_up_stats[key]
            
            # Stat name
            stat_text = font.render(f"{label}:", True, self.game.WHITE)
            self.game.screen.blit(stat_text, (popup_x + 50, popup_y + y_offset))
            
            # Old value → new value
            change_text = font.render(f"{stat['old']} → {stat['new']}", True, color)
            self.game.screen.blit(change_text, (popup_x + 150, popup_y + y_offset))
            
            # Increase amount with + sign
            increase_text = font.render(f"+{stat['increase']}", True, (0, 255, 0))
            self.game.screen.blit(increase_text, (popup_x + 300, popup_y + y_offset))
            
            y_offset += 40
        
        # Congratulatory message
        message = "All stats increased! HP and MP fully restored!"
        message_text = font.render(message, True, self.game.WHITE)
        self.game.screen.blit(message_text, (popup_x + (popup_width - message_text.get_width()) // 2, popup_y + 290))
        
        # Timer bar showing how long the popup will stay
        timer_width = int((self.game.battle.level_up_popup_timer / 180) * (popup_width - 40))
        pygame.draw.rect(self.game.screen, (100, 100, 100), (popup_x + 20, popup_y + popup_height - 20, popup_width - 40, 10))
        pygame.draw.rect(self.game.screen, (255, 215, 0), (popup_x + 20, popup_y + popup_height - 20, timer_width, 10))
