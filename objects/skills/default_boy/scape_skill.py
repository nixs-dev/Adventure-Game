import pygame
from utils import Animator

class Skill(pygame.sprite.Sprite):

    scene = None
    idle_sprite = None
    sprite_size = [50, 50]
    damage = 0
    direction = 1
    teleport_distance = 200  # pixels
    timer_event = pygame.USEREVENT + 10
    skill_index = 0
    default_player_speed = 0
    animator = None

    def __init__(self, player, scene, pos_in_skill_order):
        super().__init__()
        self.player = player
        self.scene = scene

        self.direction = 1 if not self.player.flipped else -1

        self.skill_index = pos_in_skill_order
        self.player.rect.x += self.teleport_distance * self.direction

        self.blit_skill()

    def destroy(self):
        pass

    def blit_skill(self):
        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.rect = self.surf.get_rect(x=self.player.rect.x, y=self.player.rect.y)

        self.scene.screen.blit(self.surf, self.rect)

    def update_state(self):
        pass

