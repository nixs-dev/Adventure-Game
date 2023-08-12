import pygame


class Skill(pygame.sprite.Sprite):

    scene = None
    idle_sprite = None
    damage = 0
    sprite_size = [50, 50]
    bonus = 1.5
    duration = 3000
    timer_event = pygame.USEREVENT + 10
    skill_index = 0
    default_player_speed = 0

    def __init__(self, player, scene, pos_in_skill_order):
        super().__init__()
        self.player = player
        self.scene = scene

        self.skill_index = pos_in_skill_order

        self.default_player_speed = self.player.speed
        self.player.speed += (self.player.speed * self.bonus)

        self.player.skills_cooldowns['Internals']['scape_skill'] = [self.timer_event, self.destroy]
        pygame.time.set_timer(self.timer_event, self.duration)

        self.blit_skill()

    def destroy(self):
        self.player.speed = self.default_player_speed
        self.player.actived_skills.pop(self.skill_index)

    def update_state(self):
        pass

    def blit_skill(self):
        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.rect = self.surf.get_rect(x=self.player.rect.x, y=self.player.rect.y)

        self.scene.screen.blit(self.surf, self.rect)
