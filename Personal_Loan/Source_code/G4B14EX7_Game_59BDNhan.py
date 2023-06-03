import pygame, sys, random
from pygame.locals import *

class Game:
    def __init__(self):
        ####################################
        #PHẦN 1: ĐỊNH NGHĨA CÁC THAM SỐ ##
        #####################################
        ###KÍCH THƯỚC KHUNG MÀN HÌNH GAME
        self.WINDOWWIDTH = 400
        self.WINDOWHEIGHT = 600
        ###KHỞI TẠO THƯ VIỆN ĐỂ DÙNG
        pygame.init()
        ##TỐC ĐỘ KHUNG HÌNH CỦA VIDEO
        self.FPS = 60 # Famres Per Second
        self.fpsClock = pygame.time.Clock() #Lặp theo nhịp clock (tham số FPS)
        ####################################
        #####PHẦN 2: NỀN GAME ##############
        #####################################
        #TỐC ĐỘ CUỘN NỀN
        self.BGSPEED = 20 # tốc độ cuộn nền
        self.BGIMG = pygame.image.load('Source_code/img/background.png') # hình nền
        # LAYER (SURFACE) NỀN
        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('59 Bui Duc Nhan - Game ĐUA XE')
    
def gameOver(bg, car, obstacles, score, game):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
    commentSize = commentSuface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    return
        bg.draw()
        car.draw()
        obstacles.draw()
        score.draw()
        game.DISPLAYSURF.blit(headingSuface, (int((game.WINDOWWIDTH - headingSize[0])/2), 100))
        game.DISPLAYSURF.blit(commentSuface, (int((game.WINDOWWIDTH - commentSize[0])/2), 400))
        pygame.display.update()
        game.fpsClock.tick(game.FPS)

def gameStart(bg, game):
    bg.__init__()
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('RACING', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to play', True, (0, 0, 0))
    commentSize = commentSuface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    return
        bg.draw()
        game.DISPLAYSURF.blit(headingSuface, (int((game.WINDOWWIDTH - headingSize[0])/2), 100))
        game.DISPLAYSURF.blit(commentSuface, (int((game.WINDOWWIDTH - commentSize[0])/2), 400))
        pygame.display.update()
        game.fpsClock.tick(game.FPS)

def gamePlay(bg, car, obstacles, score, game):
    car.__init__()
    obstacles.__init__()
    bg.__init__()
    score.__init__()
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveRight = True
                if event.key == K_UP:
                    moveUp = True
                if event.key == K_DOWN:
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

        if isGameover(car, obstacles):
            return
        bg.draw()
        bg.update()
        car.draw()
        car.update(moveLeft, moveRight, moveUp, moveDown)
        obstacles.draw()
        obstacles.update()
        score.draw()
        score.update()
        pygame.display.update()
        game.fpsClock.tick(game.FPS)
    
# LỚP HÌNH NỀN = CUỘN NỀN
class Background(Game):
    def __init__(self):
        Game.__init__(self)
        self.x = 0
        self.y = 0
        self.speed = self.BGSPEED
        self.img = self.BGIMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self):
        self.DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        self.DISPLAYSURF.blit(self.img, (int(self.x), int(self.y-self.height)))
    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y -= self.height
####################################
#####PHẦN 3: XE TRONG GAME #########
"""
    • X_MARGIN là lề hai bên trái và phải (xe không được vượt qua đó).
    • CARWIDTH và CARHEIGHT là kích thước của xe.
    • CARSPEED là tốc độ di chuyển (tiến, lùi, trái, phải) của xe.
    • CARIMG là ảnh chiếc xe.
"""
#####################################
#KÍCH THƯỚC XE
X_MARGIN = 80
CARWIDTH = 40
CARHEIGHT = 60
CARSPEED = 3
CARIMG = pygame.image.load('Source_code/img/car.png')
#LỚP XE TRONG GAME
class Car(Game):
    def __init__(self):
        Game.__init__(self)
        self.width = CARWIDTH
        self.height = CARHEIGHT
        self.x = (self.WINDOWWIDTH-self.width)/2
        self.y = (self.WINDOWHEIGHT-self.height)/2
        self.speed = CARSPEED
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))
    def draw(self):
        self.DISPLAYSURF.blit(CARIMG, (int(self.x), int(self.y)))
    def update(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft == True:
            self.x -= self.speed
        if moveRight == True:
            self.x += self.speed
        if moveUp == True:
            self.y -= self.speed
        if moveDown == True:
            self.y += self.speed

        if self.x < X_MARGIN:
            self.x = X_MARGIN
        if self.x + self.width > self.WINDOWWIDTH - X_MARGIN:
            self.x = self.WINDOWWIDTH - X_MARGIN - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > self.WINDOWHEIGHT :
            self.y = self.WINDOWHEIGHT - self.height

####################################
#PHẦN 4: XE CHƯỚNG NGẠI VẬT = XE NGƯỢC CHIỀU:obstacles ##
"""
• LANEWIDTH là độ rộng của 1 làn xe (đường có 4 làn).
• DISTANCE là khoảng cách giữa các xe theo chiều dọc.
• OBSTACLESSPEED là tốc độ ban đầu của những chiếc xe.
• CHANGESPEED dùng để tăng tốc độ của những chiếc xe theo thời gian.
• OBSTACLESIMG là ảnh chiếc xe.
"""
#####################################
LANEWIDTH = 60
DISTANCE = 200
OBSTACLESSPEED = 2
CHANGESPEED = 0.001
OBSTACLESIMG = pygame.image.load('Source_code/img/obstacles.png')
class Obstacles(Game):
    def __init__(self):
        Game.__init__(self)
        self.width = CARWIDTH
        self.height = CARHEIGHT
        self.distance = DISTANCE
        self.speed = OBSTACLESSPEED
        self.changeSpeed = CHANGESPEED
        self.ls = []
        for i in range(5):
            y = -CARHEIGHT-i*self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])
    def draw(self):
        for i in range(5):
            x = int(X_MARGIN + self.ls[i][0]*LANEWIDTH + (LANEWIDTH-self.width)/2)
            y = int(self.ls[i][1])
            self.DISPLAYSURF.blit(OBSTACLESIMG, (x, y))
    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.changeSpeed
        if self.ls[0][1] > self.WINDOWHEIGHT:
            self.ls.pop(0)
            y = self.ls[3][1] - self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])
####################################
#PHẦN 5: TÍNH ĐIỂM ##
#####################################
class Score(Game):
    def __init__(self):
        Game.__init__(self)
        self.score = 0
    def draw(self):
        font = pygame.font.SysFont('consolas', 30)
        scoreSuface = font.render('Score: '+str(int(self.score)), True, (0, 0, 0))
        self.DISPLAYSURF.blit(scoreSuface, (10, 10))
    def update(self):
        self.score += 0.02

####################################
#PHẦN 6: XỬ LÝ VA CHẠM: Collision ##
#####################################
def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False
def isGameover(car, obstacles):
    carRect = [car.x, car.y, car.width, car.height]
    for i in range(5):
        x = int(X_MARGIN + obstacles.ls[i][0]*LANEWIDTH + (LANEWIDTH-obstacles.width)/2)
        y = int(obstacles.ls[i][1])
        obstaclesRect = [x, y, obstacles.width, obstacles.height]
        if rectCollision(carRect, obstaclesRect) == True:
            return True
    return False
####################################
#PHẦN 7: CÁC THỦ TỤC CHƠI GAME ##
"""
• gameStart() là phần chuẩn bị khi vừa mở game lên.
• gamePlay() là phần chơi chính.
• gameOver() là phần xuất hiện khi thua 1 màn chơi.
"""
#####################################

####################################
#PHẦN 8: HÀM MAIN ##
#####################################
def play_game():
    game = Game()
    bg = Background()
    car = Car()
    obstacles = Obstacles()
    score = Score()
    gameStart(bg, game)
    while True:
        gamePlay(bg, car, obstacles, score, game)
        gameOver(bg, car, obstacles, score, game)

# if __name__ == '__main__':
#     play_game()