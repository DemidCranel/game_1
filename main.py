# Добавить класс для пули, мишеней и для отрисованных объектов-декораций

import pygame

pygame.init()

screen_xy = (1920, 1080)

screen = pygame.display.set_mode(screen_xy)
emulate_config = {
    'player_save':{
        'speed':5,
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



player = Player(
    emulate_config['player_save']['speed'],
    emulate_config['player_save']['damage'],
    emulate_config['player_save']['atack_speed'],
    emulate_config['player_save']['money_multi'],
    emulate_config['player_save']['coord'],
    emulate_config['player_save']['color'],
    emulate_config['player_save']['size'],
)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.line = "Right"
            if event.key == pygame.K_a:
                player.line = "Left"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                player.line = None

    pygame.draw.rect(screen, (60, 60, 60), (0,0,screen_xy[0],screen_xy[1]))

    player.move()
    player.player_render()


    pygame.display.flip()
