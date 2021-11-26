import pygame
import os


class Animator:

    animations = {}
    frames_paths = {}
    repeat_anims = {}
    current_frame = []
    anims_calls = {}
    frames_size = [0, 0]

    def __init__(self, animations_info, frames_size):
        self.animations = {}
        self.frames_paths = {}
        self.repeat_anims = {}
        self.current_frame = []
        self.anims_calls = {}
        self.frames_size = frames_size

        for anim in animations_info:
            self.animations[anim['name']] = []
            self.frames_paths[anim['name']] = anim['path']
            self.repeat_anims[anim['name']] = anim['repeat']
            self.anims_calls[anim['name']] = anim['call']

        self.load_anims()
        first_anim = list(self.animations.keys())[0]
        self.currentAnimation = [first_anim, 0, self.repeat_anims[first_anim], self.anims_calls[first_anim]]

    def update_anim(self, which_one):
        if self.currentAnimation[0] != which_one:
            self.currentAnimation = [which_one, 0, self.repeat_anims[which_one], self.anims_calls[which_one]]

    def fix_sprite_list(self, origin, list_):
        temp_list = []
        final_list = []

        for i in list_:
            num = i.replace('.png', '')
            num = int(num)
            temp_list.append(num)

        temp_list = sorted(temp_list, key=int)

        for i in temp_list:
            item = origin + str(i) + '.png'
            item = pygame.image.load(item)
            item = pygame.transform.scale(item, self.frames_size)
            final_list.append(item)

        return final_list

    def load_anims(self):
        for k in self.frames_paths:
            self.animations[k] = self.fix_sprite_list(self.frames_paths[k], os.listdir(self.frames_paths[k]))

    def update_anim_frame(self):
        current_frame = self.currentAnimation[1]

        try:
            self.currentAnimation[1] += 1
            next_frame = self.animations[self.currentAnimation[0]][self.currentAnimation[1]]
        except IndexError:
            if self.currentAnimation[2]:
                self.currentAnimation[1] = 0
                next_frame = self.animations[self.currentAnimation[0]][self.currentAnimation[1]]
            else:
                next_frame = self.animations[self.currentAnimation[0]][current_frame]
                self.currentAnimation[1] = current_frame
                self.currentAnimation[3]() if self.currentAnimation[3] is not None else 0

    def get_current_frame(self):
        return self.animations[self.currentAnimation[0]][self.currentAnimation[1]]