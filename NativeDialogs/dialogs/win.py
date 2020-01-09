from ctypes import windll


MessageBoxA = windll.user32.MessageBoxA

MB_TASKMODAL = 0x2000


def alert(text, title='', buttons=('OK',)):
    return MessageBoxA(
        0,
        bytes(text, encoding='utf-8'),
        bytes(title, encoding='utf-8'),
        MB_TASKMODAL,
    )
