#!/usr/bin/env python3
"""
Dungeons of Eternity - Game Balance System
"""

class CardBalance:
    """Manages card balance and scaling"""
    
    # Base damage values for different card types
    CARD_TYPE_BASE_DAMAGE = {
        'attack': 5,
        'spell': 8,
        'item': 3,
        'skill': 10
    }
    
    # Rarity modifiers
    RARITY_MODIFIERS = {
        'common': 1.0,
        'uncommon': 1.5,
        'rare': 2.0,
        'legendary': 3.0
    }
    
    @staticmethod
    def calculate_damage(card_type: str, rarity: str, level: int) -> float:
        """
        Calculate damage for a card based on type, rarity, and level.
        
        Args:
            card_type: Type of the card (attack, spell, item, skill)
            rarity: Rarity of the card (common, uncommon, rare, legendary)
            level: Current level of the card
            
        Returns:
            float: Calculated damage value
        """
        base_damage = CardBalance.CARD_TYPE_BASE_DAMAGE.get(card_type, 5)
        rarity_mod = CardBalance.RARITY_MODIFIERS.get(rarity, 1.0)
        level_scaling = 1 + (level * 0.1)  # 10% increase per level
        
        return base_damage * rarity_mod * level_scaling

class ResourceBalance:
    """Manages resource costs and rewards"""
    
    # Base costs for different actions
    ACTION_COSTS = {
        'move': 1,
        'attack': 2,
        'spell': 3,
        'item_use': 1,
        'skill_use': 4
    }
    
    # Resource rewards for different actions
    ACTION_REWARDS = {
        'enemy_defeat': 10,
        'puzzle_solve': 15,
        'treasure_find': 20,
        'boss_defeat': 50
    }
    
    @staticmethod
    def get_action_cost(action: str) -> int:
        """Get the cost for a specific action"""
        return ResourceBalance.ACTION_COSTS.get(action, 1)
    
    @staticmethod
    def get_action_reward(action: str) -> int:
        """Get the reward for a specific action"""
        return ResourceBalance.ACTION_REWARDS.get(action, 0)

class DifficultyBalance:
    """Manages game difficulty scaling"""
    
    # Base enemy stats
    ENEMY_BASE_STATS = {
        'health': 100,
        'damage': 10,
        'defense': 5
    }
    
    # Scaling factors per level
    LEVEL_SCALING = {
        'health': 1.2,  # 20% increase per level
        'damage': 1.1,  # 10% increase per level
        'defense': 1.05  # 5% increase per level
    }
    
    @staticmethod
    def scale_enemy_stats(level: int) -> dict:
        """
        Scale enemy stats based on level
        
        Args:
            level: Current game level
            
        Returns:
            dict: Scaled enemy stats
        """
        return {
            stat: base * (DifficultyBalance.LEVEL_SCALING[stat] ** (level - 1))
            for stat, base in DifficultyBalance.ENEMY_BASE_STATS.items()
        }
