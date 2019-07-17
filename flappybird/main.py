import pygame
import random

pygame.mixer.init()
pygame.init()
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

se_fly = pygame.mixer.Sound('./fb_music/fly.wav')
se_crash = pygame.mixer.Sound('./fb_music/crash.wav')
font = pygame.font.Font("./fonts/msyhbd.ttf", 24)

# 标题
img_title = pygame.image.load('./fb_img/title.png')

# 游戏背景参数
img_bg = pygame.image.load('./fb_img/baibg.png')
bg_start = 0
bg_speed = 1
game_bg = {
    'start': 0,
    'speed': 1
}

# 游戏管道参数
img_pipe = pygame.image.load('./fb_img/pipe.png')
pipe_width = 50
pipe_height = 600
pipe_speed = 2
# # 上下管道间隔
# space_up_down = 150
# 前后管道间隔
space_front_back = pipe_speed*110

max_top = -pipe_height + 70
min_top = -pipe_height + screen_height // 2 + 30
# 管道数组
pipe_list = []

# -------- goodtimp start ---------
# 金币 pX pY score
gold_list = []
gold_width = 30
gold_height = 30

# 同屏幕下最大/最小的金币数量
max_gold_count = 3
min_space = 100  # 最小间距
prop = 100  # 越大 金币数量越少
max_gold_score = 3  # 最大的分数

img_gold = pygame.image.load('./fb_img/gold_medal.png')
img_gold = pygame.transform.scale(img_gold, (gold_width, gold_height))
img_silver = pygame.image.load('./fb_img/silver_medal.png')
img_silver = pygame.transform.scale(img_silver, (gold_width, gold_height))
# -------- goodtimp end ----------

# ----- 结束开始-------
begin = pygame.image.load('./fb_img/start.png')
pause = pygame.image.load('./fb_img/pause.png')
over = pygame.image.load('./fb_img/over.png')
ready = pygame.image.load('./fb_img/ready.png')
over = pygame.transform.scale(over,(300,100))
begin_button = {
    "again":False,
    'state':True,
    'px':400,
    'py':450,
    'width':begin.get_rect().width,
    'height':begin.get_rect().height
}
# ----- 结束开始 -----

# 游戏像素鸟参数
red1 = pygame.image.load('./fb_img/red1.png')
red2 = pygame.image.load('./fb_img/red2.png')
red3 = pygame.image.load('./fb_img/red3.png')
blue1 = pygame.image.load('./fb_img/blue1.png')
blue2 = pygame.image.load('./fb_img/blue2.png')
blue3 = pygame.image.load('./fb_img/blue3.png')
yellow1 = pygame.image.load('./fb_img/yellow1.png')
yellow2 = pygame.image.load('./fb_img/yellow2.png')
yellow3 = pygame.image.load('./fb_img/yellow3.png')

bird_red = [red1, red2, red3]
bird_blue = [blue1, blue2, blue3]
bird_yellow = [yellow1, yellow2, yellow3]

# 起始速度
start_speed = -4
# 游戏鸟 1
game_bird1 = {
    'bird': bird_red,
    'width': 34,
    'height': 24,
    'pX': 300,
    'pY': 100,
    'speed': start_speed,
    'acc': 0.2,
    'isdied': False
}
# 游戏鸟 2
game_bird2 = {
    'bird': bird_blue,
    'width': 34,
    'height': 24,
    'pX': 200,
    'pY': 100,
    'speed': start_speed,
    'acc': 0.2,
    'isdied': False
}

# 游戏准备参数
game_run = {
    'isOver': False,
    'begin': False,
    'pipe_current_count': 1,
    'pipe_total_count': 8,
    'current_pass': 1
}
#  ---- yao ----
# 分数
score = 0
# 小鸟需要通过的柱子在列表里的坐标
front = 0
price = 0
scoreimg=[]
for i in range(0,10):
    url = './fb_img/n' + str(i) + '.png'
    scoreimg.append(pygame.image.load(url))

#  ---- yao ---
# 初始化
def game_init():
    global score,gold_list, front  # yao
    pipe_list.clear()
    pipe_list.append({
        'pX': screen_width + space_front_back,
        'pY': random.randint(max_top, min_top),
        'space_down': random.randint(170, 220),
        'speed_up_down': random.uniform(game_run['current_pass']-1, game_run['current_pass'])
    })
    game_bird1['pX'] = 200
    game_bird1['pY'] = 100
    game_bird1['speed'] = start_speed
    game_bird1['isdied'] = False
    game_bird2['pX'] = 300
    game_bird2['pY'] = 100
    game_bird2['speed'] = start_speed
    game_bird2['isdied'] = False
    screen.blit(img_bg, (bg_start, 0))
    game_run['isOver'] = False
    game_run['begin'] = False
    game_run['pipe_current_count'] = 1
    game_run['pipe_total_count'] = 8
    # goodtimp
    gold_list.clear()
    # yao
    score = 0
    front = 0

game_init()

# 画背景
def draw_bg():
    screen.blit(img_bg, (game_bg['start'], 0))
    game_bg['start'] -= game_bg['speed']
    if game_bg['start'] == -300:
        game_bg['start'] = 0

# --------------
#画开始
def draw_begin():
    if game_run['begin'] is False:
        screen.blit(ready, (360, 200))
    if game_run['begin'] is False or game_run['isOver']:
        begin_button['px'] = 400
        begin_button['py'] = 400
    else:
        begin_button['px'] = 20
        begin_button['py'] = screen_height - 80
    screen.blit(begin, (begin_button['px'], begin_button['py']))

#结束
def draw_over():
    screen.blit(over, (300,200))


#暂停
def bt_pause():
    if game_run['begin'] is False:
        bt_image = begin
    elif game_run['begin'] and begin_button['state'] == True:
        bt_image = begin
    elif game_run['begin'] and begin_button['state'] == False:
        bt_image = pause
    screen.blit(bt_image, (begin_button['px'], begin_button['py']))
# ---------------


# 画管道
def draw_pipe():
    global front  # yao
    for pipe in pipe_list:
        # 画上管道
        screen.blit(img_pipe, (pipe['pX'], pipe['pY']))
        # 根据上 对应画下管道
        screen.blit(img_pipe, (pipe['pX'], pipe['pY'] + pipe_height + pipe['space_down']))
        # 移动
        pipe['pX'] -= pipe_speed
        pipe['pY'] += pipe['speed_up_down']
        if pipe['pY'] < max_top or pipe['pY'] > min_top:
            pipe['speed_up_down'] = -pipe['speed_up_down']
        if pipe['pX'] < - space_front_back - pipe_width:
            pipe_list.remove(pipe)
            front -= 1  # yao


# 添加管道
def add_pipe():
    global front
    if len(pipe_list) == 0:
        front = 0
        game_run['pipe_current_count'] = 0
        game_run['current_pass'] += 1
        game_run['pipe_total_count'] = game_run['pipe_total_count']
    if len(pipe_list) == 0 or (len(pipe_list) > 0 and pipe_list[-1]['pX'] == screen_width) and game_run['pipe_current_count'] < game_run['pipe_total_count']:
        pipe_list.append({
            'pX': screen_width+space_front_back,
            'pY': random.randint(max_top, min_top),
            'space_down': random.randint(150, 200),
            'speed_up_down':  random.uniform(game_run['current_pass']-1, game_run['current_pass']-0.5)
        })
        game_run['pipe_current_count'] += 1


# 画鸟
def draw_bird(gbird):
    if gbird['speed'] == 0 or gbird['speed'] == start_speed:
        screen.blit(gbird['bird'][1], (gbird['pX'], gbird['pY']))
    elif gbird['speed'] < 0:
        screen.blit(gbird['bird'][2], (gbird['pX'], gbird['pY']))
    else:
        screen.blit(gbird['bird'][0], (gbird['pX'], gbird['pY']))
    if gbird['pY'] < screen_height:
        gbird['pY'] += gbird['speed']
        gbird['speed'] += gbird['acc']
    if gbird['isdied'] is True and gbird['pX'] > -10-gbird['width']:
        gbird['pX'] -= pipe_speed


# ---- goodtimp start ----
# 画金币
def draw_gold():
    for gold in gold_list:
        # 画上管道
        if gold["score"] > 1:
            screen.blit(img_gold, (gold['pX'], gold['pY']))
        else:
            screen.blit(img_silver, (gold['pX'], gold['pY']))
        # 移动 根据管道速度移动
        gold['pX'] -= pipe_speed
        if gold['pX'] < - space_front_back - gold_width:
            gold_list.remove(gold)


# 添加金币
def add_gold():
    if len(gold_list) >= max_gold_count:
        return
    if len(gold_list) > 0 and gold_list[-1]['pX'] + min_space > screen_width:
        return
    if len(pipe_list) > 0 and ((pipe_list[-1]['pX'] + pipe_width + pipe_width // 2) > screen_width+space_front_back or screen_width+space_front_back > (
            pipe_list[-1]['pX'] + space_front_back - pipe_width // 2)):
        return
    add = random.randint(0, prop)
    if add == 1:
        gold_list.append({
            'pX': screen_width,
            'pY': random.randint(100, screen_height - 100),
            'score': random.randint(1, max_gold_score)
        })
        return


# ---- goodtimp end ----
# 碰撞检测
def crash(gbird):
    if gbird['isdied'] is True:
        return
    if gbird['pY'] <= 0 or gbird['pY'] + gbird['height'] >= screen_height + 8:
        gbird['isdied'] = True
        se_crash.play()
        return
    for pipe in pipe_list:
        if gbird['pX'] + gbird['width'] >= pipe['pX']+5 and gbird['pX'] <= pipe['pX'] + pipe_width-5:
            if gbird['pY'] <= pipe['pY'] + pipe_height-3 or gbird['pY'] + gbird['height'] >= pipe['pY'] + pipe_height + pipe['space_down']+2:
                gbird['isdied'] = True
                se_crash.play()
                return

    # goodtimp
    for gold in gold_list:
        if (gbird['pX'] + gbird['width'] >= gold['pX'] and gbird['pX'] <= gold['pX'] + gold_width) and (
                gbird['pY'] <= gold['pY'] + gold_height and gbird['pY'] + gold_height >= gold['pY']):
            fraction(gold["score"]) # 添加分数
            gold_list.remove(gold)
# ---- yao -----
# 计算分数
def fraction(price):
    gbird = game_bird2
    if game_bird2['isdied'] is True:
        gbird = game_bird1
    global score, front
    score = score+price
    if len(pipe_list) > front:
        if gbird['pX']-34 > pipe_list[front]['pX']:
            score += 1
            front += 1
    n = 0
    for i in str(score):
        screen.blit(scoreimg[int(i)], (screen_width//2+n*23, 550))
        n += 1
# ---- yao -----

# ---------------
def bt_crash(mx,my):
    if  begin_button["px"] <= mx <= (begin_button['px'] + begin_button['width']) and begin_button['py'] <= my <= (begin_button['py'] + begin_button['height']):
            return True
    return False

draw_begin()
# ---------------

def draw_pass():
    if len(pipe_list) > 0 and pipe_list[0]['pX'] > screen_width:
        pass_text = font.render("（W）第" + str(game_run['current_pass']) + '关（U）', True, (0xff, 0xff, 0xff))
        screen.blit(pass_text, (screen_width//2-100, screen_height//2-160))


while True:
    if begin_button['again']:
        game_init()
        begin_button = {
            "again": False,
            'state': True,
            'px': 400,
            'py': 450,
            'width': begin.get_rect().width,
            'height': begin.get_rect().height
        }
        game_run['begin'] = True
    if game_run['isOver'] is False and game_run['begin'] is True and begin_button['state'] is True:
        draw_bg()
        draw_bird(game_bird2)
        draw_bird(game_bird1)
        draw_pipe()
        add_pipe()
        # goodtimp
        draw_gold()
        add_gold()
        fraction(price)
        # yao
        crash(game_bird1)
        crash(game_bird2)

        if game_bird1['isdied'] is True and game_bird2['isdied'] is True:
            game_run['isOver'] = True
            draw_over()
        draw_begin()
    # 画标题
    screen.blit(img_title, (screen_width-190, 20))
    draw_pass()
    # 事件响应
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # 键盘
        if event.type == pygame.KEYDOWN and game_run['isOver'] is False:
            if chr(event.key) == 'w' and game_bird1['isdied'] is False:
                game_bird1['speed'] = start_speed
                se_fly.play()
            if chr(event.key) == 'u' and game_bird2['isdied'] is False:
                game_bird2['speed'] = start_speed
                se_fly.play()
            if chr(event.key) == ' ':
                begin_button['state'] = not begin_button['state']
                bt_pause()
        # 鼠标
        # _________________
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if begin_button['px'] == 20 and bt_crash(mx, my):
                begin_button['state'] = not begin_button['state']
                bt_pause()

        # _________________
    # 鼠标点击
    m1, m2, m3 = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    if m1:
        # _________________
        if bt_crash(mx,my) and begin_button['px'] == 400:
            game_run['begin'] = True
        if bt_crash(mx,my) and begin_button['px'] == 400 and game_run['isOver'] is True:
            begin_button['again'] = True
        # _________________
    # if m3:
    #     game_init()
    pygame.display.update()
