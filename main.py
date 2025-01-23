# Добавить класс для мишеней и для отрисованных объектов-декораций

import pygame
import time

pygame.init()

screen_xy = (1020, 1080)
screen = pygame.display.set_mode(screen_xy)
clock = pygame.time.Clock()
bullet_speed = 20

emulate_config = {
    'player_save':{
        'speed':12,
        'damage':1,
        'atack_speed':1,
        'money_multi':1,
        'coord':[500,830],
        'color':[255,255,255],
        'size':50,
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

    def new_bullet(self):
        if time.time() - self.time_last_bullet > self.cd_bullet:
            self.bullets_all.append([player.coord[0], player.coord[1]])
            self.time_last_bullet = time.time()

    def bullet_render(self):
        for bullet in self.bullets_all:
            pygame.draw.rect(screen, (255, 55, 55), (bullet[0], bullet[1] - player.size / 2 + self.width, self.width, self.height))

    def tick(self):
        delete_bullets = []
        for index in range(len(self.bullets_all)):
            self.bullets_all[index][1] -= 20
            if self.bullets_all[index][1] + self.width < 0:
                delete_bullets.append(index)
        for index in delete_bullets:
            self.bullets_all.pop(index)

def start_cycle():
    pygame.draw.rect(screen, (60, 60, 60), (0,0,screen_xy[0],screen_xy[1])) # Задний фон

    player.move() # Выполняем функцию передвижения у игрока

    bullet.bullet_render()
    player.player_render() # Отрисовываем игрока

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

bullet = Bullets(cd_bullet=0.1) # cd_bullet содержит в себе минимальное значение в секундах между выстрелами


while True:
    # Проверка событий №1
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet.new_bullet()

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

    start_cycle()


    pygame.display.flip()
