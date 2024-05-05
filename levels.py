from random import randint 
import pygame
import json 


pygame.init()

dictionary = [
    {
        "platforms": [
            {"x": 400, "y": 500, "w": 100, "h": 20},
            {"x": 400, "y": 400, "w": 80, "h": 20},
            {"x": 400, "y": 300, "w": 120, "h": 20}
        ],
        "goal" : {"x": 400, "y": 200}
    },
    {
        "platforms": [
            {"x": 100, "y": 500, "w": 100, "h": 20},
            {"x": 300, "y": 400, "w": 80, "h": 20},
            {"x": 500, "y": 300, "w": 120, "h": 20}
        ],
        "goal": {"x": 530, "y": 200}
    }
]
with open('levels.json', 'w') as f:
    json.dump(dictionary, f)

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

FPS = 30


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, window_width, window_height):
        self.width = 50
        self.height = 50
        self.x = window_width // 2 - self.width // 2
        self.y = window_height - self.height 
        self.speed = 5
        self.jump = False
        self.jump_count = 0 

    def draw(self, window):
        pygame.draw.rect(window, BLUE, (self.x, self.y, self.width, self.height))


    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_SPACE] and not self.jump:
            self.jump_count = 20
            self.jump = True


    def update(self):
        if self.jump_count >= 0:
            self.y -= 15
            self.jump_count -= 1
        for platform in platforms:
            if self.y + self.height >= platform.y and self.y + self.height < platform.y + 10 \
                and self.x + self.width >= platform.x and self.x <= platform.x + platform.width:
                self.y = platform.y - self.height
                self.jump = False
        self.y += 10 * (self.y / (window_height - self.height))
        if self.y > window_height - self.height:
            self.y = window_height - self.height
            jump = False


class Platform:
    def __init__(self, x, y, w, h):
        self.width = w
        self.height = h 
        self.x = x 
        self.y = y 

    def draw(self, window):
        pygame.draw.rect(window, BLUE, (self.x, self.y, self.width, self.height))

class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def update(self):
        global platforms, goal 
        if player.x + player.width >= self.x and player.x <= self.x + self.width \
            and player.y + player.height >= self.y and player.y <= self.y + self.height:
            print("Goal reached!")
            platforms = []
            for d in levels[1]['platforms']:
                platform = Platform(d['x'], d['y'], d['w'], d['h'])
                platforms.append(platform)
            goal = Goal(levels[1]['goal']['x'], levels[1]['goal']['y'])
            player.x = window_width // 2 - self.width // 2
            player.y = window_height - self.height


with open('levels.json') as f:
    levels = json.load(f)

platforms = []
for d in levels[0]['platforms']:
    platform = Platform(d['x'], d['y'], d['w'], d['h'])
    platforms.append(platform)
goal = Goal(levels[0]['goal']['x'], levels[0]['goal']['y'])
player = Player(window_width, window_height)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    player.move(keys)
    player.update()


    window.fill(WHITE)
    player.draw(window)
    for platform in platforms:
        platform.draw(window)
    goal.draw(window)
    goal.update()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()