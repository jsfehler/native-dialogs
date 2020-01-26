from ctypes import windll, WINFUNCTYPE, c_buffer, c_int, POINTER


EnumWindowsProc = WINFUNCTYPE(c_int, c_int, c_int)
EnumChildProc = WINFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))


def get_visible_window_handles():
    """Returns handles to windows with matching titles"""
    hwnds = []

    """Close the last window that was opened. We expect it to be the dialog."""
    def callback(hwnd, lparam, hwnds=hwnds):
        if windll.user32.IsWindowVisible(hwnd):
            hwnds.append(hwnd)

        return True

    windll.user32.EnumWindows(EnumWindowsProc(callback), 0)

    return hwnds


def close_alert(handles):
    new_handles = get_visible_window_handles()

    # To find the handle for the alert, diff before and after opening it.
    diff = list(set(new_handles) - set(handles))

    # Close alert
    windll.user32.SendMessageA(diff[0], 0x0010, 0, 0)  # WM_CLOSE


def get_dialog_button_names(parent_handle):
    result = []

    def callback(hwnd, lParam):
        title = c_buffer(b" " * 256)
        windll.user32.GetWindowTextA(hwnd, title, 255)

        result.append(title.value)
        return True

    windll.user32.EnumChildWindows(parent_handle, EnumChildProc(callback), 0)

    return result
