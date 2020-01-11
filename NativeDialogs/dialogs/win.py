from ctypes import windll


MessageBoxA = windll.user32.MessageBoxA

MB_TASKMODAL = 0x2000


def alert(text, title='', buttons=('OK',)):
    return MessageBoxA(
        0,
        bytes(str(text).encode("utf-8")),
        bytes(str(title).encode("utf-8")),
        MB_TASKMODAL,
    )
