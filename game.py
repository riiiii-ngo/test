import pygame
from pygame.locals import *
import sys
import random

pxs = 0
pys = 0

#障害物
BLOCK_MAX = 20
block_n = 0
block_x = [0]*BLOCK_MAX
block_y = [0]*BLOCK_MAX
block_height = [0]*BLOCK_MAX
block_width = [0]*BLOCK_MAX

#プレイヤーの弾
PBOMB_MAX = 10
pbomb_n = 0
pbomb_x = [400]*PBOMB_MAX
pbomb_y = [300]*PBOMB_MAX
pbomb_xx = [0]*PBOMB_MAX
pbomb_yy = [0]*PBOMB_MAX
pbomb_s = [0]*PBOMB_MAX
pbomb_flg = [False]*PBOMB_MAX
pbomb_px = [0]*PBOMB_MAX
pbomb_py = [0]*PBOMB_MAX
pbomb_bx = [0]*PBOMB_MAX
pbomb_by = [0]*PBOMB_MAX
pbomb_count = 0

#敵
ENEMY_MAX = 30
enemy_n = 0
enemy_x = [400]*ENEMY_MAX
enemy_y = [300]*ENEMY_MAX
enemy_xx = [0]*ENEMY_MAX
enemy_yy = [0]*ENEMY_MAX
enemy_ex = [0]*ENEMY_MAX
enemy_ey = [0]*ENEMY_MAX

#障害物の処理
def setblock(screen):
    global block_n,block_x,block_y,block_height,block_width
    pygame.draw.rect(screen,(0,255,0),Rect(block_x[block_n] - pxs,block_y[block_n] - pys,block_width[block_n],block_height[block_n]),5)

#弾の処理
def bomb(screen):
    global pbomb_n,pbomb_x,pbomb_y,pbomb_s
    pbomb_yy[pbomb_n] += pbomb_s[pbomb_n]
    pbomb_y[pbomb_n] += pbomb_s[pbomb_n] -pbomb_by[pbomb_n]
    if pbomb_flg[pbomb_n] == False:
        pygame.draw.circle(screen,(10,10,10),(pbomb_x[pbomb_n],pbomb_y[pbomb_n]),5)
    else:
        pygame.draw.circle(screen,(10,10,10),(pbomb_x[pbomb_n] - pbomb_bx[pbomb_n],pbomb_y[pbomb_n] - pbomb_by[pbomb_n]),5)

#障害物の当たり判定
def hit(d,a,s,w):
    global pxs,pys,block_n,block_x,block_y,block_height,block_width
    for block_n in range(BLOCK_MAX):
        if block_x[block_n] - pxs < d and block_x[block_n] + block_width[block_n] - pxs > a and block_y[block_n] - pys < s and block_y[block_n] + block_height[block_n] - pys > w:
            return True

#壁の当たり判定
def wall(x,y,a):
    if (y - a < -600) or (x - a < -800) or (y + a > 1200) or (x + a > 1600):
        return True

#敵の処理
def setenemy(screen):
    global enemy_n,enemy_x,enemy_y,enemy_xx,enemy_yy
    enemy_x[enemy_n] += enemy_xx[enemy_n]
    enemy_y[enemy_n] += enemy_yy[enemy_n]
    pygame.draw.circle(screen,(255,0,0),(enemy_x[enemy_n] - pxs,enemy_y[enemy_n] - pys),30)

#敵の移動
def moveenemy():
    enemy_xx[enemy_n] = random.randint(-1,1)
    enemy_yy[enemy_n] = random.randint(-1,1)

def main():
    global pxs,pys,block_n,block_x,block_y,block_height,block_width,pbomb_n,pbomb_x,pbomb_y,pbomb_s,pbomb_count,enemy_n
    pygame.init()                                 # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))  # 800*600の画面

    count = 0

    #プレイヤーの座標
    px = 400
    py = 300

    #ブロックの座標
    for block_n in range(BLOCK_MAX):
        #プレイヤーの初期位置に配置させないための処理
        while True:
            block_x[block_n] = random.randint(-395,1845)
            if 450 > block_x[block_n] and block_x[block_n] > 350:
                block_x[block_n] = random.randint(-395,1845)
            else:
                break
        while True:
            block_y[block_n] = random.randint(-295,1345)
            if 350 > block_y[block_n] and block_y[block_n] >  250:
                block_y[block_n] = random.randint(-295,1345)
            else:
                break
        
        #障害物の大きさ
        block_height[block_n] = random.randint(100,200)
        block_width[block_n] = random.randint(100,200)

    while True:
        screen.fill((255,255,255))

        #壁の表示
        pygame.draw.rect(screen,(255,0,0),Rect(-400 - pxs,-300 - pys,2400,1800),5)

        #障害物の表示
        for block_n in range(BLOCK_MAX):
            setblock(screen)

        #敵の表示
        for enemy_n in range(ENEMY_MAX):
            setenemy(screen)

        #プレイヤーの表示
        pygame.draw.circle(screen,(10,10,10),(px,py),30) 

        #敵の移動
        for enemy_n in range(ENEMY_MAX):
            if count % 500 == 0:
                moveenemy()

        #敵の当たり判定処理
        for enemy_n in range(ENEMY_MAX):
            enemy_ex[enemy_n] = enemy_x[enemy_n]
            enemy_ey[enemy_n] = enemy_y[enemy_n]
            if hit(enemy_x[enemy_n] + 30,enemy_x[enemy_n],enemy_y[enemy_n] + 30,enemy_y[enemy_n]) or wall(enemy_x[enemy_n],enemy_y[enemy_n],30):
                enemy_x[enemy_n] = enemy_ex[enemy_n]
                enemy_y[enemy_n] = enemy_ey[enemy_n]

        #弾か障害物に当たれば初期位置に戻る
        for pbomb_n in range(PBOMB_MAX):
            if hit(pbomb_x[pbomb_n] + 5,pbomb_x[pbomb_n],pbomb_y[pbomb_n] + 5,pbomb_y[pbomb_n]) or wall(pbomb_xx[pbomb_n],pbomb_yy[pbomb_n],5):
                pbomb_x[pbomb_n] = 400
                pbomb_y[pbomb_n] = 300
                pbomb_s[pbomb_n] = 0   
                pbomb_flg[pbomb_n] = False 

        #弾の表示
        for pbomb_n in range(PBOMB_MAX):
            bomb(screen)
            
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    pbomb_xx[pbomb_count] = pxs
                    pbomb_yy[pbomb_count] = pys
                    pbomb_s[pbomb_count] = -1
                    if pbomb_flg[pbomb_count] == False:
                        pbomb_px[pbomb_count] = pbomb_x[pbomb_count]
                        pbomb_py[pbomb_count] = pbomb_y[pbomb_count]
                    pbomb_bx[pbomb_n] = pbomb_bx[pbomb_count] + pbomb_px[pbomb_count]
                    pbomb_by[pbomb_n] = pbomb_by[pbomb_count] + pbomb_py[pbomb_count]
                    pbomb_flg[pbomb_count] = True
                    pbomb_count += 1
                    if pbomb_count >= 10:
                        pbomb_count = 0



        #プレイヤーの移動
        keys = pygame.key.get_pressed()
        xx = pxs
        yy = pys
        #↑移動
        if keys[K_w]:
            pys -= 1
            if wall(pxs,pys,30):
                pys = -570
            if hit(430,370,330,270):
                pys = yy
        #←移動
        if keys[K_a]:
            pxs -= 1
            if wall(pxs,pys,30):
                pxs = -770
            if hit(430,370,330,270):
                pxs = xx
        #↓移動
        if keys[K_s]:
            pys += 1
            if wall(pxs,pys,30):
                pys = 1170
            if hit(430,370,330,270):
                pys = yy
        #→移動
        if keys[K_d]:
            pxs += 1
            if wall(pxs,pys,30):
                pxs = 1570
            if hit(430,370,330,270):
                pxs = xx


        #画面の更新
        pygame.display.update()

        count += 1


if __name__ == "__main__":
    main()