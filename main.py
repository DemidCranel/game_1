# Отрисовать декорации
# Отцентрировать текст по кнопке
# Сделать изменение game_status с menu на game при нажатии на кнопку старта

import pygame
import time
import random

pygame.init()

screen_xy = (1920, 1080)
screen = pygame.display.set_mode(screen_xy)
clock = pygame.time.Clock()
bullet_speed = 20

font_text = pygame.font.SysFont('Comic Sans MS', 50)

# Все возможные гейм статусы: menu - Главное меню, game - Игровой статус
game_status = 'game'

emulate_config = {
    'player_save':{
        'hp':5,
        'speed':9,
        'speed_down':3,
        'speed_up':15,
        'damage':1,
        'atack_speed':0.25,
        'coord':[screen_xy[0] / 2 - 25, screen_xy[1] - screen_xy[1] / 5], # Вычитаем 25 потому что это половина размера игрока
        'color':[60, 60, 60],
        'size':50,
        'money_multi':1,
        'max_coord_y':screen_xy[1] - screen_xy[1] / 3 - 25, # Вычитаем 25 потому что это половина размера игрока
    },
    'target_settings':{
        'speed':2.75,
        'cooldown':1,
    }
}


class Player():
    def __init__(self, speed, damage, atack_speed, money_multi, coord, color, size, speed_down, speed_up, hp, max_coord_y):
        self.speed = speed
        self.damage = damage
        self.atack_speed = atack_speed
        self.money_multi = money_multi
        self.coord = coord
        self.color = color
        self.line_x = None
        self.line_y = None
        self.size = size
        self.speed_down = speed_down
        self.speed_up = speed_up
        self.speed_status = 0 # 0 - обычная скорость, 1 - быстрая скорость, 2 - медленная скорость
        self.hp = hp
        self.score = 0
        self.max_coord_y = max_coord_y


    def move(self):
        if self.speed_status != 0 and shift_up and not space_up:
            self.speed_status = 2
        elif self.speed_status != 0 and space_up and not shift_up:
            self.speed_status = 1
        elif self.speed_status != 0 and space_up and shift_up:
            self.speed_status = 0

        if self.line_x == "Right" and self.line_y == None:
            if self.speed_status == 0:
                self.coord[0] += self.speed
            elif self.speed_status == 1:
                self.coord[0] += self.speed_up
            elif self.speed_status == 2:
                self.coord[0] += self.speed_down
        elif self.line_x == 'Right':
            if self.speed_status == 0:
                self.coord[0] += self.speed * 0.7
            elif self.speed_status == 1:
                self.coord[0] += self.speed_up * 0.7
            elif self.speed_status == 2:
                self.coord[0] += self.speed_down * 0.7

        if self.line_x == "Left" and self.line_x == None:
            if self.speed_status == 0:
                self.coord[0] -= self.speed
            elif self.speed_status == 1:
                self.coord[0] -= self.speed_up
            elif self.speed_status == 2:
                self.coord[0] -= self.speed_down
        elif self.line_x == 'Left':
            if self.speed_status == 0:
                self.coord[0] -= self.speed * 0.7
            elif self.speed_status == 1:
                self.coord[0] -= self.speed_up * 0.7
            elif self.speed_status == 2:
                self.coord[0] -= self.speed_down * 0.7

        if self.line_y == "Up" and self.line_x == None:
            if self.speed_status == 0:
                self.coord[1] -= self.speed
            elif self.speed_status == 1:
                self.coord[1] -= self.speed_up
            elif self.speed_status == 2:
                self.coord[1] -= self.speed_down
        elif self.line_y == 'Up':
            if self.speed_status == 0:
                self.coord[1] -= self.speed * 0.7
            elif self.speed_status == 1:
                self.coord[1] -= self.speed_up * 0.7
            elif self.speed_status == 2:
                self.coord[1] -= self.speed_down * 0.7

        if self.line_y == "Down" and self.line_x == None:
            if self.speed_status == 0:
                self.coord[1] += self.speed
            elif self.speed_status == 1:
                self.coord[1] += self.speed_up
            elif self.speed_status == 2:
                self.coord[1] += self.speed_down
        elif self.line_y == "Down":
            if self.speed_status == 0:
                self.coord[1] += self.speed * 0.7
            elif self.speed_status == 1:
                self.coord[1] += self.speed_up * 0.7
            elif self.speed_status == 2:
                self.coord[1] += self.speed_down * 0.7

        if self.coord[0] + self.size / 2 > screen_xy[0]:
            self.coord[0] = screen_xy[0] - self.size / 2

        if self.coord[0] - self.size / 2 < 0:
            self.coord[0] = 0 + self.size / 2

        if self.coord[1] - self.size <= self.max_coord_y:
            self.coord[1] = self.max_coord_y + self.size

        if self.coord[1] >= screen_xy[1] - self.size / 2:
            self.coord[1] = screen_xy[1] - self.size / 2


    def player_render(self):
        pygame.draw.rect(screen, self.color, (self.coord[0] - self.size/2, self.coord[1] - self.size/2, self.size, self.size)) # 25 вычитаем из-за того что это половина от размера игрока

    def player_tick(self):
        if self.hp <= 0:
            self.hp = emulate_config['player_save']['hp']
            self.score = 0



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
            self.bullets_all.append(
                {'coord':[player.coord[0] - self.width / 2, player.coord[1] - player.size / 2],
                 'damage':emulate_config['player_save']['damage']
                 })
            self.time_last_bullet = time.time()
            self.actual_targets += 1

    def bullet_render(self):
        for bullet in self.bullets_all:
            bullet = bullet['coord']
            pygame.draw.rect(screen, (255, 55, 55), (bullet[0], bullet[1] - player.size / 2 + self.width, self.width, self.height))

    def tick(self):
        if target.actual_targets > 0 and self.actual_targets > 0:
            for index_bullet in range(len(self.bullets_all)):
                for index_target in range(len(target.all_targets)):
                    if self.bullets_all[index_bullet]['coord'][0] > target.all_targets[index_target]['coord'][0] and self.bullets_all[index_bullet]['coord'][0] < target.all_targets[index_target]['coord'][0] + target.all_targets[index_target]['size']:
                        if self.bullets_all[index_bullet]['coord'][1] > target.all_targets[index_target]['coord'][1] and self.bullets_all[index_bullet]['coord'][1] < target.all_targets[index_target]['coord'][1] + target.all_targets[index_target]['size']:
                            player.score += 5
                            self.delete_bullets.append(index_bullet)
                            if target.all_targets[index_target]['hp'] - player.damage <= 0:
                                self.delete_targets.append(index_target)
                            else:
                                target.all_targets[index_target]['hp'] -= player.damage
                                target.all_targets[index_target]['color'] = (204, 255, 0)
        for index in range(len(self.bullets_all)):
            self.bullets_all[index]['coord'][1] -= self.speed
            if self.bullets_all[index]['coord'][1] + self.width < 0:
                self.delete_bullets.append(index)
        try:
            for index in self.delete_bullets:
                self.bullets_all.pop(index)
                self.actual_targets -= 1
        except: pass
        for index in self.delete_targets:
            target.all_targets.pop(index)
        self.delete_bullets = []
        self.delete_targets = []



class Target():

    def __init__(self, speed, cooldown):
        self.speed = speed
        self.all_targets = []
        self.actual_targets = 0
        self.delete_targets = []
        self.cooldown = cooldown
        self.last_time = 0

    def new_target(self):
        if time.time() - self.last_time > self.cooldown:
            if random.randint(1,2) == 1:
                size_target = random.randint(75,110)
            else:
                size_target = random.randint(140, 175)
            self.all_targets.append({
                'coord':[random.randint(size_target, screen_xy[0] - size_target * 2), size_target * -1],
                'hp':2 if size_target < 125 else 1,
                'size': size_target,
                'speed':self.speed if size_target > 125 else self.speed - (self.speed / 100) * 50,
                'color': (247, 143, 57) if size_target > 125 else (0, 255, 9),
            })
            self.actual_targets += 1
            self.last_time = time.time()

    def target_tick(self):
        self.new_target()
        for index in range(len(self.all_targets)):
            self.all_targets[index]['coord'][1] += self.all_targets[index]['speed']
            if self.all_targets[index]['coord'][1] > screen_xy[1]:
                self.delete_targets.append(index)
                player.hp -= 1
        for index in self.delete_targets:
            self.all_targets.pop(index)
            self.actual_targets -= 1
        self.delete_targets = []

    def target_render(self):
        for target in self.all_targets:
            pygame.draw.rect(screen, target['color'], (target['coord'][0], target['coord'][1], target['size'], target['size']))

menu_button_count = 0

class MainMenu():

    def __init__(self, widht, height, size_text):
        self.widht = widht
        self.height = height
        self.button_list = []
        self.size_text = size_text
        self.font_text_button = pygame.font.SysFont('Comic Sans MS', size_text)

    def new_button(self, text, coord):
        self.button_list.append([coord[0], coord[1], self.widht, self.height, text])

    def button_render(self):
        for button in self.button_list:
            pygame.draw.rect(screen, (255, 255, 255), (button[0], button[1], button[2], button[3]))
            screen.blit(self.font_text_button.render(button[4], False, (0, 0, 0)), (button[0] + self.widht / 2 - self.size_text, button[1] + self.height / 2 - self.size_text))

mainMenu = MainMenu(400, 150, size_text=50)



def start_cycle():

    if game_status == 'menu':
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_xy[0], screen_xy[1]))
        mainMenu.new_button('Start', [screen_xy[0] / 2 - mainMenu.widht / 2, screen_xy[1] / 2 - mainMenu.height / 2])
        mainMenu.button_render()

    elif game_status == 'game':
        pygame.draw.rect(screen, (60, 60, 60), (0,0,screen_xy[0],screen_xy[1])) # Задний фон

        player.move() # Выполняем функцию передвижения у игрока

        pygame.draw.rect(screen, (255, 255, 255), (0, screen_xy[1] - screen_xy[1] / 3, screen_xy[0], screen_xy[1] / 3))

        bullet.bullet_render() # Отрисовываем пули
        target.target_render() # Отрисовываем таргет
        player.player_render() # Отрисовываем игрока


        # Текст здоровья
        text_hp = font_text.render(f'Здоровье: {player.hp}', False, (255, 255, 255))
        screen.blit(text_hp, (50, 50))
        # Текст счета
        text_score = font_text.render(f'Счет: {player.score}', False, (255, 255, 255))
        screen.blit(text_score, (50, 110))


        target.target_tick()
        bullet.tick()
        player.player_tick()
        clock.tick(160) # Ограничение фпс



# Тут создаются объекты класса и так же происходит их настройка
player = Player( # Характеристики игрока
    speed=emulate_config['player_save']['speed'],
    damage=emulate_config['player_save']['damage'],
    atack_speed=emulate_config['player_save']['atack_speed'],
    money_multi=emulate_config['player_save']['money_multi'],
    coord=emulate_config['player_save']['coord'],
    color=emulate_config['player_save']['color'],
    size=emulate_config['player_save']['size'],
    speed_down=emulate_config['player_save']['speed_down'],
    speed_up=emulate_config['player_save']['speed_up'],
    hp=emulate_config['player_save']['hp'],
    max_coord_y=emulate_config['player_save']['max_coord_y'],
)
bullet = Bullets(cd_bullet=emulate_config['player_save']['atack_speed']) # cd_bullet содержит в себе минимальное значение в секундах между выстрелами
target = Target(
    speed=emulate_config['target_settings']['speed'],
    cooldown=emulate_config['target_settings']['cooldown'],
)

mouse_lkm_down = False
shift_up = True
space_up = True

while True:

    # Проверка событий №1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_status == 'game':
            game_status = 'menu'

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_lkm_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_lkm_down = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            player.speed_status = 1
            shift_up = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.speed_status = 2
            space_up = False

        if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            shift_up = True
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space_up = True

    # Проверка событий №2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.line_x = "Right"
    elif keys[pygame.K_a]:
        player.line_x = "Left"
    else:
        player.line_x = None
    if keys[pygame.K_d] and keys[pygame.K_a]:
        player.line_x = None

    if keys[pygame.K_w]:
        player.line_y = "Up"
    elif keys[pygame.K_s]:
        player.line_y = "Down"
    else:
        player.line_y = None
    if keys[pygame.K_w] and keys[pygame.K_s]:
        player.line_y = None

    if mouse_lkm_down:
        bullet.new_bullet()

    start_cycle()


    pygame.display.flip()
