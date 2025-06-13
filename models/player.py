import random

class Player:
    def __init__(self, EXP_TABLE, MAP_WIDTH, MAP_HEIGHT):
        self.x = 25  # X coordinate on map (center area)
        self.y = 25  # Y coordinate on map (center area)
        self.level = 1
        self.exp = 0
        self.max_exp = EXP_TABLE[1]
        self.hp = 30  # Increased starting HP by 10 (from 20 to 30)
        self.max_hp = 30  # Increased starting max HP by 10 (from 20 to 30)
        self.mp = 10  # Magic Points for special attacks
        self.max_mp = 10
        self.attack = 5
        self.defense = 3
        self.speed = 3
        self.steps = 0  # Step counter (used for enemy encounter check)
        self.MAP_WIDTH = MAP_WIDTH
        self.MAP_HEIGHT = MAP_HEIGHT
        self.EXP_TABLE = EXP_TABLE
        
        # Enemy defeat tracking
        self.defeated_enemies = {
            "Slime": 0,
            "Goblin": 0,
            "Bat": 0,
            "Zombie": 0,
            "Wolf": 0,
            "total": 0
        }
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Wall, mountain, water are impassable (values 1, 5, 3)
        impassable = [1, 5, 3]
        
        # Check if within map bounds and tile is passable
        if (0 <= new_x < self.MAP_WIDTH and 0 <= new_y < self.MAP_HEIGHT and 
            game_map[new_y][new_x] not in impassable):
            self.x = new_x
            self.y = new_y
            self.steps += 1
            return True
        return False
    
    def level_up(self):
        if self.level >= 100:  # Max level
            return False
            
        if self.exp >= self.max_exp:
            self.level += 1
            self.exp -= self.max_exp
            self.max_exp = self.EXP_TABLE[self.level] - self.EXP_TABLE[self.level - 1]
            
            # Stat increases
            hp_increase = random.randint(3, 8)
            mp_increase = random.randint(2, 5)  # MP increase on level up
            attack_increase = random.randint(1, 3)
            defense_increase = random.randint(1, 2)
            speed_increase = random.randint(0, 1)
            
            # Store old stats for level up display
            old_max_hp = self.max_hp
            old_max_mp = self.max_mp
            old_attack = self.attack
            old_defense = self.defense
            old_speed = self.speed
            
            # Apply increases
            self.max_hp += hp_increase
            self.max_mp += mp_increase
            self.hp = self.max_hp  # Full HP recovery on level up
            self.mp = self.max_mp  # Full MP recovery on level up
            self.attack += attack_increase
            self.defense += defense_increase
            self.speed += speed_increase
            
            # Create a dictionary of stat changes for the popup
            stat_changes = {
                "level": self.level,
                "hp": {"old": old_max_hp, "new": self.max_hp, "increase": hp_increase},
                "mp": {"old": old_max_mp, "new": self.max_mp, "increase": mp_increase},
                "attack": {"old": old_attack, "new": self.attack, "increase": attack_increase},
                "defense": {"old": old_defense, "new": self.defense, "increase": defense_increase},
                "speed": {"old": old_speed, "new": self.speed, "increase": speed_increase}
            }
            
            return stat_changes
        return False
    
    def gain_exp(self, exp):
        # Increase experience by 20%
        exp = int(exp * 1.2)
        self.exp += exp
        leveled = False
        stat_changes = None
        
        while self.exp >= self.max_exp and self.level < 100:
            result = self.level_up()
            if result:
                leveled = True
                stat_changes = result  # Store the stat changes from the most recent level up
                
        return leveled, stat_changes
