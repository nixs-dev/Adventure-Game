from PyQt5 import QtWidgets
from views.CharacterPick import CharacterPick
import sys

app = QtWidgets.QApplication(sys.argv)
window = CharacterPick()
window.setup()
window.show()
sys.exit(app.exec_())