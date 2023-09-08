import pygame

class GameStats:
    """跟踪统计游戏信息"""

    def __init__(self , ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.score = 0
        with open('high_score') as p:
            self.high_score = int(p.read())

    def reset_stats(self):
        """初始化在游戏变化期间可能变化的游戏信息"""
        self.ships_left = self.settings.ship_limit
        self.level = 1
