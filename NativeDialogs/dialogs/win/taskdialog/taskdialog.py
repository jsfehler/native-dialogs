from ctypes import (
    byref,
    c_int,
    c_void_p,
    sizeof,
    windll,
)

from .const import (
    TDF_ALLOW_DIALOG_CANCELLATION,
    TDN_CREATED,
    WM_SETICON,
    ICON_BIG,
    ICON_SMALL,
)

from .taskdialogconfig import (
    PFTASKDIALOGCALLBACK, TASKDIALOGCONFIG, TASKDIALOG_BUTTON,
)


TaskDialogIndirect = windll.comctl32.TaskDialogIndirect
TaskDialogIndirect.restype = c_void_p

SendMessage = windll.user32.SendMessageW


def task_dialog_callback(hwnd, message, wParam, lParam, lpRefData):
    if message == TDN_CREATED:
        SendMessage(hwnd, WM_SETICON, ICON_BIG, c_void_p())
        SendMessage(hwnd, WM_SETICON, ICON_SMALL, c_void_p())


callback = PFTASKDIALOGCALLBACK(task_dialog_callback)

conf_size = sizeof(TASKDIALOGCONFIG)


def alert(text, title='', buttons=('OK',)):
    config = TASKDIALOGCONFIG()
    config.cbSize = conf_size
    config.hwndParent = c_void_p()
    config.pszWindowTitle = title
    config.pszContent = text

    # Disable the system menu for consistency
    config.pfCallback = callback
    config.dwFlags = TDF_ALLOW_DIALOG_CANCELLATION

    # Add custom buttons
    buttons_list = []
    for index, item in enumerate(buttons):
        b = TASKDIALOG_BUTTON()
        b.nButtonID = index
        b.pszButtonText = item
        buttons_list.append(b)

    num_buttons = len(buttons_list)
    config.cButtons = num_buttons
    config.pButtons = (TASKDIALOG_BUTTON * num_buttons)(*buttons_list)

    button = c_int()

    TaskDialogIndirect(
        byref(config),
        byref(button),
        byref(c_int()),
        byref(c_int()),
    )

    return button.value
