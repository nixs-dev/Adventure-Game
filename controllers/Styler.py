class Styler:

    char_icon_idle = 'border: 1px solid #000000'
    char_icon_selected = 'border: 3px solid #FF00FF'

    @staticmethod
    def char_icon_over(elem, event):
        elem.setStyleSheet(Styler.char_icon_selected)

    @staticmethod
    def char_icon_leave(elem, event):
        elem.setStyleSheet(Styler.char_icon_idle)
