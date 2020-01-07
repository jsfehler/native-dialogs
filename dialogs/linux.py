from ctypes import *
import os.path


def _get_file_path():
    cwd = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(cwd, 'x11_dialog.so')


x11_dialog = CDLL(_get_file_path())


def alert(text, title='', buttons=('OK',)):
    text = bytes(text, encoding='utf-8')
    title = bytes(title, encoding='utf-8')
    
    message_box = x11_dialog.MessageBox
    message_box.argtypes = [c_char_p, c_char_p]
    return message_box(text, title)
