import pygame
import random

pygame.mixer.init()

mu1 = pygame.mixer.Sound('./music/music1.wav')

# 向系统申请一块屏幕
screen_with = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_with, screen_height))

pygame.init()

font = pygame.font.SysFont("", 54)

over = font.render("GAME OVER", True, (0xff,0xff,0x00))

bg = pygame.image.load('./imgs/qiBg.jpg')
screen.blit(bg, (-500, 0))

screen.blit(over, (50, 50))

text_list = []
zimu_list = []

for cc in range(26):
    zimu_list.append(chr(ord('A')+cc))

# print(zimu_list)

isOver = False
score = 0
#
while True:
    screen.blit(bg, (-500, 0))

    # 随机0~20 只有1的时候才执行随机生成，减小概率
    if random.randint(0, 20) == 1:
        # 随机生成 0或1 个字母，再次减小概率
        for i in range(random.randint(0, 1)):
            tt = {
                'zimu': zimu_list[random.randint(0, len(zimu_list)-1)],
                'pX': random.randint(100, screen_with-100),
                'pY': -100,
                'vY': 2,
                'color': (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            }
            text_list.append(tt)
    # 遍历字母数组
    for item in text_list:
        text = font.render(item['zimu'], True, item['color'])
        screen.blit(text, (item['pX'], item['pY']))
        # 改变位置
        item['pY'] += item['vY']
        # 字母超出下方屏幕处理
        if item['pY'] > screen_height:
            isOver = True
            text_list.remove(item)

    score_text = font.render("SCORE: " + str(score), True, (0xff, 0xff, 0x00))
    screen.blit(score_text, (50, 50))
    if isOver is True:
        screen.blit(over, (50, 100))

    # 单独获取响应事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # 键盘
        if event.type == pygame.KEYDOWN:
            # print(chr(event.key-32))
            for item in text_list:
                # 一句巧妙之处，将键盘小写字母ASCII值对应屏幕上的大写字母
                if item['zimu'] == chr(event.key-(ord('a')-ord('A'))):
                    mu1.play()
                    text_list.remove(item)
                    score += 10
                    break
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            dx, dy = event.pos
            for item in text_list:
                if  dx >= item['pX'] and  + dx <= item['pX'] + 25 and dy >= item['pY'] and  dy <= item['pY'] + 25:
                    mu1.play()
                    text_list.remove(item)
                    score += 10
                    break

    pygame.display.update()
