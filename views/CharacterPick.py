from PyQt5 import QtWidgets, QtGui, QtCore
from controllers.Character import Character as Chars
from controllers.Styler import Styler as Styler
from controllers.SelectionPlayer import SelectionPlayer
from views import Game as GameFile
from functools import partial


class CharacterPick(QtWidgets.QMainWindow):
    window_width = 1024
    window_height = 700
    sounds = SelectionPlayer()

    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.characters_panel = QtWidgets.QWidget()
        self.characters_layout = QtWidgets.QGridLayout(self.characters_panel)

        self.setup()

    def pick_char(self, char_code, event):
        self.sounds.picked_character()
        char_code = char_code.split('.')[0]

        self.close()
        GameFile.Game(char_code)

    def show_chars(self):
        max_per_column = 3
        x = 0
        y = 0

        for c in Chars.get_all_icon():
            character_frame = QtWidgets.QWidget()
            character_frame.setFixedSize(80, 80)
            character_frame.setStyleSheet(Styler.char_icon_idle)
            character_frame.enterEvent = partial(Styler.char_icon_over, character_frame)
            character_frame.leaveEvent = partial(Styler.char_icon_leave, character_frame)
            character_frame.mousePressEvent = partial(self.pick_char, c['char_code'])
            character_icon = QtWidgets.QLabel(character_frame)
            character_icon.setStyleSheet('border: None')
            character_icon.setFixedSize(78, 78)
            character_icon.setPixmap(QtGui.QPixmap(c['icon_path']))
            character_icon.setScaledContents(True)
            self.characters_layout.addWidget(character_frame, x, y)

            x += 1

            if x > max_per_column:
                x = 0
                y += 1

    def setup(self):
        background_palette = QtGui.QPalette()
        background_image = QtGui.QPixmap('assets/general_sprites/pick_screen_background.jpg').scaled(self.window_width, self.window_height)
        background_palette.setBrush(10, QtGui.QBrush(background_image))

        self.setPalette(background_palette)
        self.setFixedSize(self.window_width, self.window_height)
        self.main_layout.setDirection(QtWidgets.QVBoxLayout.TopToBottom)
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.characters_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.characters_layout.setAlignment(QtCore.Qt.AlignTop)
        self.characters_panel.setFixedHeight(round(self.window_height/2))
        self.characters_panel.setStyleSheet('background-color: #FFFFFF; border: 5px solid #990099')

        self.main_layout.addWidget(self.characters_panel)
        self.setCentralWidget(self.central_widget)
        self.setPalette(background_palette)

        self.show_chars()