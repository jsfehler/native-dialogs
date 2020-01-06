import os.path


from ctypes import *


file_path = os.path.abspath(os.path.dirname(__file__))
x11_dialog = CDLL(os.path.join(file_path, 'x11_dialog.so'))


def alert(text, title='', buttons=('OK',)):
    return x11_dialog.MessageBox(text, title)
