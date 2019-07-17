import pygame
import random
# import time
# 向系统申请一块屏幕
pygame.mixer.init()
pygame.mixer.music.load('./music/flourish.mid')
mu2 = pygame.mixer.Sound('./music/music2.wav')
mu1 = pygame.mixer.Sound('./music/music1.wav')

pygame.init()
font = pygame.font.Font("./fonts/msyhbd.ttf", 26)


screen_with = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_with, screen_height))

bg = pygame.image.load('./imgs/qiBg.jpg')
screen.blit(bg, (-500, 0))
bat = pygame.image.load('./imgs/bat.png')
mu = pygame.image.load('./imgs/mu.jpg')
quan = pygame.image.load('./imgs/restart1.png')

ball64 = pygame.image.load('./imgs/ball_64.png')
ball32 = pygame.image.load('./imgs/ball_32.png')

ball_list = [{'img': ball64,
              'size': 64},
             {'img': ball32,
              'size': 32}]
bat_list = []
ball_number = 1
f_list = []


# 初始化和随机数组
def init_list():
    f_list.clear()
    for i in range(4):
        item = []
        for j in range(11):
            item.append(random.randint(0, 1))
        f_list.append(item)


init_list()

# 攻击对象
react = {
    'rac': quan,
    'size': 48
}
# 球对象
myball = {
    # 'ball': ball_list[random.randint(0, len(ball_list)-1)],
    'ball': ball_list[1],
    'pX': random.randint(50, screen_with - 100),
    'pY': random.randint(50, screen_height//2 - 100),
    # 'vX': random.randint(1, 5),
    # 'vY': random.randint(1, 8)
    'vX': 5,
    'vY': 8
}
# 托盘对象
tuopan = {
    'img': mu,
    'tx': 100,
    'ty': 600,
    'width': 300,
    'height': 30
}
#
while True:
    # 单独获取响应事件
    screen.blit(bg, (-500, 0))
    count = 0
    # 遍历甜甜圈数组
    for i, item in enumerate(f_list):
        for j, value in enumerate(item):
            f_x = 250 + j * 60
            f_y = 50 + i * 60
            if value == 1:
                count += 1
                if myball['pY'] + myball['ball']['size'] >= f_y and myball['pY'] <= (f_y + react['size']) and myball['pX'] + myball['ball']['size'] >= f_x and myball['pX'] <= f_x + react['size']:
                    if myball['pX'] + myball['ball']['size']//2 <= f_x or myball['pX'] + myball['ball']['size']//2 >= f_x + react['size']:
                        myball['vX'] = -myball['vX']
                        f_list[i][j] = 0
                    elif myball['pY'] + myball['ball']['size']//2 <= f_y or myball['pY'] + myball['ball']['size']//2 >= f_y + react['size']:
                        myball['vY'] = -myball['vY']
                        f_list[i][j] = 0
                    else:
                        myball['vX'] = -myball['vX']
                        myball['vY'] = -myball['vY']
                        f_list[i][j] = 0
                    mu2.play()

                # 画甜甜圈
                screen.blit(react['rac'], (f_x, f_y))
    # 甜甜圈没了，随机生成
    if count == 0:
        init_list()
    # 处理文本
    score = font.render("剩余数量" + str(count), True, (0xff, 0xff, 0x00))
    screen.blit(score, (50, 50))
    # 画球
    screen.blit(myball['ball']['img'], (myball['pX'], myball['pY']))
    # 改变位置
    myball['pY'] += myball['vY']
    myball['pX'] += myball['vX']
    # 判断上下边界
    if myball['pY'] >= (screen_height - myball['ball']['size']) or myball['pY'] <= 0:
        myball['vY'] = -myball['vY']
        mu1.play()
    # 判断左右边界
    if myball['pX'] >= (screen_with - myball['ball']['size']) or myball['pX'] <= 0:
        myball['vX'] = -myball['vX']
        mu1.play()
    # 球与图盘的碰撞
    if tuopan['ty'] - myball['ball']['size'] <= myball['pY'] <= (tuopan['ty'] + tuopan['height']) and tuopan['tx']-myball['ball']['size'] <= myball['pX'] <= tuopan['tx']+tuopan['width']:
        myball['vY'] = -myball['vY']
        mu1.play()

    tuopan['tx'] = myball['pX'] - 150

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(tuopan['img'], (tuopan['tx'], tuopan['ty']))

    # 鼠标移动
    # mousex,mousey = pygame.mouse.get_pos()
    # tuopan['tx'] = mousex - tuopan['width']//2
    pygame.display.update()

