import pygame
import time
import random
import configparser

pygame.init()

screen_xy = (1920, 1080)
screen = pygame.display.set_mode(screen_xy)
clock = pygame.time.Clock()
bullet_speed = 20

font_text = pygame.font.SysFont('Comic Sans MS', 50)

# Все возможные гейм статусы: menu - Главное меню, game - Игровой статус
game_status = 'menu'

config = configparser.ConfigParser()

def save_config():
    # Сохранение изминения в конфиг файле
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def read_config():
    # Чтение файла конфигурации
    config.read('config.ini')

read_config() # Читаем конфиг чтобы работать с ним

emulate_config = {
    'player_save':{
        'hp':float(config.get('Stats', 'hp')),
        'speed':float(config.get('Stats', 'speed')),
        'speed_down':float(config.get('Stats', 'speed_down')),
        'speed_up':float(config.get('Stats', 'speed_up')),
        'damage':float(config.get('Stats', 'damage')),
        'atack_speed':float(config.get('Stats', 'atack_speed')),
        'coord':[screen_xy[0] / 2 - 25, screen_xy[1] - screen_xy[1] / 5], # Вычитаем 25 потому что это половина размера игрока
        'color':[60, 60, 60],
        'size':50,
        'point_multi':float(config.get('Stats', 'point_multi')),
        'max_coord_y':screen_xy[1] - screen_xy[1] / 3 - 25, # Вычитаем 25 потому что это половина размера игрока
        'lvl_upgrade_damage':float(config.get('Stats', 'lvl_upgrade_damage')),
        'lvl_upgrade_hp':float(config.get('Stats', 'lvl_upgrade_hp')),
        'lvl_upgrade_atack_speed':float(config.get('Stats', 'lvl_upgrade_atack_speed')),
        'max_hp':float(config.get('Stats', 'max_hp')),
        'lvl_upgrade_speed_target':int(config.get('Stats', 'lvl_upgrade_speed_target')),
        'lvl_upgrade_count_bullet':int(config.get('Stats', 'lvl_upgrade_count_bullet')),
    },
    'target_settings':{
        'speed':float(config.get('Target', "speed")),
        'cooldown':float(config.get('Target', 'cooldown')),
    }
}


class Player():
    def __init__(
            self, speed, damage, atack_speed,
            point_multi, coord, color, size,
            speed_down, speed_up, hp, max_coord_y,
            all_points, lvl_upgrade_damage, lvl_upgrade_hp, lvl_upgrade_atack_speed,
            max_hp, lvl_upgrade_speed_target, lvl_upgrade_count_bullet):

        self.speed = speed
        self.damage = damage
        self.atack_speed = atack_speed
        self.point_multi = point_multi
        self.coord = coord
        self.color = color
        self.line_x = None
        self.line_y = None
        self.size = size
        self.speed_down = speed_down
        self.speed_up = speed_up
        self.speed_status = 0 # 0 - обычная скорость, 1 - быстрая скорость, 2 - медленная скорость
        self.hp = hp
        self.max_hp = max_hp
        self.score = 0
        self.max_coord_y = max_coord_y
        self.all_points = all_points
        self.lvl_upgrade_damage = lvl_upgrade_damage
        self.lvl_upgrade_hp = lvl_upgrade_hp
        self.lvl_upgrade_atack_speed = lvl_upgrade_atack_speed
        self.lvl_upgrade_speed_target = lvl_upgrade_speed_target
        self.lvl_upgrade_count_bullet = lvl_upgrade_count_bullet
        self.last_multi_time = time.time()



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
        if time.time() - self.last_multi_time >= 5:
            self.last_multi_time = time.time()
            self.point_multi = round(self.point_multi + 0.1, 1)


        if self.hp <= 0:
            self.hp = self.max_hp
            config.set('Stats', 'hp', str(self.max_hp))
            self.score = 0
            self.point_multi = emulate_config['player_save']['point_multi']



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
        self.cd_bullet = player.atack_speed
        if time.time() - self.time_last_bullet > self.cd_bullet:
            if player.lvl_upgrade_count_bullet == 0:
                self.bullets_all.append(
                    {'coord':[player.coord[0] - self.width / 2, player.coord[1] - player.size / 2],
                     'damage':emulate_config['player_save']['damage']
                     })
                self.time_last_bullet = time.time()
                self.actual_targets += 1

            elif player.lvl_upgrade_count_bullet == 1:
                self.bullets_all.append(
                    {'coord':[player.coord[0] - (self.width / 2 + self.width * 2), player.coord[1] - player.size / 2],
                     'damage':emulate_config['player_save']['damage']})
                self.bullets_all.append(
                    {'coord': [player.coord[0] - (self.width / 2 - self.width * 2), player.coord[1] - player.size / 2],
                     'damage': emulate_config['player_save']['damage']})
                self.time_last_bullet = time.time()
                self.actual_targets += 2

            if player.lvl_upgrade_count_bullet == 2:
                self.bullets_all.append(
                    {'coord':[player.coord[0] - self.width / 2, player.coord[1] - player.size / 2],
                     'damage':emulate_config['player_save']['damage']
                     })
                self.bullets_all.append(
                    {'coord':[player.coord[0] - (self.width / 2 + self.width * 4), player.coord[1] - player.size / 2],
                     'damage':emulate_config['player_save']['damage']
                     })
                self.bullets_all.append(
                    {'coord':[player.coord[0] - (self.width / 2 - self.width * 4), player.coord[1] - player.size / 2],
                     'damage':emulate_config['player_save']['damage']
                     })
                self.time_last_bullet = time.time()
                self.actual_targets += 3

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
                            if player.damage == 2 and target.all_targets[index_target]['size'] < 125:
                                player.score += 10 * player.point_multi
                                player.all_points += 10 * player.point_multi
                            else:
                                player.score += 5 * emulate_config['player_save']['point_multi']
                                player.all_points += 5 * emulate_config['player_save']['point_multi']
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
        try:
            for index in self.delete_targets:
                target.all_targets.pop(index)
        except: pass
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
        self.cost_upgrade_damage = 100
        self.max_upgrade_damage = 1
        self.cost_upgrade_hp = 50
        self.max_upgrade_hp = 5
        self.cost_atack_speed = 75
        self.max_atack_speed = 4
        self.cost_upgrade_speed_target = 100
        self.max_upgrade_speed_target = 2
        self.cost_upgrade_count_bullet = 100
        self.max_upgrade_count_bullet = 2

    def new_mini_button(self, coord, text='test'): # Размер кнопок всегда 50
        font_text = pygame.font.SysFont('Comic Sans MS', 25)
        pygame.draw.rect(screen, (255, 255, 255), (coord[0], coord[1], 50, 50)) # Рисуем плюсики
        pygame.draw.rect(screen, (0, 0, 0), (coord[0] + 10, coord[1] + 20, 30, 10)) # Рисуем плюсики
        pygame.draw.rect(screen, (0, 0, 0), (coord[0] + 20, coord[1] + 10, 10, 30)) # Рисуем плюсики
        screen.blit(font_text.render(text, True, (255, 255, 255)), (coord[0] + 75, coord[1] + 2.5))

    def event_buy(self, type_event):
        if type_event == 'damage' and player.all_points >= self.cost_upgrade_damage and player.lvl_upgrade_damage < self.max_upgrade_damage:
            config.set('Stats', 'all_points', f'{player.all_points - self.cost_upgrade_damage}')
            config.set('Stats', 'lvl_upgrade_damage', f'{player.lvl_upgrade_damage + 1}')
            config.set('Stats', 'damage', f'{player.damage + 1}')
            player.all_points -= self.cost_upgrade_damage
            player.lvl_upgrade_damage += 1
            player.damage += 1
            save_config()
            read_config()

        elif type_event == 'hp' and player.all_points >= self.cost_upgrade_hp and player.lvl_upgrade_hp < self.max_upgrade_hp:
            config.set('Stats', 'all_points', f'{player.all_points - self.cost_upgrade_hp}')
            config.set('Stats', 'lvl_upgrade_hp', f'{player.lvl_upgrade_hp + 1}')
            config.set('Stats', 'max_hp', f'{player.hp + 1}')
            player.all_points -= self.cost_upgrade_hp
            player.lvl_upgrade_hp += 1
            player.max_hp += 1
            player.hp = player.max_hp
            save_config()
            read_config()

        elif type_event == 'atack_speed' and player.all_points >= self.cost_atack_speed and player.lvl_upgrade_atack_speed < self.max_atack_speed:
            config.set('Stats', 'all_points', f'{player.all_points - self.cost_atack_speed}')
            config.set('Stats', 'lvl_upgrade_atack_speed', f'{player.lvl_upgrade_atack_speed + 1}')
            config.set('Stats', 'atack_speed', f'{player.atack_speed - 0.1}')
            emulate_config['player_save']['atack_speed'] = player.atack_speed - 0.1
            player.all_points -= self.cost_atack_speed
            player.lvl_upgrade_atack_speed += 1
            player.atack_speed -= 0.1
            save_config()
            read_config()

        elif type_event == 'speed_target' and player.all_points >= self.cost_upgrade_speed_target and player.lvl_upgrade_speed_target < self.max_upgrade_speed_target:
            config.set('Stats', 'all_points', f'{player.all_points - self.cost_upgrade_speed_target}')
            config.set('Stats', 'lvl_upgrade_speed_target', f'{player.lvl_upgrade_speed_target + 1}')
            config.set('Target', 'speed', f'{target.speed - 1}')
            emulate_config['target_settings']['speed'] = target.speed - 1
            player.all_points -= self.cost_upgrade_speed_target
            player.lvl_upgrade_speed_target += 1
            target.speed -= 1
            save_config()
            read_config()

        elif type_event == 'count_bullet' and player.all_points >= self.cost_upgrade_count_bullet and player.lvl_upgrade_count_bullet < self.max_upgrade_count_bullet:
            config.set('Stats', 'all_points', f'{player.all_points - self.cost_upgrade_count_bullet}')
            config.set('Stats', 'lvl_upgrade_count_bullet', f'{player.lvl_upgrade_count_bullet + 1}')
            emulate_config['player_save']['lvl_upgrade_count_bullet'] = player.lvl_upgrade_count_bullet + 1
            player.all_points -= self.cost_upgrade_count_bullet
            player.lvl_upgrade_count_bullet += 1
            save_config()
            read_config()

    def menu_render(self):
        pygame.draw.rect(screen, (255, 255, 255), (screen_xy[0] // 2 - self.widht // 2, screen_xy[1] // 2 - self.height // 2, self.widht, self.height))

        text_start = font_text.render("Старт", True, (0, 0, 0))
        text_start_rect = text_start.get_rect(center=(self.widht // 2, self.height // 2))
        text_start_rect.x += screen_xy[0] // 2 - self.widht // 2
        text_start_rect.y += screen_xy[1] // 2 - self.height // 2
        screen.blit(text_start, text_start_rect)

        # Информация о балансе на экране
        font_text_1 = pygame.font.SysFont('Comic Sans MS', 25)
        screen.blit(font_text_1.render(f'Баланс {int(player.all_points)} поинтов', True, (255, 255, 255)), (100, 100 + 2.5))

        self.new_mini_button([100, screen_xy[1] - 600],
                             f'Улучшить урон за {int(self.cost_upgrade_damage)} поинтов | {int(player.lvl_upgrade_damage)} lvl' if player.lvl_upgrade_damage < self.max_upgrade_damage
                             else f'Максимальное улучшение! | {int(player.lvl_upgrade_damage)} lvl')
        if click and pygame.Rect(100, screen_xy[1] - 600, 50, 50).collidepoint(pygame.mouse.get_pos()):
            self.event_buy('damage')

        self.new_mini_button([100, screen_xy[1] - 500], f'Улучшить хп за {int(self.cost_upgrade_hp)} поинтов | {int(player.lvl_upgrade_hp)} lvl'
                            if player.lvl_upgrade_hp < self.max_upgrade_hp else f'Максимальное улучшение! | {int(player.lvl_upgrade_hp)} lvl')
        if click and pygame.Rect(100, screen_xy[1] - 500, 50, 50).collidepoint(pygame.mouse.get_pos()):
            self.event_buy('hp')

        self.new_mini_button([100, screen_xy[1] - 400],
                             f'Улучшить скорость атаки за {int(self.cost_atack_speed)} поинтов | {int(player.lvl_upgrade_atack_speed)} lvl'
                             if player.lvl_upgrade_atack_speed < self.max_atack_speed else f'Максимальное улучшение! | {int(player.lvl_upgrade_atack_speed)} lvl')
        if click and pygame.Rect(100, screen_xy[1] - 400, 50, 50).collidepoint(pygame.mouse.get_pos()):
            self.event_buy('atack_speed')

        self.new_mini_button([100, screen_xy[1] - 300],
                             f'Улучшить замедление мишеней за {int(self.cost_upgrade_speed_target)} поинтов | {int(player.lvl_upgrade_speed_target)} lvl'
                             if player.lvl_upgrade_speed_target < self.max_upgrade_speed_target else f'Максимальное улучшение! | {int(player.lvl_upgrade_speed_target)} lvl')
        if click and pygame.Rect(100, screen_xy[1] - 300, 50, 50).collidepoint(pygame.mouse.get_pos()):
            self.event_buy('speed_target')

        self.new_mini_button([100, screen_xy[1] - 200],
                             f'Улучшить количество пулей за {int(self.cost_upgrade_count_bullet)} поинтов | {int(player.lvl_upgrade_count_bullet)} lvl'
                             if player.lvl_upgrade_count_bullet < self.max_upgrade_count_bullet else f'Максимальное улучшение! | {int(player.lvl_upgrade_count_bullet)} lvl')
        if click and pygame.Rect(100, screen_xy[1] - 200, 50, 50).collidepoint(pygame.mouse.get_pos()):
            self.event_buy('count_bullet')



mainMenu = MainMenu(400, 150, size_text=50)
menu_status_last = False

# Тут создаются объекты класса и так же происходит их настройка
player = Player( # Характеристики игрока
    speed=emulate_config['player_save']['speed'],
    damage=emulate_config['player_save']['damage'],
    atack_speed=emulate_config['player_save']['atack_speed'],
    point_multi=emulate_config['player_save']['point_multi'],
    coord=emulate_config['player_save']['coord'],
    color=emulate_config['player_save']['color'],
    size=emulate_config['player_save']['size'],
    speed_down=emulate_config['player_save']['speed_down'],
    speed_up=emulate_config['player_save']['speed_up'],
    hp=emulate_config['player_save']['hp'],
    max_coord_y=emulate_config['player_save']['max_coord_y'],
    all_points=float(config.get('Stats', 'all_points')),
    lvl_upgrade_damage=emulate_config['player_save']['lvl_upgrade_damage'],
    lvl_upgrade_hp=emulate_config['player_save']['lvl_upgrade_hp'],
    lvl_upgrade_atack_speed=emulate_config['player_save']['lvl_upgrade_atack_speed'],
    max_hp=emulate_config['player_save']['max_hp'],
    lvl_upgrade_speed_target=emulate_config['player_save']['lvl_upgrade_speed_target'],
    lvl_upgrade_count_bullet=emulate_config['player_save']['lvl_upgrade_count_bullet'],
)
bullet = Bullets(cd_bullet=emulate_config['player_save']['atack_speed']) # cd_bullet содержит в себе минимальное значение в секундах между выстрелами
target = Target(
    speed=emulate_config['target_settings']['speed'],
    cooldown=emulate_config['target_settings']['cooldown'],
)

mouse_lkm_down = False
shift_up = True
space_up = True

time_cycle_last = 0

def start_cycle():
    global menu_status_last
    if game_status == 'menu':
        pygame.draw.rect(screen, (70, 70, 70), (0, 0, screen_xy[0], screen_xy[1]))
        mainMenu.menu_render()
        menu_status_last = True

    elif game_status == 'game':
        if menu_status_last:
            menu_status_last = False
            player.coord = emulate_config['player_save']['coord']
            bullet.bullets_all = []
            target.all_targets = []
            target.last_time = 0
            player.score = 0
            player.hp = emulate_config['player_save']['hp']

        pygame.draw.rect(screen, (60, 60, 60), (0,0,screen_xy[0],screen_xy[1])) # Задний фон

        player.move() # Выполняем функцию передвижения у игрока

        pygame.draw.rect(screen, (255, 255, 255), (0, screen_xy[1] - screen_xy[1] / 3, screen_xy[0], screen_xy[1] / 3))

        bullet.bullet_render() # Отрисовываем пули
        target.target_render() # Отрисовываем таргет
        player.player_render() # Отрисовываем игрока


        # Текст здоровья
        text_hp = font_text.render(f'Здоровье: {int(player.hp)} / {int(player.max_hp)}', False, (255, 255, 255))
        screen.blit(text_hp, (50, 50))
        # Текст полученного счета
        text_score = font_text.render(f'Полученный счет: {int(player.score)}', False, (255, 255, 255))
        screen.blit(text_score, (50, 110))
        # Текст всего счета
        text_score = font_text.render(f'Счет: {int(player.all_points)}', False, (255, 255, 255))
        screen.blit(text_score, (50, 170))
        # Текст урона
        text_score = font_text.render(f'Урон: {int(player.damage)}', False, (255, 255, 255))
        screen.blit(text_score, (50, 230))
        # Текст множетеля
        text_score = font_text.render(f'Множитель: {player.point_multi}', False, (255, 255, 255))
        screen.blit(text_score, (50, 290))


        target.target_tick()
        bullet.tick()
        player.player_tick()
        clock.tick(160) # Ограничение фпс


    global time_cycle_last
    if time.time() - time_cycle_last >= 5:
        time_cycle_last = time.time()
        config.set('Stats', 'all_points', str(player.all_points))
        save_config()
        read_config()



while True:
    click = False
    # Проверка событий №1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Better to seperate to a new if statement aswell, since there's more buttons that can be clicked and makes for cleaner code.
            if event.button == 1:
                click = True
                if (event.pos[0] > screen_xy[0] // 2 - mainMenu.widht // 2 and event.pos[0] < screen_xy[0] // 2 + mainMenu.widht // 2):
                    if (event.pos[1] > screen_xy[1] // 2 - mainMenu.height // 2 and event.pos[1] < screen_xy[1] // 2 + mainMenu.height // 2):
                        game_status = 'game'

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_status == 'game':
            game_status = 'menu'

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_lkm_down = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
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
