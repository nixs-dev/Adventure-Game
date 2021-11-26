import pygame
import os
import random
from objects.hosts.Player import Player
from objects.hosts.monsters.Monster_Mushroom import Mushroom
from objects.hosts.monsters.Evil_Wolf import Wolf
from objects.Ground import Ground
from objects.GameOverFrame import GameOverFrame, TryAgainButton
from objects.WinnerFrame import WinnerFrame, PlayAgainButton


class Game:
    player = None
    current_player_code = ''
    current_scene_code = ''
    ground = None
    scene_song = None
    screen_size = [1024, 500]
    monsterAmount = 5
    monsters = []
    currentMonster = None
    gameEnd = False
    gameOver = None
    winner_frame = None
    tryAgainButton = None
    playAgainButton = None

    background_size = (screen_size[0] * 3, screen_size[1])
    parallaxBackgroundPosition = [0, 0]

    screen = None
    background = pygame.image.load('assets/general_sprites/background.png')
    background = pygame.transform.scale(background, background_size)
    canRun = True

    def __init__(self, char_code, scene_code='default_scene'):
        pygame.init()

        self.screen = pygame.display.set_mode(self.screen_size)
        self.current_player_code = char_code
        self.current_scene_code = scene_code
        self.load_initial_world_data()

        while self.canRun:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.canRun = False

                self.player.check_cooldowns(event) if not self.gameEnd else 0
                self.tryAgainButton.checkClick(event, self) if self.gameOver is not None else 0

            self.parallax_update()
            self.draw_world()

            ##OBJECTS ACTIONS###
            if not self.gameEnd:
                self.draw_player()
                self.draw_monsters()
                self.check_collision()
                self.objets_movement()
            else:
                self.check_game_result()

            pygame.display.flip()
            pygame.time.Clock().tick(40)

        pygame.quit()

    def load_initial_world_data(self):
        self.monsters = []
        self.currentMonster = None
        self.gameEnd = False
        self.gameOver = None
        self.winner_frame = None
        self.tryAgainButton = None
        self.playAgainButton = None
        self.canRun = True
        self.player = Player(self, self.current_player_code)
        self.ground = Ground(self.screen_size)
        self.load_monsters()
        self.start_scene_song()

    def check_game_result(self):
        if len(self.monsters) == 0:
            self.draw_winner_frame()
        else:
            self.draw_game_over()

    def start_scene_song(self):
        self.scene_song.stop() if self.scene_song is not None else 0

        songs_path = 'assets/scenes_songs/'
        song = ''

        for s in os.listdir(songs_path):
            if s.split('.')[0] == self.current_scene_code:
                song = songs_path + s
                break

        self.scene_song = pygame.mixer.Sound(song)
        self.scene_song.play(loops=10)
        self.scene_song.set_volume(0.3)

    def parallax_update(self):
        self.parallaxBackgroundPosition[0] -= 5

        if -self.parallaxBackgroundPosition[0] + self.screen_size[0] >= self.background_size[0]:
            self.parallaxBackgroundPosition[0] = 0

    def draw_game_over(self):
        self.gameOver = GameOverFrame(self.screen_size)
        self.tryAgainButton = TryAgainButton(self.screen_size)

        self.screen.blit(self.gameOver.surf, self.gameOver.rect)
        self.screen.blit(self.tryAgainButton.surf, self.tryAgainButton.rect)

    def draw_winner_frame(self):
        self.winner_frame = WinnerFrame(self.screen_size)
        self.playAgainButton = PlayAgainButton(self.screen_size)

        self.screen.blit(self.winner_frame.surf, self.winner_frame.rect)
        self.screen.blit(self.playAgainButton.surf, self.playAgainButton.rect)

    def load_monsters(self):
        avaible_monsters = [Mushroom, Wolf]

        for i in range(0, self.monsterAmount):
            random_monster = random.randint(0, len(avaible_monsters)-1)
            new_monster = avaible_monsters[random_monster](self)
            self.monsters.append(new_monster)

    def check_collision(self):
        self.player.onTheGround = pygame.sprite.collide_rect(self.player, self.ground)
        self.currentMonster.onTheGround = pygame.sprite.collide_rect(self.currentMonster, self.ground)
        self.player.lose_life() if pygame.sprite.collide_rect(self.currentMonster, self.player) else 0

        for skill in self.player.actived_skills:
            if pygame.sprite.collide_rect(self.currentMonster, skill) and skill.damage > 0:
                skill.destroy()
                self.currentMonster.die()
                break

    def objets_movement(self):
        self.player.fall_due_gravity()
        self.currentMonster.fallDueGravity()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.player.update_state(1, -1)
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.player.update_state(-1, -1)
        else:
            if keys[pygame.K_UP]:
                self.player.update_state(0, -1)
            elif keys[pygame.K_RIGHT]:
                self.player.update_state(1, 0)
            elif keys[pygame.K_LEFT]:
                self.player.update_state(-1, 0)
            else:
                self.player.update_state(0, 0)

        if keys[pygame.K_q]:
            self.player.use_skill('damage_skill')
        elif keys[pygame.K_f]:
            self.player.use_skill('scape_skill')

        self.currentMonster.update_state()

    def draw_world(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, self.parallaxBackgroundPosition)
        self.screen.blit(self.ground.surf, self.ground.rect)

    def draw_monsters(self):
        try:
            self.currentMonster = self.monsters[0]
            self.screen.blit(self.currentMonster.surf, self.currentMonster.rect)
        except IndexError:
            self.gameEnd = True

    def draw_player(self):
        if not self.player.flipped:
            self.screen.blit(self.player.surf, self.player.rect)
        else:
            self.screen.blit(pygame.transform.flip(self.player.surf, True, False), self.player.rect)

        for i in self.player.lifes:
            self.screen.blit(i.surf, i.rect)

        for i in self.player.actived_skills:
            i.blit_skill()
