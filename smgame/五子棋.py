import pygame
import random

pygame.mixer.init()
pygame.init()
screen_with = 700
screen_height = 720
screen = pygame.display.set_mode((screen_with, screen_height))
bg = pygame.image.load('./imgs/qiBg.jpg')
mu2 = pygame.mixer.Sound('./music/music2.wav')
font = pygame.font.SysFont("", 16)
font1 = pygame.font.Font("./fonts/msyhbd.ttf", 66)
font2 = pygame.font.Font("./fonts/msyhbd.ttf", 12)
font3 = pygame.font.Font("./fonts/msyhbd.ttf", 16)
baiqi = pygame.image.load('./imgs/baiqi.png')
heiqi = pygame.image.load('./imgs/heiqi.png')
restart = pygame.image.load('./imgs/restart1.png')
restart2 = pygame.image.load('./imgs/restart2.png')
restart = pygame.transform.scale(restart, (restart.get_rect().width*2, restart.get_rect().height//3*2))
restart2 = pygame.transform.scale(restart2, (restart2.get_rect().width*2, restart2.get_rect().height//3*2))

size = 42
start = 57
qi_list = []
player_pos = []
pc_pos = []
# 5点
dian_list = [[3, 3], [11, 3], [7, 7], [3, 11], [11, 11]]
# 方向
fangxiang = [[0, -1], [-1, -1], [-1, 0], [-1, 1]]
restat_text = font3.render("重新开始", True, (0xff, 0x00, 0xff))
# 棋子数量
count = 0
newBtn = font1.render("右键重新开始", True, (0x00, 0xff, 0xff))
bai = font1.render("游戏结束 " + '白赢了', True, (0xff, 0xff, 0xff))
hei = font1.render("游戏结束 " + '黑赢了', True, (0x00, 0xaa, 0xff))
isclick = 1
result = 0
baiwin = 0
heiwin = 0
# 先手颜色( 0 白棋 1 黑棋)
first = 1
# pc先True 玩家先False
ishei = True

# 初始化
def init():
    screen.blit(bg, (0, 0))
    player_pos.clear()
    pc_pos.clear()
    qi_list.clear()
    for i in range(15):
        item = []
        pygame.draw.line(screen, (0xff, 0xff, 0xff), (size * i + start, start), (size * i + start, size * 14 + start),2)
        num = font2.render(str(i+1), True, (0xff, 0xff, 0xff))
        screen.blit(num, (start-25, i*size+start-10))
        for j in range(15):
            if i == 0:
                num = font2.render(chr(ord('A')+j), True, (0xff, 0xff, 0xff))
                screen.blit(num, (j * size + start - 5, start - 25))
            pygame.draw.line(screen, (0xff, 0xff, 0xff), (start, size * j + start),(size * 14 + start, size * j + start), 2)
            qi = {
                'img': baiqi,
                'pX': size * j + start - 16,
                'pY': size * i + start - 16,
                'isHave': 0,
                'num': 0,
                'color': (0x00, 0x00, 0x00)
            }
            item.append(qi)
        qi_list.append(item)
    for dian in dian_list:
        pygame.draw.rect(screen, (0xff, 0xff, 0xff), (size * dian[0] + start - 3, size * dian[1] + start - 3, 8, 8), 6)
    screen.blit(restart,
                (screen_with // 2 - restart.get_rect().width // 2, screen_height - restart.get_rect().height - 10))
    screen.blit(restat_text, (screen_with // 2 - restat_text.get_rect().width // 2, screen_height - 37))
init()

# 判断最佳落点（次数最大）(只可惜当前只能同数量判断  无法综合判断！！！)
def addmax(rai_list,pc_list, mx,pc):
    rai_list.append(mx)
    if rai_list.count(mx) >= pc:
        pc_list[0] = mx
        pc = rai_list.count(mx)
    return pc

# 中间空一个的情况，有无意义
def can_kong(cx,cy,fx, baiorhei):
    can_num = 0
    isqian = True
    ishou = True
    for cc in range(5):
        if cc > 0:
            if isqian == True:
                if 0 <= cx - fx[0] * cc < len(qi_list) and 0 <= cy - fx[1] * cc < len(qi_list) and (qi_list[cx - fx[0] * cc][cy - fx[1] * cc]['num'] % 2 == baiorhei or qi_list[cx - fx[0] * cc][cy - fx[1] * cc]['isHave'] == 0):
                    can_num += 1
                else:
                    isqian = False
            if ishou == True:
                if 0 <= cx + fx[0] * cc < len(qi_list) and 0 <= cy + fx[1] * cc < len(qi_list) and (qi_list[cx + fx[0] * cc][cy + fx[1] * cc]['num'] % 2 == baiorhei or qi_list[cx + fx[0] * cc][cy + fx[1] * cc]['isHave'] == 0):
                    can_num += 1
                else:
                    ishou = False
            if can_num >= 4:
                return True
    return False

# 查询中间空一个的情况
def aikong(kong, pos_list):
    rai_list = []
    pc = 0
    pc_list = [(0,0)]
    for item in pos_list:
        wi, wj = item
        for fx in fangxiang:
            cc = 0
            for zz in range(kong-1):
                if 0<=wi+(fx[0]*(zz+1))<len(qi_list) and 0<=wj+(fx[1]*(zz+1))<len(qi_list) and (wi+(fx[0]*(zz+1)),wj+(fx[1]*(zz+1))) in pos_list:
                    cc += 1
                else:
                    break
            if cc == kong-1:
                if 0 <= wi - fx[0] < len(qi_list) and 0 <= wj - fx[1] < len(qi_list) and qi_list[wi - fx[0]][wj - fx[1]]['isHave'] == 0 and 0 <= wi - 2*fx[0] < len(qi_list) and 0 <= wj - 2*fx[1] < len(qi_list) and (wi - 2*fx[0], wj - 2*fx[1]) in pos_list:
                    if can_kong(wi-fx[0], wj-fx[1],fx,(qi_list[wi][wj]["num"]%2)):
                        pc = addmax(rai_list,pc_list,(wi-fx[0], wj-fx[1]),pc)
                if 0 <= wi + kong*fx[0] < len(qi_list) and 0 <= wj + kong*fx[1] < len(qi_list) and qi_list[wi + kong*fx[0]][wj + kong*fx[1]]['isHave'] == 0 and 0 <= wi + kong * fx[0] + fx[0] < len(qi_list) and 0 <= wj + kong * fx[1] +fx[1] < len(qi_list) and (wi + kong * fx[0] + fx[0], wj + kong * fx[1] +fx[1]) in pos_list:
                    if can_kong(wi + kong*fx[0], wj + kong*fx[1], fx,(qi_list[wi][wj]["num"]%2)):
                        pc = addmax(rai_list, pc_list, (wi + kong*fx[0], wj + kong*fx[1]), pc)
    if pc == 0:
        return []
    else:
        return pc_list

# 综合二三判断
def allbtu(pos_list):
    line_list = []
    line_list.extend(aihuo(3, pos_list, True))
    line_list.extend(aihuo(2, pos_list, True))
    count = 1
    pc_list = [(0,0)]
    for item in line_list:
        if line_list.count(item) > count:
            pc_list[0] = item
            count = line_list.count(item)
    # print(count)
    # print(pc_list)
    if count > 1:
        return pc_list
    else:
        return []

# 查询活几 ||冲4
def aihuo(num, pos_list, dang):
    rai_list = []
    pc = 0
    pc_list = [(0,0)]
    for item in pos_list:
        wi, wj = item
        for fx in fangxiang:
            cc = 0
            for zz in range(num-1):
                if 0<=wi+(fx[0]*(zz+1))<len(qi_list) and 0<=wj+(fx[1]*(zz+1))<len(qi_list) and (wi+(fx[0]*(zz+1)),wj+(fx[1]*(zz+1))) in pos_list:
                    cc += 1
                else:
                    break
            if cc == num-1:
                if num == 4 or num == 1 or dang == True:
                    if 0 <= wi - fx[0] < len(qi_list) and 0 <= wj - fx[1] < len(qi_list) and qi_list[wi - fx[0]][wj - fx[1]]['isHave'] == 0:
                        pc = addmax(rai_list, pc_list, (wi - fx[0], wj - fx[1]), pc)
                    if 0 <= wi + num * fx[0] < len(qi_list) and 0 <= wj + num * fx[1] < len(qi_list) and qi_list[wi + num * fx[0]][wj + num * fx[1]]['isHave'] == 0:
                        pc = addmax(rai_list, pc_list, (wi + num * fx[0], wj + num * fx[1]), pc)
                else:
                    if 0 <= wi - fx[0] < len(qi_list) and 0 <= wj - fx[1] < len(qi_list) and qi_list[wi - fx[0]][wj - fx[1]]['isHave'] == 0 and \
                            0 <= wi + num*fx[0] < len(qi_list) and 0 <= wj + num*fx[1] < len(qi_list) and qi_list[wi + num*fx[0]][wj + num*fx[1]]['isHave'] == 0:
                        if can_kong(wi - fx[0], wj - fx[1], fx, (qi_list[wi][wj]["num"] % 2)) and 0 <= wi - fx[0]*2 < len(qi_list) and 0 <= wj - fx[1]*2 < len(qi_list) and qi_list[wi - fx[0]*2][wj - fx[1]*2]['isHave'] == 0:
                            pc = addmax(rai_list, pc_list, (wi-fx[0], wj-fx[1]), pc)
                        if can_kong(wi + num * fx[0], wj + num * fx[1], fx, (qi_list[wi][wj]["num"] % 2)) and 0 <= wi + (num+1)*fx[0] < len(qi_list) and 0 <= wj + (num+1)*fx[1] < len(qi_list) and qi_list[wi + (num+1)*fx[0]][wj + (num+1)*fx[1]]['isHave'] == 0:
                            pc = addmax(rai_list, pc_list, (wi + num*fx[0], wj + num*fx[1]), pc)
    if num == 1 or dang == True:
        return rai_list
    elif pc == 0:
        return []
    else:
        return pc_list

# 判断连线个数
def line5(m, n, mx, nx):
    baiorhei = qi_list[m][n]['num'] % 2
    count = 0
    for cc in range(5):
        if m+cc*mx < 0 or m+cc*mx > 14 or n + cc*nx < 0 or n + cc*nx > 14:
            break
        elif qi_list[m+cc*mx][n + cc*nx]['isHave'] == 0 or qi_list[m+cc*mx][n + cc*nx]['num'] % 2 != baiorhei:
            break
        else:
            count += 1
    return count

# 存在5子连线
def haveline5(i, j):
    for fx in fangxiang:
        # 因为自己会算两次 故大于5（无需等于）
        if (line5(i, j, fx[0], fx[1])+line5(i, j, -fx[0], -fx[1])) > 5:
            if qi_list[i][j]['num'] % 2 is first:
                return 2
            else:
                return 1
    return 0

# 赢的次数++ 显示
def wincount():
    baileft = font2.render('白赢次数: ' + str(baiwin), True, (0xff, 0xff, 0xff))
    heileft = font2.render('黑赢次数: ' + str(heiwin), True, (0x00, 0xaa, 0xff))
    screen.blit(baileft, (15, 10))
    screen.blit(heileft, (590, 10))
wincount()

# 游戏落子 下棋
def luozi(i, j, cnum):
    qi_list[i][j]['isHave'] = 1
    qi_list[i][j]['num'] = cnum
    if cnum % 2 is first:
        qi_list[i][j]['img'] = heiqi
        qi_list[i][j]['color'] = (0xff, 0xff, 0xff)
    else:
        qi_list[i][j]['img'] = baiqi
        qi_list[i][j]['color'] = (0x00, 0x00, 0x00)
    mu2.play()
    return haveline5(i, j)

while True:
    # 每次落子后才去渲染棋子和结果（一次），节省内存
    if isclick == 1:
        # 判断是否结束
        if result > 0:
            if result == 1:
                screen.blit(bai, (120, 250))
                baiwin += 1
            elif result == 2:
                screen.blit(hei, (120, 250))
                heiwin += 1
            screen.blit(newBtn, (140, 350))
        # 画棋子
        for item in qi_list:
            for value in item:
                if value['isHave'] == 1:
                    screen.blit(value['img'], (value['pX'], value['pY']))
                    qi = font.render(str(value['num']), True, value['color'])
                    m_left = 9
                    if value['num'] < 10:
                        m_left = 12
                    elif value['num'] > 99:
                        m_left = 5
                    screen.blit(qi, (value['pX']+m_left, value['pY']+11))
        isclick = 0
    # pc下棋
    if ishei is True and result == 0:
        count += 1
        for hh in range(4):
            if hh == 2:
                all = allbtu(pc_pos)
                if len(all) > 0:
                    chx, chy = random.choice(all)
                    break
                all = allbtu(player_pos)
                if len(all) > 0:
                    chx, chy = random.choice(all)
                    break
            if hh < 3:
                all = aikong(3 - hh, pc_pos)
                if len(all) > 0:
                    chx, chy = random.choice(all)
                    break
                all = aikong(3 - hh, player_pos)
                if len(all) > 0:
                    chx, chy = random.choice(all)
                    break
            all = aihuo(4-hh, pc_pos,False)
            if len(all) > 0:
                chx, chy = random.choice(all)
                break
            all = aihuo(4-hh, player_pos,False)
            if len(all) > 0:
                while True:
                    chx, chy = random.choice(all)
                    if qi_list[chx][chy]['isHave'] == 0:
                        break
                break
        if len(player_pos) == 0:
            chx = random.randint(3, 11)
            chy = random.randint(3, 11)
        result = luozi(chx, chy, count)
        pc_pos.append((chx, chy))
        isclick = 1
        ishei = False
    # 事件响应
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dx, dy = event.pos
            if result == 0:
                for i, value in enumerate(qi_list):
                    for j, item in enumerate(value):
                        if (qi_list[i][j]['isHave']) == 0:
                            if qi_list[i][j]['pX'] <= dx <= qi_list[i][j]['pX'] + 32 and dy >= qi_list[i][j]['pY'] <= dy <= qi_list[i][j]['pY'] + 32:
                                count += 1
                                result = luozi(i, j, count)
                                player_pos.append((i, j))
                                ishei = True
                                break
                isclick = 1
    # 鼠标点击 （重行开始）
    m1, m2, m3 = pygame.mouse.get_pressed()
    mx,my = pygame.mouse.get_pos()
    if m3 or (m1 and screen_with // 2 - restart.get_rect().width // 2 < mx < screen_with // 2 + restart.get_rect().width // 2 and \
            screen_height - restart.get_rect().height - 10 < my < screen_height - 10):
        screen.blit(restart2, (screen_with // 2 - restart.get_rect().width // 2, screen_height - restart.get_rect().height - 10))
        init()
        ishei = True
        result = 0
        count = 0
        isclick = 1
        wincount()
    else:
        screen.blit(restart,(screen_with // 2 - restart.get_rect().width // 2, screen_height - restart.get_rect().height - 10))
    screen.blit(restat_text, (screen_with // 2 - restat_text.get_rect().width // 2, screen_height - 37))
    pygame.display.update()
