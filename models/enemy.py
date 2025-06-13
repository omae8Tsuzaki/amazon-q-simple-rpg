import random

class Enemy:
    def __init__(self, player_level):
        # Random level up to player's level
        self.level = random.randint(max(1, player_level - 3), player_level)
        self.hp = 10 + self.level * 2
        self.max_hp = self.hp
        self.attack = 3 + self.level
        self.defense = 1 + self.level // 2
        self.speed = 2 + self.level // 3
        
        # Calculate base experience points
        base_exp = self.level * 10
        
        # Apply level-based bonus: higher level enemies give more exp
        level_bonus = 1.0
        if self.level > player_level:
            # Bonus for enemies higher than player level (challenging enemies)
            level_bonus = 1.5
        elif self.level == player_level:
            # Bonus for enemies at player level
            level_bonus = 1.2
        elif self.level >= player_level - 1:
            # Slight bonus for enemies just below player level
            level_bonus = 1.1
            
        # Apply the 20% general increase
        self.exp = int(base_exp * level_bonus * 1.2)
        
        # Randomly select enemy type
        enemy_types = ["Slime", "Goblin", "Bat", "Zombie", "Wolf"]
        self.name = random.choice(enemy_types)
        
        # Animation variables
        self.is_hit = False
        self.hit_timer = 0
