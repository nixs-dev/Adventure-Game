import pygame


class Wolf(pygame.sprite.Sprite):
    scene = None
    speed = 7
    gravity = 7
    isJumping = False
    onTheGround = False
    canGo = True
    canBack = True
    GoToRight = False
    spawn_pos = [500, 40]
    sprite_size = [50, 100]
    idle_sprite = pygame.image.load('assets/monsters_sprites/evil_wolf/idle.png')

    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        self.idle_sprite = pygame.transform.scale(self.idle_sprite, self.sprite_size)
        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(self.idle_sprite, (0, 0))
        self.rect = self.surf.get_rect(x=self.spawn_pos[0], y=self.spawn_pos[1])

    def update_state(self):
        if not self.onTheGround:
            return

        if self.GoToRight:
            if self.canGo:
                self.rect.x += self.speed
            else:
                self.GoToRight = False
        else:
            if self.canBack:
                self.rect.x -= self.speed
            else:
                self.GoToRight = True

        self.checkLimits()

    def checkLimits(self):
        if self.rect.x <= 0:
            self.canBack = False
        else:
            self.canBack = True

        if self.rect.x >= self.scene.screen_size[0] - self.sprite_size[0]:
            self.canGo = False
        else:
            self.canGo = True

    def fallDueGravity(self):
        if not self.isJumping and not self.onTheGround:
            self.rect.y += self.gravity

    def die(self):
        self.scene.monsters.pop(0)
