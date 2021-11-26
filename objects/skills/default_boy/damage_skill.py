import pygame

class Skill(pygame.sprite.Sprite):

    scene = None
    speed = 15
    damage = 1
    sprite_size = [30, 30]
    idle_sprite = None
    skill_index = 0

    def __init__(self, player, scene, pos_in_skill_order):
        super().__init__()
        self.player = player
        self.scene = scene

        self.skill_index = pos_in_skill_order

        self.idle_sprite = pygame.image.load('assets/skills_sprites/{}/damage_skill/idle.png'.format(player.char_code))

        self.idle_sprite = pygame.transform.scale(self.idle_sprite, self.sprite_size)
        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(self.idle_sprite, (0, 0))
        self.rect = self.surf.get_rect(x=player.rect.x, y=player.rect.y)

    def update_state(self):
        self.rect.x += self.speed

        self.checkLimits()

    def checkLimits(self):
        if self.rect.x <= 0 or self.rect.x >= self.scene.screen_size[0] - self.sprite_size[0]:
            self.destroy()

    def destroy(self):
        self.player.actived_skills.pop(self.skill_index)

    def blit_skill(self):
        self.scene.screen.blit(self.surf, self.rect)