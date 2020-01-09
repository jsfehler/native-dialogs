from ctypes import windll


MessageBoxA = windll.user32.MessageBoxA

MB_TASKMODAL = 0x00002000L


def alert(text, title='', buttons=('OK',)):
    return MessageBoxA(
        0,
        bytes(text),
        bytes(title),
        MB_TASKMODAL,
    )
