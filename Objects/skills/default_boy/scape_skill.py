import pygame


class Skill(pygame.sprite.Sprite):

    scene = None
    idle_sprite = None
    sprite_size = [50, 50]
    teleport_distance = 200  # pixels
    timer_event = pygame.USEREVENT + 10
    skill_index = 0
    default_player_speed = 0

    def __init__(self, player, scene, pos_in_skill_order):
        super().__init__()
        self.player = player
        self.scene = scene

        self.skill_index = pos_in_skill_order

        self.player.rect.x += self.teleport_distance

        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.rect = self.surf.get_rect(x=self.player.rect.x, y=self.player.rect.y)

    def destroy(self):
        pass

    def move(self):
        pass

