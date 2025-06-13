import pygame
import sys
import math

class GamePart5:
    def __init__(self, game):
        self.game = game
    
    def handle_map_input(self, key):
        # Don't process movement if menu or status screen is open
        if self.game.show_menu or self.game.show_status or self.game.game_part3.show_enemy_stats:
            self.handle_menu_keyboard(key)
            return
            
        moved = False
        if key == pygame.K_UP:
            moved = self.game.player.move(0, -1, self.game.map)
        elif key == pygame.K_DOWN:
            moved = self.game.player.move(0, 1, self.game.map)
        elif key == pygame.K_LEFT:
            moved = self.game.player.move(-1, 0, self.game.map)
        elif key == pygame.K_RIGHT:
            moved = self.game.player.move(1, 0, self.game.map)
        elif key == pygame.K_ESCAPE or key == pygame.K_m:  # ESC or M key toggles menu
            self.game.show_menu = not self.game.show_menu
        elif key == pygame.K_s:  # S key for status screen
            self.game.show_status = True
        elif key == pygame.K_e:  # E key for enemy stats screen
            self.game.game_part3.show_enemy_stats = True
        
        if moved:
            self.game.game_part2.check_enemy_encounter()
    
    def handle_map_mouse(self, pos):
        # Check if menu button was clicked
        menu_button_rect = pygame.Rect(self.game.SCREEN_WIDTH - 100, 10, 90, 30)
        if menu_button_rect.collidepoint(pos):
            self.game.show_menu = not self.game.show_menu
            self.game.show_status = False  # Close status screen if open
            self.game.game_part3.show_enemy_stats = False  # Close enemy stats screen if open
            return
            
        # If enemy stats screen is open, check for close button
        if self.game.game_part3.show_enemy_stats:
            panel_width, panel_height = 450, 400
            panel_x = (self.game.SCREEN_WIDTH - panel_width) // 2
            panel_y = (self.game.SCREEN_HEIGHT - panel_height) // 2
            
            close_button_rect = pygame.Rect(panel_x + 125, panel_y + 340, 200, 40)
            if close_button_rect.collidepoint(pos):
                self.game.game_part3.show_enemy_stats = False
            return
            
        # If status screen is open, check for close button
        if self.game.show_status:
            status_width, status_height = 450, 400  # Match the updated size
            status_x = (self.game.SCREEN_WIDTH - status_width) // 2
            status_y = (self.game.SCREEN_HEIGHT - status_height) // 2
            
            close_button_rect = pygame.Rect(status_x + 125, status_y + 330, 200, 40)
            if close_button_rect.collidepoint(pos):
                self.game.show_status = False
            return
            
        # If menu is open, check for menu button clicks
        if self.game.show_menu:
            menu_width, menu_height = 300, 340  # Updated height for new button
            menu_x = (self.game.SCREEN_WIDTH - menu_width) // 2
            menu_y = (self.game.SCREEN_HEIGHT - menu_height) // 2
            
            # Status button
            status_button_rect = pygame.Rect(menu_x + 50, menu_y + 80, 200, 40)
            if status_button_rect.collidepoint(pos):
                self.game.show_status = True
                self.game.show_menu = False  # Close menu when opening status
                return
                
            # Enemy Stats button
            enemy_stats_button_rect = pygame.Rect(menu_x + 50, menu_y + 140, 200, 40)
            if enemy_stats_button_rect.collidepoint(pos):
                self.game.game_part3.show_enemy_stats = True
                self.game.show_menu = False  # Close menu when opening enemy stats
                return
            
            # Quit button
            quit_button_rect = pygame.Rect(menu_x + 50, menu_y + 200, 200, 40)
            if quit_button_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()
                
            # Close button
            close_button_rect = pygame.Rect(menu_x + 50, menu_y + 260, 200, 40)
            if close_button_rect.collidepoint(pos):
                self.game.show_menu = False
    
    def handle_battle_keyboard(self, key):
        if self.game.battle.turn != 0 or self.game.battle.state != "choosing" or self.game.battle.action_in_progress:
            return
        
        # Attack command - A key
        if key == pygame.K_a:
            self.game.battle.player_attack()
        
        # Strong Attack command - S key
        elif key == pygame.K_s:
            if self.game.player.mp >= 3:  # Check if enough MP
                self.game.battle.player_strong_attack()
            else:
                self.game.battle.message = "Not enough MP for Strong Attack!"
        
        # Run command - R key
        elif key == pygame.K_r:
            self.game.battle.player_run()
    
    def handle_menu_keyboard(self, key):
        # If enemy stats screen is open
        if self.game.game_part3.show_enemy_stats:
            # Close enemy stats screen - Enter or Space
            if key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_ESCAPE:
                self.game.game_part3.show_enemy_stats = False
            return
            
        # If status screen is open
        if self.game.show_status:
            # Close status screen - Enter or Space
            if key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_ESCAPE:
                self.game.show_status = False
            return
            
        # If menu is open
        if self.game.show_menu:
            # Status button - S key
            if key == pygame.K_s:
                self.game.show_status = True
                self.game.show_menu = False  # Close menu when opening status
                return
                
            # Enemy Stats button - E key
            elif key == pygame.K_e:
                self.game.game_part3.show_enemy_stats = True
                self.game.show_menu = False  # Close menu when opening enemy stats
                return
            
            # Quit button - Q key
            elif key == pygame.K_q:
                pygame.quit()
                sys.exit()
                
            # Close button - C key or Escape
            elif key == pygame.K_c or key == pygame.K_ESCAPE:
                self.game.show_menu = False
    
    def handle_battle_input(self, pos):
        if self.game.battle.turn != 0 or self.game.battle.state != "choosing" or self.game.battle.action_in_progress:
            return
        
        # Attack command
        if 20 <= pos[0] <= 130 and 525 <= pos[1] <= 555:
            self.game.battle.player_attack()
        
        # Strong Attack command
        elif 140 <= pos[0] <= 250 and 525 <= pos[1] <= 555:
            if self.game.player.mp >= 3:  # Check if enough MP
                self.game.battle.player_strong_attack()
            else:
                self.game.battle.message = "Not enough MP for Strong Attack!"
        
        # Run command
        elif 260 <= pos[0] <= 370 and 525 <= pos[1] <= 555:
            self.game.battle.player_run()
    
    def update(self):
        if self.game.game_state == "battle":
            self.game.battle.update()
            
            # Check for battle end conditions
            if self.game.battle.state in ["victory", "defeat", "escape"] and not self.game.battle.action_in_progress:
                # If there's a level up popup, wait for it to finish before returning to map
                if hasattr(self.game.battle, 'show_level_up_popup') and self.game.battle.show_level_up_popup:
                    # Don't return to map yet, wait for popup to finish
                    print(f"Level up popup active, timer: {self.game.battle.level_up_popup_timer}")
                    pass
                else:
                    # No level up popup or it has finished, return to map after delay
                    pygame.time.delay(1000)
                    if self.game.battle.state == "defeat":
                        self.game.player.hp = self.game.player.max_hp // 2  # Recover half HP and continue
                    self.game.game_state = "map"
                    print(f"Battle ended with state: {self.game.battle.state}, returning to map")
