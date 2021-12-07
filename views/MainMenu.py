import pygame
import sys
from PyQt5 import QtWidgets
from views.CharacterPick import CharacterPick
from utils.Animator import Animator


class MainMenu:
    scene_song = None
    screen_size = [1024, 500]
    title_font = None
    option_font = None
    pointer_surf = None
    pointer_rect = None
    background_size = (screen_size[0], screen_size[1])
    pointer_sprite_size = [30, 30]

    screen = None
    background_animator = None
    canRun = True

    options = []
    selected_option = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)

        self.title_font = pygame.font.Font('assets/fonts/Collegiate.ttf', 70)
        self.option_font = pygame.font.Font('assets/fonts/Collegiate.ttf', 30)

        pointer_sprite = pygame.image.load('assets/main_menu/selector.png')
        pointer_sprite = pygame.transform.scale(pointer_sprite, self.pointer_sprite_size)

        self.pointer_surf = pygame.Surface(self.pointer_sprite_size, pygame.SRCALPHA)
        self.pointer_surf.blit(pointer_sprite, (0, 0))
        self.pointer_rect = self.pointer_surf.get_rect()

        self.options = [
            {
                'name': 'Start',
                'placed_on': [0, 0],
                'callback': self.start_game,
            },
            {
                'name': 'Options',
                'object': None,
                'placed_on': [0, 0],
                'callback': None,
            }
        ]
        animations_data = [
            {
                'name': 'idle_background',
                'path': 'assets/main_menu/background/',
                'repeat': True,
                'call': None
            }
        ]

        self.background_animator = Animator(animations_data, self.background_size)

        while self.canRun:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.canRun = False

            self.draw_world()
            self.change_option()

            pygame.display.flip()
            pygame.time.Clock().tick(20)

        pygame.quit()

    def start_game(self):
        app = QtWidgets.QApplication(sys.argv)
        cp_window = CharacterPick()

        pygame.quit()
        cp_window.show()

        sys.exit(app.exec_())

    def change_option(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.selected_option -= 1
        elif keys[pygame.K_DOWN]:
            self.selected_option += 1
        elif keys[pygame.K_RETURN]:
            self.options[self.selected_option]['callback']()

        if self.selected_option < 0:
            self.selected_option = len(self.options)-1
        elif self.selected_option > len(self.options)-1:
            self.selected_option = 0

    def draw_options(self):
        spacing = 40
        x_offset = 40
        before_y = self.screen_size[1]//2

        for index, option in enumerate(self.options):
            option_surf = self.option_font.render(option['name'], True, (255, 128, 0))
            option_rect = option_surf.get_rect()

            option_rect.x = x_offset
            option_rect.y = before_y + spacing

            self.screen.blit(option_surf, option_rect)

            self.options[index]['placed_on'] = [option_rect.x, option_rect.y]
            before_y += spacing

    def draw_world(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background_animator.get_current_frame(), (0, 0))

        title_surf = self.title_font.render('Adventure Game', True, (255, 255, 0))
        title_rect = title_surf.get_rect()
        self.screen.blit(title_surf, title_rect)

        self.draw_options()

        self.pointer_rect.y = self.options[self.selected_option]['placed_on'][1]
        self.screen.blit(self.pointer_surf, self.pointer_rect)

        self.background_animator.update_anim_frame()