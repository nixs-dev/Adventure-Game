import pygame
import os


class Player(pygame.sprite.Sprite):
    flipped = False
    speed = 4
    MaxSpeed = 4
    gravity = 3
    jumpForce = 5
    maxJumpHeight = 30
    jumpHeight = 0
    onTheGround = False
    canBack = True
    canGo = True
    isJumping = False
    position = [0, 0]
    sprite_size = (75, 100)
    animations = {
        'idle_player' : [],
        'running_player': []
    }
    currentAnimation = ['idle_player', 0]
    

    def __init__(self):
        super(Player, self).__init__()
        self.loadSprites()

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

        idle_sprites = self.fixSpriteList(idle, os.listdir(idle))
        run_sprites = self.fixSpriteList(run, os.listdir(run))
        
        self.animations['idle_player'] = idle_sprites
        self.animations['running_player'] = run_sprites

    def move(self, x, y):
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

        if self.isJumping:
            y = -1 * self.jumpForce
            self.jumpHeight -= y

        if self.jumpHeight == self.maxJumpHeight:
            self.isJumping = False
            self.jumpHeight = 0

        self.rect.x += x
        self.rect.y += y

        if x != 0:
            self.updateAnim('running_player')
        else:
            self.updateAnim('idle_player')


    def updateAnim(self, whichOne):
        if self.currentAnimation[0] != whichOne:
            self.currentAnimation = [whichOne, 0]
            self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
            self.surf.blit(self.animations[whichOne][0], (0,0))

    def updateAnimFrame(self):
        try:
            self.currentAnimation[1] += 1
            nextFrame = self.animations[self.currentAnimation[0]][self.currentAnimation[1]]
        except IndexError:
            self.currentAnimation[1] = 0
            nextFrame = self.animations[self.currentAnimation[0]][self.currentAnimation[1]]
        finally:
            self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
            self.surf.blit(nextFrame, (0,0))


    def fallDueGravity(self):
        if not self.isJumping:
            self.rect.y += self.gravity
