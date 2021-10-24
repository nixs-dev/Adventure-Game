import os


class Character:

    chars_icon = 'assets\\chars_icon\\'


    def get_all_icon():
        chars = []

        for c in os.listdir(Character.chars_icon):
            full_path = (Character.chars_icon + c).replace('\\', '/')
            chars.append({
                'icon_path': full_path,
                'char_code': c
            })

        return chars