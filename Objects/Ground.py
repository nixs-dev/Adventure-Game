import pygame

class Ground(pygame.sprite.Sprite):
    ground_sprite = pygame.image.load('assets/general_sprites/ground.png')
    position = [0, 400]

    def __init__(self, screen_size):
        super(Ground, self).__init__()
        self.ground_sprite = pygame.transform.scale(self.ground_sprite, [screen_size[0], 100])

        self.surf = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.surf.blit(self.ground_sprite, (0,0))
        self.rect = self.surf.get_rect(x=self.position[0], y=self.position[1])