import pygame
import sys #인터프리터 제어
import random 
import math #삼각함수, 소수
from pygame.locals import * #QUIT, MOUSEBUTTONDOWN 대신 * 사용하면 모듈 이름 생략 가능
import time

pygame.init()

width = 15
height = 10
size = 64
num_of_bombs = 20
empty = 0
bomb = 1
opened = 2
key = 3
start = 4
final = 5
heart = 6
mouse = 7
open_count = 0
checked = [[0 for _ in range(width)] for _ in range(height)]
global second, minute

#윈도우 생성 및 사진 불러오기
surface = pygame.display.set_mode((width*size, height*size)) # 윈도우 생성. pygame.display.set_mode() 함수가 pygame.surface 객체를 반환>set_mode() 함수에 알려줌.
ground = pygame.image.load("ground_04.png")
playerR_png = pygame.image.load("player_18.png").convert_alpha()
playerL_png = pygame.image.load("player_21.png").convert_alpha() 
playerU_png = pygame.image.load("player_09.png").convert_alpha()
playerD_png = pygame.image.load("player_06.png").convert_alpha()
flag_png = pygame.image.load("environment_05.png").convert_alpha()
bomb_png = pygame.image.load("crate_23.png")
box_png = pygame.image.load("block_03.png")
key_png = pygame.image.load("environment_12.png")
heart_png = pygame.image.load("heart.png").convert_alpha()
mouse_png = pygame.image.load("environment_08.png").convert_alpha()
final = pygame.image.load("block_01.png")
life1_png = pygame.image.load("life1.png").convert_alpha()
life2_png = pygame.image.load("life2.png").convert_alpha()
life3_png = pygame.image.load("life3.png").convert_alpha()
life4_png = pygame.image.load("life_+1.png").convert_alpha()
startground = pygame.image.load("ground_05.png")
rule_png = pygame.image.load("rule.png").convert_alpha()
clock = pygame.time.Clock() #게임 루프의 주기 결정. clock.tick(60)에 사용됨
bgm = pygame.mixer.Sound("Digital_Voyage.wav")
bgm_game = pygame.mixer.Sound("Seven_Twenty.wav")
wrong = pygame.mixer.Sound("wrong.wav")

# 주변 지뢰의 개수 반환
def num_of_bomb(field, x_pos, y_pos):
    count = 0	# 지뢰 개수의 초기값은 0
    for yoffset in range(-1,2): 
        for xoffset in range(-1,2):
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset) 
            if 0 <= xpos < width and 0 <= ypos < height and field[ypos][xpos] == bomb:
                count += 1
    return count # 지뢰 개수 반환

# 타일 오픈
def open_tile(field, x_pos, y_pos):
    global open_count # 전역변수
    checked = [[0 for _ in range(width)] for _ in range(height)]
    if checked[y_pos][x_pos] == True:
        return

    checked[y_pos][x_pos] = True
    if num_of_bomb(field, x_pos, y_pos) == 0:
        for yoffset in range(-1,2):
            for xoffset in range(-1,2):
                xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
                if 0 <= xpos < width and 0 <= ypos < height and field[ypos][xpos] == empty:
                    field[ypos][xpos] = opened # 주위 좌표(xpos, ypos) empty면 open
                    open_count += 1
                    count = num_of_bomb(field, xpos, ypos)
                    if count == 0 and not (xpos == x_pos and ypos == y_pos):
                        open_tile(field, xpos, ypos)
    else:
        field[y_pos][x_pos] = opened

# 게임 진행
def runGame(minute, second):
    global surface, player_png
    global score
    global A, B
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    list1 = [64,64]
    playershow = 3
    life = 3
    score = 0
    result = 0
    minutes = 0
    seconds = 0
    A = 0
    B = 0
    c = 0

    field = [[empty for xpos in range(width+1)] for ypos in range(height+1)]
    flag = [[empty for xpos in range(width+1)] for ypos in range(height+1)] # 깃발 표시 하기 위한 배열

    message_clear = largefont.render("GAME CLEAR", True, (0,0,0)) # 게임성공 문구
    message_over = largefont.render("GAME OVER!", True, (0,0,0)) # 게임종료 문구
    message_rect = message_over.get_rect()
    message_rect.center = (width*size/2, height*size/2) #성공/종료 문구 위치

    message_new = smallfont.render("PRESS F5 TO RESTART", True, (0,0,0))
    message_newre = message_new.get_rect()
    message_newre.center = (width*size/1.95, height*size/1.7)

    game_over = False
    game_clear = False
    getkey = False
    getheart = False
    getmouse = False
    mouse_range = False
    run = False

    bgm_game.play(-1)
    
    #출발지, 목적지 / 출발지 주변 칸에 지뢰X
    for y in range(-1,2):
        for x in range(-1,2):
            field[1+y][1+x] = start
    field[8][13] = final

    #폭탄 설치
    count = 0
    while count < num_of_bombs:
        xpos, ypos = random.randint(0, width-1), random.randrange(0, height-1)
        if field[ypos][xpos] == empty:
            field[ypos][xpos] = bomb
            count += 1
    #열쇠 설치
    countkey = 0
    while countkey < 1:
        xpos, ypos = random.randint(0, width-1), random.randrange(0, height-1)
        if field[ypos][xpos] == empty:
            field[ypos][xpos] = key
            countkey += 1
    #하트 설치
    countheart = 0
    while countheart < 1:
        xpos, ypos = random.randint(0, width-1), random.randrange(0, height-1)
        if field[ypos][xpos] == empty:
            field[ypos][xpos] = heart
            countheart += 1
    #마우스 아이템 설치
    countmouse = 0
    while countmouse < 1:
        xpos, ypos = random.randint(0, width-1), random.randrange(0, height-1)
        if field[ypos][xpos] == empty:
            field[ypos][xpos] = mouse
            countmouse += 1

    #캐릭터 이동
    while True:
        surface.fill((0,0,0))
        ticks = pygame.time.get_ticks()
        for x in range(width+1) :       
            for y in range(height+1):
                surface.blit(ground, (x*size, y*size))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                xpos = list1[0]//size
                ypos = list1[1]//size
                if event.key == pygame.K_UP:
                    if field[ypos-1][xpos] == opened or field[ypos-1][xpos] == start:
                        list1[1] -= 64
                    else:
                        list1[1] += 0
                    playershow = 0
                elif event.key == pygame.K_DOWN:
                    if field[ypos+1][xpos] == opened or field[ypos+1][xpos] == start:
                        list1[1] += 64
                    else:
                        list1[1] += 0
                    playershow = 1
                elif event.key == pygame.K_LEFT:
                    if field[ypos][xpos-1] == opened or field[ypos][xpos-1] == start:
                        list1[0] -= 64
                    else:
                        list1[0] += 0
                    playershow = 2
                elif event.key == pygame.K_RIGHT:
                    if field[ypos][xpos+1] == opened or field[ypos][xpos+1] == start:
                        list1[0] += 64
                    else:
                        list1[0] += 0
                    playershow = 3

                elif event.key == pygame.K_F5:
                    bgm_game.stop()
                    initGame_new()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    list1[1] += 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    list1[0] += 0

            # f로 깃발 표시, 1인 경우 표시
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    xpos = list1[0]//size
                    ypos = list1[1]//size

                    if playershow == 0: # 위쪽
                        ypos -= 1
                    elif playershow == 1: # 아래쪽
                        ypos += 1
                    elif playershow == 2: # 왼쪽
                        xpos -= 1
                    elif playershow == 3: # 오른쪽
                        xpos += 1
                        
                    if flag[ypos][xpos] == 1:   # 깃발이 있는 곳에서 f 누르면 깃발 삭제
                        flag[ypos][xpos] = 0
                    else:
                        flag[ypos][xpos] = 1

            # 마우스 오른쪽클릭으로 깃발 표시
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # event.button==3: 마우스 오른쪽
                xpos, ypos = math.floor(event.pos[0]/size), math.floor(event.pos[1]/size)

                if flag[ypos][xpos] == 1:
                    flag[ypos][xpos] = 0
                else:
                    flag[ypos][xpos] = 1

            # 마우스 왼쪽클릭하면 블럭 열림
            if game_over == False:
                if event.type == MOUSEBUTTONDOWN and event.button == 1: # event.button==1: 마우스 왼쪽
                    xpos, ypos = math.floor(event.pos[0]/size), math.floor(event.pos[1]/size)
                    mouse_range = False
                            
                    for y in range(-1,1):
                            if field[ypos+y][xpos] == opened or field[ypos+y][xpos] == start:
                                mouse_range = True
                    for x in range(-1,1):
                            if field[ypos][xpos+x] == opened or field[ypos][xpos+x] == start:
                                mouse_range = True

                    if mouse_range == True :            
                        if field[ypos][xpos] == bomb:
                            life = life-1
                            wrong.play()
                            score -= 100
                            if(life == 0):
                                game_over = True
                        elif field[ypos][xpos] == final:
                            if getkey == True:
                                game_clear = True
                        else:
                            if field[ypos][xpos] == key and flag[ypos][xpos] != 1:
                                getkey = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)

                            if field[ypos][xpos] == heart and flag[ypos][xpos] != 1:
                                getheart = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)
                                life += 1
                                score += 200

                            if field[ypos][xpos] == mouse and flag[ypos][xpos] != 1:
                                getmouse = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)
                                score += 200

                            if flag[ypos][xpos] != 1:
                                open_tile(field, xpos, ypos)

                    elif mouse_range == False and getmouse == True:            
                        if field[ypos][xpos] == bomb:
                            life = life-1
                            wrong.play()
                            score -= 100
                            if life == 0:
                                game_over = True

                        elif field[ypos][xpos] == final:
                            if getkey == True:
                                game_clear = True

                        else:
                            if field[ypos][xpos] == key and flag[ypos][xpos] != 1:
                                getkey = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)

                            if field[ypos][xpos] == heart and flag[ypos][xpos] != 1:
                                getheart = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)
                                life += 1
                                score += 200

                            if field[ypos][xpos] == mouse and flag[ypos][xpos] != 1:
                                getmouse = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)
                                score += 200

                            if flag[ypos][xpos] != 1:
                                open_tile(field, xpos, ypos)

                        if field[ypos][xpos] == final:
                            if getkey == False:
                                getmouse = True
                        else:
                            getmouse = False

                # 스페이스 바 누르면 앞에 있는 블럭 열림
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        xpos = list1[0]//size
                        ypos = list1[1]//size

                        if playershow == 0:
                            ypos -= 1
                        elif playershow == 1:
                            ypos += 1
                        elif playershow == 2:
                            xpos -= 1
                        elif playershow == 3:
                            xpos += 1

                        if field[ypos][xpos] == bomb:
                            if flag[ypos][xpos] != 1:
                                life = life - 1
                                wrong.play()
                                score -= 100
                                if(life==0):
                                    game_over = True
                        elif field[ypos][xpos] == final:
                            if getkey == True:
                                game_clear = True
                        else:                             
                            if field[ypos][xpos] == key and flag[ypos][xpos] != 1:
                                getkey = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)

                            if field[ypos][xpos] == heart and flag[ypos][xpos] != 1:
                                getheart = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)
                                life = life + 1
                                score += 200

                            if field[ypos][xpos] == mouse and flag[ypos][xpos] != 1:
                                getmouse = True
                                field[ypos][xpos] = empty
                                open_tile(field, xpos, ypos)
                                score += 200

                            if flag[ypos][xpos] != 1:
                                open_tile(field, xpos, ypos)                                    

        for ypos in range(height):
            for xpos in range(width):
                tile = field[ypos][xpos]

                # 아무것도 없으면 일반 블럭
                if tile == empty:
                    surface.blit(box_png, (xpos*size,ypos*size)) #블럭 위를 상자로 덮기
                # 폭탄 있으면 폭탄 블럭
                elif tile == bomb:
                    surface.blit(bomb_png, (xpos*size,ypos*size))
                    surface.blit(box_png, (xpos*size,ypos*size)) #블럭 위를 상자로 덮기
                # 열쇠 있으면 열쇠 블럭
                elif tile == key:
                    surface.blit(box_png, (xpos*size,ypos*size))
                    surface.blit(key_png, (xpos*size,ypos*size))
                # 목적지는 목적지 블럭
                elif tile == final:
                    surface.blit(final, (xpos*size,ypos*size))
                    if game_clear == True:
                        surface.blit(final, (xpos*size,ypos*size))
                        surface.blit(key_png, (xpos*size,ypos*size))
                # 열려있으면 숫자 출력
                elif tile == opened:
                    count = num_of_bomb(field, xpos, ypos)                  
                    if count > 0:
                        num_image = smallfont.render("{}".format(count), True, (255, 255, 0))
                        surface.blit(num_image, (xpos*size + 25, ypos*size + 20))
                # 하트 있으면 하트 블럭
                elif tile == heart:
                    surface.blit(box_png, (xpos*size,ypos*size))
                    surface.blit(heart_png, (xpos*size + 16, ypos*size + 16))
                # 마우스 아이템 있으면 마우스 블럭
                elif tile == mouse:
                    surface.blit(box_png, (xpos*size,ypos*size))
                    surface.blit(mouse_png, (xpos*size,ypos*size))

        # 게임오버
        if game_over == True:
            for ypos in range(height):
                for xpos in range(width):
                    tile = field[ypos][xpos]
                    if tile == bomb:
                        surface.blit(bomb_png, (xpos*size,ypos*size))
                        
            surface.blit(message_over, message_rect.topleft)
            surface.blit(message_new,message_newre.topleft)

            if A==0 and B==0:
                seconds = int(ticks/1000 % 60)
                A += 1
                minutes = int(ticks/60000 % 24)
                B += 1

            bgm_game.stop()
            message_time = smallfont.render("PLAY TIME = " +  str(abs(minutes-minute)) + ":" + str(abs(seconds-second)), True, (0,0,0))            
            message_retime = message_new.get_rect()
            message_retime.center = (width*size/1.85, height*size/1.4)

            message_score = smallfont.render("SCORE = {}".format(score), True, (0,0,0))
            message_rescore = message_score.get_rect()
            message_rescore.center = (width*size/2, height*size/1.3)
            
            surface.blit(message_time, message_retime.topleft)
            surface.blit(message_score, message_rescore.topleft)

        # 게임클리어 
        elif getkey and game_clear:
            surface.blit(message_clear, message_rect.topleft)
            surface.blit(message_new,message_newre.topleft)
            
            while True:
                if A == 0:
                    seconds = int(ticks/1000 % 60)
                    A += 1
                if B == 0:
                    minutes = int(ticks/60000 % 24)
                    B += 1
                if A == 1 and B == 1:
                    break

            if c == 0:
                if minutes-minute == 0:
                    score = score+(60-seconds+second)*500+5000
                    c += 1
                elif minutes-minute == 1:
                    score = score+(60-seconds+second)*450+4000
                    c += 1
                elif minutes-minute == 2:
                    score = score+(60-seconds+second)*400+3000
                    c += 1
                elif minutes-minute == 3:
                    score = score+(60-seconds+second)*350+2000
                    c += 1
                elif minutes-minute == 4:
                    score = score+(60-seconds+second)*300+1000
                    c += 1
                elif minutes-minute == 5:
                    score = score+(60-seconds+second)*250+500
                    c += 1
                else:
                    score = score+(60-seconds+second)*200+250
                    c += 1

            bgm_game.stop()
            message_time = smallfont.render("PLAY TIME = " +  str(abs(minutes-minute)) + ":" + str(abs(seconds-second)), True, (0,0,0))            
            message_retime = message_new.get_rect()
            message_retime.center = (width*size/1.85, height*size/1.4)
          
            message_score = smallfont.render("SCORE = {}".format(score), True, (0,0,0))
            message_rescore = message_score.get_rect()
            message_rescore.center = (width*size/2, height*size/1.3)

            surface.blit(message_time, message_retime.topleft)
            surface.blit(message_score, message_rescore.topleft)
            
        clock.tick(60)
            
        # 깃발 표시한 블럭이면 깃발 이미지 추가
        for ypos in range(height):
            for xpos in range(width):
                if flag[ypos][xpos] == 1 and field[ypos][xpos] != opened:
                    surface.blit(flag_png, (xpos*size,ypos*size))
                

        #키방향에 따른 캐릭터 표면 출력
        if playershow == 0: # 위쪽
            surface.blit(playerU_png, list1)           
        elif playershow == 1: # 아래쪽
            surface.blit(playerD_png, list1)
        elif playershow == 2: # 왼쪽
            surface.blit(playerL_png, list1)
        elif playershow == 3: # 오른쪽
            surface.blit(playerR_png, list1)
                
        #아이템 얻으면 아이템 이미지 오른쪽 상단에 뜨도록
        if getkey == True:
            key_png_big = pygame.transform.scale(key_png, (80,80))
            surface.blit(key_png_big, (880, 0))
        if getmouse == True:
            mouse_png_big = pygame.transform.scale(mouse_png, (80,80))
            surface.blit(mouse_png_big, (880, 50))

        #하트 개수 왼쪽 상단에 뜨도록
        if life == 4:
            surface.blit(life4_png, (20, 20))
        elif life == 3:
            surface.blit(life3_png, (20, 20))
        elif life == 2:
            surface.blit(life2_png, (20, 20))
        elif life == 1:
            surface.blit(life1_png, (20, 20))
        
        pygame.display.flip()

# 처음 실행
def initGame():
    pygame.display.set_caption("minesweeper")
    surface.fill((0,0,0))
    pygame.init() #파이게임 라이브러리 초기화
    startGame()

# F5키를 눌러 새로 게임 새로 시작
def initGame_new():
    ticks=pygame.time.get_ticks()
    A=-1
    B=-1
    pygame.display.set_caption("minesweeper")
    surface.fill((0,0,0))
    pygame.init() #파이게임 라이브러리 초기화
    if A == -1 and B == -1:
        second = int(ticks/1000 % 60)
        A += 1
        minute = int(ticks/60000 % 24)
        B += 1
        if A == 0 and B == 0:
            runGame(minute, second)

# 처음 화면
def startGame():
    largefont = pygame.font.SysFont(None, 72)
    smallfont=pygame.font.SysFont(None, 36)
    a = False
    b = False
    A = -1
    B = -1
    for x in range(width+1) :
        for y in range(height+1):
            surface.blit(startground, (x*size, y*size))

    message_name = largefont.render("MINESWEEPER", True, (0,0,0))
    message_stna = message_name.get_rect()
    message_stna.center = (width*size/2, height*size/2.2)

    message_start = smallfont.render("START GAME : PRESS F5", True, (0,0,0))
    message_stre = message_start.get_rect()
    message_stre.center = (width*size/2, height*size/1.7)

    message_rule = smallfont.render("GAME RULE : PRESS SPACEBAR", True, (0,0,0))
    message_stru = message_rule.get_rect()
    message_stru.center = (width*size/2, height*size/1.5)

    surface.blit(message_name, message_stna.topleft)
    surface.blit(message_start, message_stre.topleft)
    surface.blit(message_rule, message_stru.topleft)
    pygame.display.flip()
    bgm.play(-1)
    
    while True :
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    a = True
                elif event.key == pygame.K_SPACE:
                    b = True

        if a == True:
            if A==-1 and B==-1:
                second = int(ticks/1000 % 60)
                A += 1
                minute = int(ticks/60000 % 24)
                B += 1
                if A == 0 and B == 0:
                    bgm.stop()
                    runGame(minute, second)

        if b == True:
            for x in range(width+1) :
                for y in range(height+1):
                    surface.blit(startground, (x*size, y*size))
            surface.blit(rule_png,(100,100))
            
        pygame.display.flip()

initGame()
