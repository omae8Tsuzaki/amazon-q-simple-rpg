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
            
            self.max_hp += hp_increase
            self.max_mp += mp_increase  # Increase max MP
            self.hp = self.max_hp  # Full HP recovery on level up
            self.mp = self.max_mp  # Full MP recovery on level up
            self.attack += attack_increase
            self.defense += defense_increase
            self.speed += speed_increase
            
            return True
        return False
    
    def gain_exp(self, exp):
        # Increase experience by 20%
        exp = int(exp * 1.2)
        self.exp += exp
        leveled = False
        while self.exp >= self.max_exp and self.level < 100:
            leveled = self.level_up() or leveled
        return leveled
