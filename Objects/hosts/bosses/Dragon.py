import pygame
from utils.Animator import Animator


class Dragon(pygame.sprite.Sprite):
    scene = None
    speed = 7
    gravity = 7
    isJumping = False
    onTheGround = False
    spawn_pos = [500, 40]
    sprite_size = [500, 500]
    animator = None

    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        animation_data = [
            {
                'name': 'default',
                'path': 'assets/monsters_sprites/bosses/Dragon/',
                'repeat': True,
                'call': None
            }
        ]

        self.animator = Animator(animation_data, self.sprite_size)

        default_sprite = pygame.transform.scale(self.animator.get_current_frame(), self.sprite_size)

        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(default_sprite, (0, 0))
        self.surf = pygame.transform.flip(self.surf, True, False)
        self.rect = self.surf.get_rect(x=self.spawn_pos[0], y=self.spawn_pos[1])

        self.start_idle_song()

    def update_state(self):
        self.animator.update_anim_frame()
        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(self.animator.get_current_frame(), (0, 0))
        self.surf = pygame.transform.flip(self.surf, True, False)

    def start_idle_song(self):
        pass

    def fallDueGravity(self):
        if not self.isJumping and not self.onTheGround:
            self.rect.y += self.gravity

    def die(self):
        self.scene.monsters.pop(0)
