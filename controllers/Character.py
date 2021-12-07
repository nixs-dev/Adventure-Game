import os


class Character:

    chars_icon = 'assets\\chars_icon\\'
    skills_icon = 'assets\\skills_icons\\'

    @staticmethod
    def get_all_icon():
        chars = []

        for c in os.listdir(Character.chars_icon):
            full_path = (Character.chars_icon + c).replace('\\', '/')
            chars.append({
                'icon_path': full_path,
                'char_code': c
            })

        return chars

    @staticmethod
    def get_skill_icons_paths(player_code):
        player_specific_path = Character.skills_icon + player_code + '\\'
        skills = {}

        for file in os.listdir(player_specific_path):
            without_ext = file.split('.')[0]

            skills[without_ext] = player_specific_path + file

        return skills
