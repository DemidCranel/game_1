# Отрисовать декорации, сделать счетчик, сделать хп и перезапуск счетчика после падения хп до 0
# Сделать ускорение при зажатом пробеле и замедление при зажатом шифте

import pygame
import time
import random

pygame.init()

screen_xy = (1920, 1080)
screen = pygame.display.set_mode(screen_xy)
clock = pygame.time.Clock()
bullet_speed = 20

emulate_config = {
    'player_save':{
        'speed':8,
        'damage':1,
        'atack_speed':0.25,
        'money_multi':1,
        'coord':[500,830],
        'color':[255,255,255],
        'size':50,
    },
    'target_settings':{
        'size':125,
        'speed':2.75,
        'cooldown':1,
    }
}


class Player():
    def __init__(self, speed, damage, atack_speed, money_multi, coord, color, size):
        self.speed = speed
        self.damage = damage
        self.atack_speed = atack_speed
        self.money_multi = money_multi
        self.coord = coord
        self.color = color
        self.line = None
        self.size = size


    def move(self):
        if self.line == "Right":
            self.coord[0] += self.speed

        if self.line == "Left":
            self.coord[0] -= self.speed

        if self.coord[0] + self.size / 2 > screen_xy[0]:
            self.coord[0] = screen_xy[0] - self.size / 2

        if self.coord[0] - self.size / 2 < 0:
            self.coord[0] = 0 + self.size / 2


    def player_render(self):
        pygame.draw.rect(screen, (255,255,255), (self.coord[0] - self.size/2, self.coord[1] - self.size/2, self.size, self.size)) # 25 вычитаем из-за того что это половина от размера игрока



class Bullets():

    def __init__(self, cd_bullet):
        self.height = 25
        self.width = 10
        self.bullets_all = []
        self.time_last_bullet = 0
        self.cd_bullet = cd_bullet
        self.delete_bullets = []
        self.delete_targets = []
        self.actual_targets = 0
        self.speed = 10

    def new_bullet(self):
        if time.time() - self.time_last_bullet > self.cd_bullet:
            self.bullets_all.append([player.coord[0], player.coord[1]])
            self.time_last_bullet = time.time()
            self.actual_targets += 1

    def bullet_render(self):
        for bullet in self.bullets_all:
            pygame.draw.rect(screen, (255, 55, 55), (bullet[0], bullet[1] - player.size / 2 + self.width, self.width, self.height))

    def tick(self):
        if target.actual_targets > 0 and self.actual_targets > 0:
            for index_bullet in range(len(self.bullets_all)):
                for index_target in range(len(target.all_targets)):
                    if self.bullets_all[index_bullet][0] > target.all_targets[index_target][0] and self.bullets_all[index_bullet][0] < target.all_targets[index_target][0] + target.size:
                        if self.bullets_all[index_bullet][1] > target.all_targets[index_target][1] and self.bullets_all[index_bullet][1] < target.all_targets[index_target][1] + target.size:
                            self.delete_bullets.append(index_bullet)
                            self.delete_targets.append(index_target)
        for index in range(len(self.bullets_all)):
            self.bullets_all[index][1] -= self.speed
            if self.bullets_all[index][1] + self.width < 0:
                self.delete_bullets.append(index)
        for index in self.delete_bullets:
            self.bullets_all.pop(index)
            self.actual_targets -= 1
        for index in self.delete_targets:
            target.all_targets.pop(index)
        self.delete_bullets = []
        self.delete_targets = []



class Target():

    def __init__(self, size, speed, cooldown):
        self.size = size
        self.speed = speed
        self.all_targets = []
        self.actual_targets = 0
        self.delete_targets = []
        self.cooldown = cooldown
        self.last_time = 0

    def new_target(self):
        if time.time() - self.last_time > self.cooldown: # обавить условие
            self.all_targets.append([random.randint(self.size, screen_xy[0] - self.size * 2), self.size * -1])
            self.actual_targets += 1
            self.last_time = time.time()

    def target_tick(self):
        self.new_target()
        for index in range(len(self.all_targets)):
            self.all_targets[index][1] += self.speed
            if self.all_targets[index][1] > screen_xy[1]:
                self.delete_targets.append(index)
        for index in self.delete_targets:
            self.all_targets.pop(index)
            self.actual_targets -= 1
        self.delete_targets = []

    def target_render(self):
        for target in self.all_targets:
            pygame.draw.rect(screen, (247, 143, 57), (target[0], target[1], self.size, self.size))



def start_cycle():
    pygame.draw.rect(screen, (60, 60, 60), (0,0,screen_xy[0],screen_xy[1])) # Задний фон

    player.move() # Выполняем функцию передвижения у игрока

    bullet.bullet_render() # Отрисовываем пули
    target.target_render() # Отрисовываем таргет
    player.player_render() # Отрисовываем игрока

    target.target_tick()
    bullet.tick()
    clock.tick(160) # Ограничение фпс


# Тут создаются объекты класса и так же происходит их настройка
player = Player( # Характеристики игрока
    emulate_config['player_save']['speed'],
    emulate_config['player_save']['damage'],
    emulate_config['player_save']['atack_speed'],
    emulate_config['player_save']['money_multi'],
    emulate_config['player_save']['coord'],
    emulate_config['player_save']['color'],
    emulate_config['player_save']['size'],
)
bullet = Bullets(cd_bullet=emulate_config['player_save']['atack_speed']) # cd_bullet содержит в себе минимальное значение в секундах между выстрелами
target = Target(
    size=emulate_config['target_settings']['size'],
    speed=emulate_config['target_settings']['speed'],
    cooldown=emulate_config['target_settings']['cooldown'],
)

mouse_lkm_down = False

while True:
    # Проверка событий №1
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_lkm_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_lkm_down = False

    # Проверка событий №2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.line = "Right"
    elif keys[pygame.K_a]:
        player.line = "Left"
    else:
        player.line = None
    if keys[pygame.K_d] and keys[pygame.K_a]:
        player.line = None



    if mouse_lkm_down:
        bullet.new_bullet()

    start_cycle()


    pygame.display.flip()
