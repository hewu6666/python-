import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self,ai_game):
        """初始化飞船并设置初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images\ship3.png')
        self.rect = self.image.get_rect()

        #对于每艘新的飞船，把它放在屏幕最底端的中央
        self.rect.midbottom = self.screen_rect.midbottom
        self.x=float(self.rect.x)

        #移动标志
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)


    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x=self.x


    def center_ship(self):
        """让飞船在屏幕底部居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

