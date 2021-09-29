import pygame

class Heart(pygame.sprite.Sprite):
    heart_sprite = pygame.image.load('assets/sprites/heart_alive.png')
    on = True
    position = []
    size = [20, 20]

    def __init__(self, x_offset):
        super(Heart, self).__init__()
        position = [0, 0]

        self.heart_sprite = pygame.transform.scale(self.heart_sprite, self.size)
        
        position[0] += x_offset
        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surf.blit(self.heart_sprite, (0,0))
        self.rect = self.surf.get_rect(x=position[0], y=position[1])
        self.position = position

    def off(self):
        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.heart_sprite = pygame.image.load('assets/sprites/heart_dead.png')
        self.heart_sprite = pygame.transform.scale(self.heart_sprite, self.size)
        self.surf.blit(self.heart_sprite, (0,0))
        self.on = False