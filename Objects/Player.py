import pygame
import os
from Objects.Heart import Heart


class Player(pygame.sprite.Sprite):
    scene = None
    flipped = False
    maxLifes = 3
    lifesAmount = 3
    lifes = []
    speed = 7
    MaxSpeed = 7
    gravity = 7
    jumpForce = 10
    maxJumpHeight = 100
    jumpHeight = 0
    onTheGround = False
    canBack = True
    canGo = True
    isJumping = False
    position = [0, 0]
    intangible = False
    intangibility_event = pygame.USEREVENT 
    intangibleTimer = 2000 #2 seconds
    sprite_size = (75, 100)
    dead = False
    animations = {
        'idle_player' : [],
        'running_player': [],
        'jumping_player': [],
        'dying_player': [],
        'falling_player': [],
    }
    currentAnimation = ['idle_player', 0, True, None]
    

    def __init__(self, scene):
        super(Player, self).__init__()
        self.scene = scene
        self.loadSprites()
        self.loadLifes()

        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(self.animations['idle_player'][0], (0,0))
        self.rect = self.surf.get_rect(x=self.position[0], y=self.position[1])

    def fixSpriteList(self, origin, list_):
        tempList = []
        finalList = []

        for i in list_:
            num = i.replace('.png', '')
            num = int(num)
            tempList.append(num)

        tempList = sorted(tempList, key=int)

        for i in tempList:
            item = origin + str(i) + '.png'
            item = pygame.image.load(item)
            item = pygame.transform.scale(item, self.sprite_size)
            finalList.append(item)

        return finalList

    def loadSprites(self):
        idle = 'assets/sprites/player/idle/'
        run = 'assets/sprites/player/run/'
        jump = 'assets/sprites/player/jump/'
        dead = 'assets/sprites/player/dead/'
        fall = 'assets/sprites//player/fall/'

        idle_sprites = self.fixSpriteList(idle, os.listdir(idle))
        run_sprites = self.fixSpriteList(run, os.listdir(run))
        jump_sprites = self.fixSpriteList(jump, os.listdir(jump))
        dead_sprites = self.fixSpriteList(dead, os.listdir(dead))
        fall_sprites = self.fixSpriteList(fall, os.listdir(fall))


        self.animations['idle_player'] = idle_sprites
        self.animations['running_player'] = run_sprites
        self.animations['jumping_player'] = jump_sprites
        self.animations['dying_player'] = dead_sprites
        self.animations['falling_player'] = fall_sprites

    def loadLifes(self):
        self.lifes = []
        
        previous_pos = -50
        for i in range(0, self.maxLifes):
            previous_pos += 50
            heart = Heart(previous_pos)
            self.lifes.append(heart)

    def move(self, x, y):
        if self.dead:
            return 

        x = x * self.speed

        if x < 0:
            if not self.canBack:
                x = 0
            if not self.flipped:
                self.flipped = True


        if x > 0: 
            if not self.canGo:
                x = 0
            if self.flipped:
                self.flipped = False

        if y < 0:
            self.isJumping = True
            self.updateAnim('jumping_player', False, None)

        if self.isJumping:
            y = -1 * self.jumpForce
            self.jumpHeight -= y

        if self.jumpHeight == self.maxJumpHeight:
            self.isJumping = False
            self.jumpHeight = 0

        self.rect.x += x
        self.rect.y += y

        if self.onTheGround and not self.isJumping:
            if x != 0:
                self.updateAnim('running_player', True, None)
            else:
                self.updateAnim('idle_player', True, None)

        if not self.onTheGround and not self.isJumping:
            self.updateAnim('falling_player', False, None)
        self.checkLimits()

    def loseLife(self):
        if self.lifesAmount > 0:
            if not self.intangible:
                self.lifesAmount -= 1
                self.lifes[self.lifesAmount].off()

                self.get_intangible()
        else:
            self.dead = True
            self.updateAnim('dying_player', False, self.die)

    def checkCoolDowns(self, event):
        if event.type == self.intangibility_event and self.intangible:
            self.intangible = False
            pygame.time.set_timer(self.intangibility_event, 0)


    def get_intangible(self):
        pygame.time.set_timer(self.intangibility_event, self.intangibleTimer)
        self.intangible = True

    def checkLimits(self):
        if self.rect.x <= 0:
            self.canBack = False
        else:
            self.canBack = True

        if self.rect.x >= self.scene.screen_size[0] - self.sprite_size[0]:
            self.canGo = False
        else:
            self.canGo = True


    def updateAnim(self, whichOne, repeat, finalAction):
        if self.currentAnimation[0] != whichOne:
            self.currentAnimation = [whichOne, 0, repeat, finalAction]
            self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
            self.surf.blit(self.animations[whichOne][0], (0,0))

    def updateAnimFrame(self):
        currentFrame = self.currentAnimation[1]
        try:
            self.currentAnimation[1] += 1
            nextFrame = self.animations[self.currentAnimation[0]][self.currentAnimation[1]]
        except IndexError:
            if self.currentAnimation[2]:
                self.currentAnimation[1] = 0
                nextFrame = self.animations[self.currentAnimation[0]][self.currentAnimation[1]]
            else:
                nextFrame = self.animations[self.currentAnimation[0]][currentFrame]
                self.currentAnimation[1] = currentFrame
                self.currentAnimation[3]() if self.currentAnimation[3] != None else 0
        finally:
            self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
            self.surf.blit(nextFrame, (0,0))



    def fallDueGravity(self):
        if not self.isJumping and not self.onTheGround:
            self.rect.y += self.gravity

    def die(self):
        self.scene.gameEnd = True