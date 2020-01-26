from ctypes import (
    c_int,
    c_long,
    c_uint,
    c_ushort,
    c_wchar_p,
    c_void_p,
    POINTER,
    Structure,
    Union,
    WINFUNCTYPE,
)


PFTASKDIALOGCALLBACK = WINFUNCTYPE(
    c_void_p, c_void_p, c_uint, c_uint, c_long, c_long,
)


class TASKDIALOG_BUTTON(Structure):
    _fields_ = [
        ('nButtonID', c_int),
        ('pszButtonText', c_wchar_p),
    ]


class FOOTERICON(Union):
    _fields_ = [
        ("hFooterIcon", c_void_p),
        ("pszFooterIcon", c_ushort),
    ]


class MAINICON(Union):
    _fields_ = [
        ("hMainIcon", c_void_p),
        ("pszMainIcon", c_ushort),
    ]


class TASKDIALOGCONFIG(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("hwndParent", c_void_p),
        ("hInstance", c_void_p),
        ("dwFlags", c_uint),
        ("dwCommonButtons", c_uint),
        ("pszWindowTitle", c_wchar_p),
        ("uMainIcon", MAINICON),
        ("pszMainInstruction", c_wchar_p),
        ("pszContent", c_wchar_p),
        ("cButtons", c_uint),
        ("pButtons", POINTER(TASKDIALOG_BUTTON)),
        ('nDefaultButton', c_int),
        ('cRadioButtons', c_uint),
        ('pRadioButtons', POINTER(TASKDIALOG_BUTTON)),
        ('nDefaultRadioButton', c_int),
        ('pszVerificationText', c_wchar_p),
        ('pszExpandedInformation', c_wchar_p),
        ('pszExpandedControlText', c_wchar_p),
        ('pszCollapsedControlText', c_wchar_p),
        ('uFooterIcon', FOOTERICON),
        ('pszFooter', c_wchar_p),
        ('pfCallback', PFTASKDIALOGCALLBACK),
        ('lpCallbackData', c_long),
        ('cxWidth', c_uint),
    ]
