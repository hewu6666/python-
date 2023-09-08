class Settings:
    """存储游戏中所有设置的类"""
    def __init__(self):
        """初始化的游戏设置"""
        #屏幕设置
        self.screen_width = 1500
        self.screen_height = 850
        self.bg_color = (230,230,230)

        #子弹设置
        self.bullet_speed = 2.0
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullets_allowed = 2
        self.bullet_color = (60,60,60)

        #外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 20
        #fleet_direction为1时表示右移，0表示左移
        self.fleet_direction = 1

        #飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3

        #加快游戏节奏的速度
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 1.0

        #fleet_direction为1表示向右，-1表示向左
        self.fleet_direction = 1

        #计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale



