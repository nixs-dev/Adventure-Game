import pygame


class Skill(pygame.sprite.Sprite):

    scene = None
    idle_sprite = None
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

        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.rect = self.surf.get_rect(x=self.player.rect.x, y=self.player.rect.y)

        self.player.skills_cooldowns['Internals']['scape_skill'] = [self.timer_event, self.destroy]
        pygame.time.set_timer(self.timer_event, self.duration)

    def destroy(self):
        self.player.speed = self.default_player_speed
        self.player.actived_skills.pop(self.skill_index)

    def move(self):
        pass

