import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvation:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invation")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self._create_fleet()
        self.play_button = Button(self,"PLAY")
        self.sb = Scoreboard(self)


    def _check_key_down_event_(self,event):
        #响应按下
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_key_up_event(self,event):
        #响应松开
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_event_(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pose = pygame.mouse.get_pos()
                self._check_play_button(mouse_pose)


    def _check_play_button(self,mouse_pose):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pose)
        if button_clicked and not self.stats.game_active:
            #重置游戏统治信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.score = 0
            self.sb.prep_score()
            self.sb.prep_ships()
            self.sb.prep_level()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人并且让飞船屈中
            self._create_fleet()
            self.ship.center_ship()

            #隐藏鼠标光标
            #pygame.mouse.set_visible(False)


    def _fire_bullet(self):
        """创建一颗子弹并且把它加入到编组中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _create_fleet(self):
        """创建外星人群"""

        #创建一个外星人并计算一行可以容纳多少外星人
        #外星人间距设置为外星人宽度
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (alien_width * 2)
        number_aliens_x = available_space_x // (2 * alien_width)

        #计算屏幕最多可容纳多少外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 3 *alien_height - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #创建一个外星人并加入当前行
                self._create_alien(alien_number , row_number)



    def _create_alien(self , alien_number , row_number):
        # 创建一个外星人并加入当前行
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """将外星人群向下移动并且改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1



    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹位置并删除子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #删除现有子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()

            #提升等级
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()



    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:

            #将ship_left减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.stats.game_active = False


    def _check_alien_bottom(self):
        """检查是否有外星人到达底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _update_aliens(self):
        """检查是否有外星人位于边缘"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检查是否有外星人到达底部
        self._check_alien_bottom()


    def run_game(self):
        """开始游戏主循环"""
        while True:
            #监听键盘和鼠标事件
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()

            self._update_screen()



if __name__ == '__main__':
    #创建游戏实例并运行实例
    ai = AlienInvation()
    ai.run_game()