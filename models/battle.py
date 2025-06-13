import random

class Battle:
    def __init__(self, player, enemy, screen_width):
        self.player = player
        self.enemy = enemy
        self.turn = 0  # 0: Player's turn, 1: Enemy's turn
        self.message = f"A {self.enemy.name} appeared!"
        self.state = "choosing"  # choosing, fighting, victory, defeat
        self.action_in_progress = False
        self.action_timer = 0
        self.damage_to_show = 0
        self.damage_position = (0, 0)
        self.damage_timer = 0
        self.damage_target = None  # "player" or "enemy"
        self.SCREEN_WIDTH = screen_width
        
        # Level up popup properties
        self.show_level_up_popup = False
        self.level_up_stats = None
        self.level_up_popup_timer = 0
        
        # Determine first attacker based on speed
        if player.speed < enemy.speed:
            self.turn = 1
            self.message += f"\n{self.enemy.name} attacks first!"
    
    def player_attack(self):
        if self.action_in_progress:
            return
            
        self.action_in_progress = True
        self.action_timer = 60  # 1 second at 60 FPS
        damage = max(1, self.player.attack - self.enemy.defense // 2)
        damage = int(damage * random.uniform(0.8, 1.2))  # Damage variation
        self.damage_to_show = damage
        self.damage_position = (self.SCREEN_WIDTH // 2, 150)
        self.damage_timer = 60
        self.damage_target = "enemy"
        self.message = f"Your attack!"
        
    def player_strong_attack(self):
        if self.action_in_progress:
            return
            
        # Check if player has enough MP
        if self.player.mp < 3:
            self.message = "Not enough MP for Strong Attack!"
            return
            
        self.player.mp -= 3  # Consume MP
        self.action_in_progress = True
        self.action_timer = 60  # 1 second at 60 FPS
        
        # Strong attack does 1.8x normal damage
        damage = max(1, int(self.player.attack * 1.8) - self.enemy.defense // 2)
        damage = int(damage * random.uniform(0.9, 1.3))  # Damage variation
        self.damage_to_show = damage
        self.damage_position = (self.SCREEN_WIDTH // 2, 150)
        self.damage_timer = 60
        self.damage_target = "enemy"
        self.message = f"Your strong attack!"
        
    def complete_player_attack(self):
        damage = self.damage_to_show
        self.enemy.hp -= damage
        
        if self.message == "Your attack!":
            self.message = f"You dealt {damage} damage to {self.enemy.name}!"
        else:  # Strong attack
            self.message = f"Strong attack! {damage} damage to {self.enemy.name}!"
        
        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            self.state = "victory"
            
            # Calculate level difference bonus for display
            level_diff = self.enemy.level - self.player.level
            bonus_text = ""
            if level_diff > 0:
                bonus_text = f" (+50% level bonus)"
            elif level_diff == 0:
                bonus_text = f" (+20% level bonus)"
            elif level_diff == -1:
                bonus_text = f" (+10% level bonus)"
                
            # Track defeated enemy
            self.player.defeated_enemies[self.enemy.name] += 1
            self.player.defeated_enemies["total"] += 1
                
            self.message += f"\nDefeated the {self.enemy.name} (Lv.{self.enemy.level})! Gained {self.enemy.exp} EXP{bonus_text}!"
            leveled, stat_changes = self.player.gain_exp(self.enemy.exp)
            if leveled:
                self.message += f"\nLevel up! You are now level {self.player.level}!"
                self.level_up_stats = stat_changes  # Store the stat changes for the popup
                self.show_level_up_popup = True
                self.level_up_popup_timer = 0  # Reset timer to trigger popup
                print("Level up detected! Showing popup.")  # Debug message
            else:
                self.show_level_up_popup = False
        else:
            self.turn = 1  # Enemy's turn
            self.message += f"\n{self.enemy.name}'s turn."
        
        self.action_in_progress = False
    
    def enemy_attack(self):
        if self.action_in_progress:
            return
            
        self.action_in_progress = True
        self.action_timer = 60  # 1 second at 60 FPS
        damage = max(1, self.enemy.attack - self.player.defense // 2)
        damage = int(damage * random.uniform(0.8, 1.2))  # Damage variation
        self.damage_to_show = damage
        self.damage_position = (self.SCREEN_WIDTH // 2, 330)
        self.damage_timer = 60
        self.damage_target = "player"
        self.message = f"{self.enemy.name} attacks!"
    
    def complete_enemy_attack(self):
        damage = self.damage_to_show
        self.player.hp -= damage
        self.message = f"{self.enemy.name} dealt {damage} damage to you!"
        
        if self.player.hp <= 0:
            self.player.hp = 0
            self.state = "defeat"
            self.message += "\nYou were defeated..."
        else:
            self.turn = 0  # Player's turn
            self.message += "\nYour turn."
        
        self.action_in_progress = False
    
    def player_run(self):
        if self.action_in_progress:
            return
            
        self.action_in_progress = True
        self.action_timer = 60  # 1 second at 60 FPS
        self.message = "Attempting to escape..."
    
    def complete_player_run(self):
        # Escape chance depends on speed
        escape_chance = 0.3 + (self.player.speed - self.enemy.speed) * 0.05
        escape_chance = max(0.1, min(0.9, escape_chance))  # Limited to 10%~90% range
        
        if random.random() < escape_chance:
            self.state = "escape"
            self.message = "Successfully escaped!"
            print("Escape successful!")  # Debug message
        else:
            self.message = "Couldn't escape!"
            self.turn = 1  # Enemy's turn
            self.message += f"\n{self.enemy.name}'s turn."
        
        self.action_in_progress = False
    
    def update(self):
        # Update timers and handle action completion
        if self.action_in_progress:
            self.action_timer -= 1
            if self.action_timer <= 0:
                if self.turn == 0 and self.state == "choosing":
                    # Player's action completion
                    if self.message == "Your attack!" or self.message == "Your strong attack!":
                        self.complete_player_attack()
                    elif self.message == "Attempting to escape...":
                        self.complete_player_run()
                elif self.turn == 1:
                    # Enemy's action completion
                    self.complete_enemy_attack()
        
        # Update damage display timer
        if self.damage_timer > 0:
            self.damage_timer -= 1
        
        # Handle level up popup
        if self.show_level_up_popup:
            if self.level_up_popup_timer <= 0:
                # Initialize the timer when popup is first shown
                self.level_up_popup_timer = 180  # Show for 3 seconds (60 fps * 3)
            else:
                # Count down the timer
                self.level_up_popup_timer -= 1
                if self.level_up_popup_timer <= 0:
                    self.show_level_up_popup = False
        
        # Auto-trigger enemy attack if it's enemy's turn
        if self.turn == 1 and not self.action_in_progress and self.state == "choosing":
            self.enemy_attack()
