import pygame
import os
from utils import Animator


class Skill(pygame.sprite.Sprite):

    scene = None
    idle_sprite = None
    damage = 0
    sprite_size = [50, 50]
    duration = 3000
    timer_event = pygame.USEREVENT + 10
    skill_index = 0
    default_player_gravity = 0
    particle_sprite = None
    animator = None

    def __init__(self, player, scene, pos_in_skill_order):
        super().__init__()
        self.player = player
        self.scene = scene

        self.skill_index = pos_in_skill_order
        self.default_player_gravity = self.player.gravity
        self.player.gravity = 0
        self.sprite_size = self.player.sprite_size

        self.player.skills_cooldowns['Internals']['scape_skill'] = [self.timer_event, self.destroy]
        pygame.time.set_timer(self.timer_event, self.duration)

        animations_data = [
            {
                'name':  'default',
                'path': 'assets/skills_sprites/{}/scape_skill/flowers_particles/'.format(player.char_code),
                'repeat': True,
                'call': None
             }
        ]

        self.animator = Animator.Animator(animations_data, self.sprite_size)
        self.blit_skill()

    def destroy(self):
        self.player.gravity = self.default_player_gravity
        self.player.actived_skills.pop(0)

    def blit_skill(self):
        frame = self.animator.animations[self.animator.currentAnimation[0]][self.animator.currentAnimation[1]]
        frame = pygame.transform.scale(frame, self.sprite_size)

        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(frame, (0, 0))
        self.rect = self.surf.get_rect(x=self.player.rect.x, y=self.player.rect.y)

        self.scene.screen.blit(self.surf, self.rect)

    def update_state(self):
        self.animator.update_anim_frame()

