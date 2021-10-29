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
pbomb_x = [400.0]*PBOMB_MAX
pbomb_y = [300.0]*PBOMB_MAX
pbomb_xx = [0.0]*PBOMB_MAX
pbomb_yy = [0.0]*PBOMB_MAX
pbomb_s = [0.0]*PBOMB_MAX
pbomb_flg = [False]*PBOMB_MAX
pbomb_count = 0

#マウスの座標
mpos_x = 0
mpos_y = 0
mflg_x = True
mflg_y = True
mpos_s = 0

#敵
ENEMY_MAX = 50
enemy_n = 0
enemy_x = [400]*ENEMY_MAX
enemy_y = [300]*ENEMY_MAX
enemy_xx = [0]*ENEMY_MAX
enemy_yy = [0]*ENEMY_MAX

#障害物の処理
def setblock(screen):
    global block_n,block_x,block_y,block_height,block_width
    pygame.draw.rect(screen,(0,255,0),Rect(block_x[block_n] - pxs,block_y[block_n] - pys,block_width[block_n],block_height[block_n]),5)

#弾の処理
def bomb(screen):
    global pbomb_n,pbomb_x,pbomb_y,pbomb_s
    pbomb_x[pbomb_n] += pbomb_xx[pbomb_n]
    pbomb_y[pbomb_n] += pbomb_yy[pbomb_n]
    print('x = ' + str(pbomb_x[pbomb_n]) + ',y = ' + str(pbomb_y[pbomb_n]) + ',xx = ' + str(pbomb_xx[pbomb_n]) + ',yy = ' + str(pbomb_yy[pbomb_n]) + ',s = ' + str(pbomb_s[pbomb_n]) + ',n == ' + str(pbomb_n))
    pygame.draw.circle(screen,(10,10,10),(pbomb_x[pbomb_n],pbomb_y[pbomb_n]),5)

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

def attack():
    global mpos_x,mpos_y,mflg_x,mflg_y,mpos_s,pbomb_xx,pbomb_yy
    mpos_x,mpos_y = pygame.mouse.get_pos()

    if mpos_x > 400:
        mflg_x = True
    else:
        mflg_x = False
    if mpos_y > 300:
        mflg_y = True
    else:
        mflg_y = False

    if mflg_x == False or mflg_y == False:
        if mpos_x * -1 > mpos_y:
            mpos_s = mpos_x
        else:
            mpos_s = mpos_y
    else:
        if mpos_x > mpos_y:
            mpos_s = mpos_x
        else:
            mpos_s = mpos_y

    pbomb_xx = (mpos_x - 400) / mpos_s
    pbomb_yy = (mpos_y - 300) / mpos_s


def main():
    global pxs,pys,block_n,block_x,block_y,block_height,block_width,pbomb_n,pbomb_x,pbomb_y,pbomb_s,pbomb_count,enemy_n
    pygame.init()                                 # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))  # 800*600の画面

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
            if random.randint(0,100) % 100 == 0:
                moveenemy()

        #敵の当たり判定処理
        for enemy_n in range(ENEMY_MAX):
            if hit(enemy_x[enemy_n] + 30 - pxs,enemy_x[enemy_n] - pxs,enemy_y[enemy_n] + 30 - pys,enemy_y[enemy_n] - pys) or wall(enemy_x[enemy_n] - 400,enemy_y[enemy_n] - 300,30):
                enemy_xx[enemy_n] *= -1
                enemy_yy[enemy_n] *= -1

        #弾か障害物に当たれば初期位置に戻る
        #for pbomb_n in range(PBOMB_MAX):
         #   if hit(int(pbomb_x[pbomb_n]) + 5,int(pbomb_x[pbomb_n]),int(pbomb_y[pbomb_n]) + 5,int(pbomb_y[pbomb_n])) or wall(int(pbomb_xx[pbomb_n]),int(pbomb_yy[pbomb_n]),5):
          #      pbomb_x[pbomb_n] = 400
           #     pbomb_y[pbomb_n] = 300
            #    pbomb_s[pbomb_n] = 0   
             #   pbomb_flg[pbomb_n] = False 

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
                    pbomb_s[pbomb_count] = -1
                    attack()
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


if __name__ == "__main__":
    main()