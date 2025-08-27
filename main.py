#imports
import pygame
import random
import os

screen_size = (200, 450) #width 200, height 450
background_color = (255, 255, 255) #white
FPS = 60
font_name = pygame.font.match_font("arial")

block_types = ["I", "T", "J", "L", "S", "Z", "O"]
falling_frame = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1]
clearing_score = [0, 40, 100, 300, 1000]
image_dict = {
    0 : pygame.image.load(os.path.join("./images/ground.png")),
    "I" : pygame.image.load(os.path.join("./images/block_I.png")),
    "T" : pygame.image.load(os.path.join("./images/block_T.png")),
    "J" : pygame.image.load(os.path.join("./images/block_J.png")),
    "L" : pygame.image.load(os.path.join("./images/block_L.png")),
    "S" : pygame.image.load(os.path.join("./images/block_S.png")),
    "Z" : pygame.image.load(os.path.join("./images/block_Z.png")),
    "O" : pygame.image.load(os.path.join("./images/block_O.png"))
}
little_image_dict = {
    "I" : pygame.image.load(os.path.join("./images/little_I.png")),
    "T" : pygame.image.load(os.path.join("./images/little_T.png")),
    "J" : pygame.image.load(os.path.join("./images/little_J.png")),
    "L" : pygame.image.load(os.path.join("./images/little_L.png")),
    "S" : pygame.image.load(os.path.join("./images/little_S.png")),
    "Z" : pygame.image.load(os.path.join("./images/little_Z.png")),
    "O" : pygame.image.load(os.path.join("./images/little_O.png"))
}
tetromino_dict = {
    "I" : [
        [(0,0), (1,0), (2,0), (3,0)],
        [(2,-1), (2,0), (2,1), (2,2)],
        [(0,1), (1,1), (2,1), (3,1)],
        [(1,-1), (1,0), (1,1), (1,2)]],
    "O" : [
        [(0,0), (1,0), (0,1), (1,1)],
        [(0,0), (1,0), (0,1), (1,1)],
        [(0,0), (1,0), (0,1), (1,1)],
        [(0,0), (1,0), (0,1), (1,1)]],
    "T" : [
        [(0,0), (1,0), (2,0), (1,1)],
        [(1,-1), (1,0), (1,1), (0,0)],
        [(0,1), (1,1), (2,1), (1,0)],
        [(1,-1), (1,0), (1,1), (2,0)]],
    "S" : [
        [(1,0), (2,0), (0,1), (1,1)],
        [(1,-1), (1,0), (2,0), (2,1)],
        [(1,1), (2,1), (0,2), (1,2)],
        [(0,-1), (0,0), (1,0), (1,1)]],
    "Z" : [
        [(0,0), (1,0), (1,1), (2,1)],
        [(2,-1), (1,0), (2,0), (1,1)],
        [(0,1), (1,1), (1,2), (2,2)],
        [(1,-1), (0,0), (1,0), (0,1)]],
    "J" : [
        [(0,0), (0,1), (1,1), (2,1)],
        [(0,0), (0,1), (1,0), (0,2)],
        [(0,1), (1,1), (2,1), (2,2)], 
        [(0,2), (1,0), (1,1), (1,2)]],
    "L" : [
        [(2,0), (0,1), (1,1), (2,1)],
        [(0,-1), (0,0), (0,1), (1,1)],
        [(0,0), (1,0), (2,0), (0,1)],
        [(0,-1), (1,-1), (1,0), (1,1)]]
}

class block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_dict[board[y][x]]
        self.rect = self.image.get_rect()
        self.rect.left = x*20
        self.rect.top = y*20+10
        self.x = x
        self.y = y

    def update(self):
        self.image = image_dict[board[self.y][self.x]]

class little(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = little_image_dict[block_queue[0]]
        self.rect = self.image.get_rect()
        self.rect.left = 150
        self.rect.centery = 25
    def update(self):
        self.image = little_image_dict[block_queue[0]]
        self.rect = self.image.get_rect()
        self.rect.left = 150
        self.rect.centery = 25

class tetromino():
    def __init__(self):
        global playing, waiting_counter
        self.x = 4
        self.y = 0
        self.type = block_queue[0]
        self.status = 0
        for dx, dy in tetromino_dict[self.type][self.status]:
            if board[self.y+dy][self.x+dx] != 0:
                playing = 2
                waiting_counter = 0
                break
        else:
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type
            del block_queue[0]
            self.down()
            self.down()

    def down(self):
        stop = False
        for dx, dy in tetromino_dict[self.type][self.status]:
            board[self.y+dy][self.x+dx] = 0
        self.y += 1
        for dx, dy in tetromino_dict[self.type][self.status]:
            if self.y+dy >= 22 or board[self.y+dy][self.x+dx] != 0:
                stop = True
                break
        else:
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type
        if stop:
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy-1][self.x+dx] = self.type
            clear()
            self.__init__()

    def left(self):
        blocked = False
        for dx, dy in tetromino_dict[self.type][self.status]:
            board[self.y+dy][self.x+dx] = 0
        for dx, dy in tetromino_dict[self.type][self.status]:
            if self.x+dx-1 < 0 or board[self.y+dy][self.x+dx-1] != 0:
                blocked = True
                break
        else:
            self.x -= 1
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type
        if blocked:
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type

    def right(self):
        blocked = False
        for dx, dy in tetromino_dict[self.type][self.status]:
            board[self.y+dy][self.x+dx] = 0
        for dx, dy in tetromino_dict[self.type][self.status]:
            if self.x+dx+1 >= 10 or board[self.y+dy][self.x+dx+1] != 0:
                blocked = True
                break
        else:
            self.x += 1
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type
        if blocked:
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type
    
    def spin(self):
        blocked = False
        for dx, dy in tetromino_dict[self.type][self.status]:
            board[self.y+dy][self.x+dx] = 0
        for dx, dy in tetromino_dict[self.type][(self.status+1)%4]:
            if (self.x+dx >= 10 or 
                self.x+dx < 0 or 
                self.y+dy >= 22 or 
                self.y+dy < 0 or 
                board[self.y+dy][self.x+dx] != 0):
                blocked = True
                break
        else:
            self.status = (self.status+1)%4
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type
        if blocked:
            for dx, dy in tetromino_dict[self.type][self.status]:
                board[self.y+dy][self.x+dx] = self.type

#setup
pygame.init()
pygame.key.set_repeat(267, 100) #16, 6 frame
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")
pygame.display.set_icon(little_image_dict["T"])

running = True
playing = 0
waiting_counter = 0
random.shuffle(block_types)
block_queue = block_types[:]
board = [[0 for _ in range(10)] for _ in range(22)]

blocks = pygame.sprite.Group()
tetro = tetromino()

level = 0
score = 0
frame_counter = 0
clear_counter = 0

def draw_text(text, size, x, y, centerx=False):
    surf = screen
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.left = x
    if centerx:
        text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)

def clear():
    global score, clear_counter, level
    cleared = 0
    for i in range(21, 1, -1):
        for j in range(10):
            if board[i][j] == 0:
                break
        else:
            cleared += 1
            del board[i]
    score += clearing_score[cleared]*(level+1)
    clear_counter +=  cleared
    level = clear_counter // 10
    for i in range(cleared):
        board.insert(0, [0 for _ in range(10)])

def init():
    global playing, level, score, frame_counter, clear_counter, board, block_types, block_queue
    level = 0
    score = 0
    frame_counter = 0
    clear_counter = 0
    board = [[0 for _ in range(10)] for _ in range(22)]
    random.shuffle(block_types)
    block_queue = block_types[:]
    block_icon = little()
    blocks.add(block_icon)
    for i in range(2, 22):
        for j in range(10):
            bl = block(j, i)
            blocks.add(bl)
    tetro.__init__()
    playing = 1

while running:
    screen.fill(background_color)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if playing == 0:
        draw_text("START", 36, 100, 200, True)
        draw_text("press any key", 18, 100, 240, True)
        for event in events:
            if event.type == pygame.KEYUP:
                init()

    if playing == 1:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tetro.right()
                if event.key == pygame.K_LEFT:
                    tetro.left()
                if event.key == pygame.K_DOWN:
                    tetro.down()
                if event.key == pygame.K_UP:
                    tetro.spin()

        if len(block_queue) <= 7:
            random.shuffle(block_types)
            block_queue += block_types

        frame_counter += 1
        if frame_counter >= falling_frame[level]:
            frame_counter = 0
            tetro.down()

        blocks.update()
        blocks.draw(screen)
        draw_text(f"Score : {score}", 14, 10, 10)
        draw_text(f"Level : {level}", 14, 10, 30)
        draw_text("Next : ", 14, 107, 25)

    if playing == 2:
        waiting_counter += 1
        draw_text("YOU LOSE", 32, 100, 200, True)
        draw_text(f"Score : {score}", 20, 100, 225, True)
        draw_text("press any key to restart", 12, 100, 250, True)

        for event in events:
            if event.type == pygame.KEYUP and waiting_counter > 60:
                init()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()