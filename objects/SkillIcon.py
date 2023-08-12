import pygame
from controllers.Character import Character


class SkillIcon(pygame.sprite.Sprite):
    sprite = None
    position = [0, 0]
    size = [50, 50]

    def __init__(self, screen_size, offset, player_code, skill_type):
        super().__init__()

        self.position[0] = (screen_size[0] - self.size[0]) - offset

        sprite_path = Character.get_skill_icons_paths(player_code)[skill_type]

        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, self.size)

        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surf.blit(self.sprite, (0, 0))
        self.rect = self.surf.get_rect(x=self.position[0], y=self.position[1])
