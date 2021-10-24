import PyQt5.QtCore as C
import PyQt5.QtMultimedia as M


class SelectionPlayer(M.QMediaPlayer):
    picked_character_song = 'assets/general_songs/char_picked.wav'

    def __init__(self):
        super().__init__()

    def picked_character(self):
        url = C.QUrl.fromLocalFile(self.picked_character_song)
        content = M.QMediaContent(url)
        self.setMedia(content)
        self.play()



