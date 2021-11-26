import pygame
import os
import importlib.util
from objects.Heart import Heart
from utils import Animator

class Player(pygame.sprite.Sprite):
    scene = None
    animator = None
    flipped = False
    char_code = ''
    maxLifes = 3
    lifesAmount = 3
    lifes = []
    speed = 7
    MaxSpeed = 7
    gravity = 7
    jumpForce = 10
    maxJumpHeight = 100
    jumpHeight = 0
    onTheGround = False
    canBack = True
    canGo = True
    isJumping = False
    position = [0, 0]
    intangible = False
    intangibility_event = pygame.USEREVENT
    skills_cooldowns = {
        'damage_skill': [pygame.USEREVENT + 1, 2000, True],
        'scape_skill': [pygame.USEREVENT + 2, 5000, True],
        'Internals': {}
    }
    intangibleTimer = 1000 # 1 second
    sprite_size = (75, 100)
    dead = False
    skills = {
        'damage_skill': None,
        'scape_skill': None
    }

    jump_default_song = None
    currentAnimation = ['idle_player', 0, True, None]
    actived_skills = []

    def __init__(self, scene, char_code):
        super(Player, self).__init__()
        self.char_code = char_code

        self.scene = scene
        self.dead = False
        self.actived_skills = []
        self.jumpHeight = 0
        self.speed = self.MaxSpeed

        self.load_songs()
        self.load_lifes()
        self.load_skills()

        animations_data = [
            {
                'name': 'idle_player',
                'path': 'assets/chars_sprites/{}/idle/'.format(self.char_code),
                'repeat': True,
                'call': None
            },
            {
                'name': 'running_player',
                'path': 'assets/chars_sprites/{}/run/'.format(self.char_code),
                'repeat': True,
                'call': None
            },
            {
                'name': 'jumping_player',
                'path': 'assets/chars_sprites/{}/jump/'.format(self.char_code),
                'repeat': False,
                'call': None
            },
            {
                'name': 'dying_player',
                'path': 'assets/chars_sprites/{}/dead/'.format(self.char_code),
                'repeat': False,
                'call': self.die
            },
            {
                'name': 'falling_player',
                'path': 'assets/chars_sprites/{}/fall/'.format(self.char_code),
                'repeat': False,
                'call': None
            }
        ]

        self.animator = Animator.Animator(animations_data, self.sprite_size)

        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(self.animator.get_current_frame(), (0, 0))
        self.rect = self.surf.get_rect(x=self.position[0], y=self.position[1])

    def load_songs(self):
        self.jump_default_song = pygame.mixer.Sound('assets/general_songs/jump.mp3')

    def load_skills(self):
        skills_path = 'objects/skills/{}/'.format(self.char_code)

        for skill in os.listdir(skills_path):
            skill_name = skill.split('.')[0]

            if skill_name in self.skills:
                spec = importlib.util.spec_from_file_location(skill_name, skills_path + skill)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                self.skills[skill_name] = foo.Skill


    def load_lifes(self):
        self.lifes = []
        self.lifesAmount = self.maxLifes
        previous_pos = -50
        for i in range(0, self.maxLifes):
            previous_pos += 50
            heart = Heart(previous_pos)
            self.lifes.append(heart)

    def move(self, x, y):
        x = x * self.speed

        if x < 0:
            if not self.canBack:
                x = 0
            if not self.flipped:
                self.flipped = True

        if x > 0:
            if not self.canGo:
                x = 0
            if self.flipped:
                self.flipped = False

        if self.gravity > 0:
            y = 0 if not self.onTheGround else y

            if y < 0:
                self.isJumping = True
                self.animator.update_anim('jumping_player')
                self.play_song(self.jump_default_song)

            if self.isJumping:
                y = -1 * self.jumpForce
                self.jumpHeight -= y

            if self.jumpHeight >= self.maxJumpHeight:
                self.isJumping = False
                self.jumpHeight = 0
        else:
            if y < 0:
                y = y * self.speed

        self.rect.x += x
        self.rect.y += y

        if self.onTheGround and not self.isJumping:
            if x != 0:
                self.animator.update_anim('running_player')
            else:
                self.animator.update_anim('idle_player')

        if not self.onTheGround and not self.isJumping:
            self.animator.update_anim('falling_player')

    def update_state(self, x, y):
        if not self.dead:
            self.move(x, y)

        self.skills_move()
        self.animator.update_anim_frame()
        self.check_limits()
        self.check_effects()

    def use_skill(self, which):
        if not self.skills_cooldowns[which][2]:
            return

        skill_index = len(self.actived_skills)
        skill = self.skills[which](self, self.scene, skill_index)

        self.actived_skills.append(skill)

        pygame.time.set_timer(self.skills_cooldowns[which][0], self.skills_cooldowns[which][1])
        self.skills_cooldowns[which][2] = False

    def skills_move(self):
        for s in self.actived_skills:
            s.update_state()

    def play_song(self, which):
        which.play()

    def lose_life(self):
        if self.dead:
            return

        if self.lifesAmount > 0:
            if not self.intangible:
                self.lifesAmount -= 1
                self.lifes[self.lifesAmount].off()

                self.get_intangible()

        if self.lifesAmount == 0:
            self.dead = True
            self.animator.update_anim('dying_player')

    def check_cooldowns(self, event):
        if event.type == self.intangibility_event and self.intangible:
            self.intangible = False
            pygame.time.set_timer(self.intangibility_event, 0)

            return

        for k in self.skills_cooldowns:
            if k != 'Internals':
                if self.skills_cooldowns[k][0] == event.type:
                    self.skills_cooldowns[k][2] = True
                    pygame.time.set_timer(self.skills_cooldowns[k][0], 0)

                    return

        for i in self.skills_cooldowns['Internals']:
            if event.type == self.skills_cooldowns['Internals'][i][0]:
                pygame.time.set_timer(self.skills_cooldowns['Internals'][i][0], 0)
                self.skills_cooldowns['Internals'][i][1]()

    def get_intangible(self):
        pygame.time.set_timer(self.intangibility_event, self.intangibleTimer)
        self.intangible = True

    def check_limits(self):
        if self.rect.x <= 0:
            self.canBack = False
        else:
            self.canBack = True

        if self.rect.x >= self.scene.screen_size[0] - self.sprite_size[0]:
            self.canGo = False
        else:
            self.canGo = True

    def fall_due_gravity(self):
        if not self.isJumping and not self.onTheGround:
            self.rect.y += self.gravity

    def die(self):
        self.scene.gameEnd = True

    def check_effects(self):
        currentFrame = self.animator.get_current_frame()
        if self.intangible and not self.dead:
            self.intangibility_effect(currentFrame)
        else:
            currentFrame.set_alpha(255)
            self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
            self.surf.blit(currentFrame, (0,0))

    def intangibility_effect(self, currentFrame):
        currentFrame.set_alpha(127)
        self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
        self.surf.blit(currentFrame, (0,0))