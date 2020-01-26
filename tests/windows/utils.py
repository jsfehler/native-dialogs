from ctypes import windll, WINFUNCTYPE, c_buffer, c_int, POINTER


BM_CLICK = 0x00F5
WM_CLOSE = 0x0010

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


class AlertManager:
    def __init__(self, current_handles):
        self.handle = self.get_handle(current_handles)

    def get_handle(self, current_handles):
        new_handles = get_visible_window_handles()
        # To find the handle for the alert, diff before and after opening it.
        diff = list(set(new_handles) - set(current_handles))

        return diff[0]

    def get_child_handles(self, expected_button_text):
        """Get the handles for a dialog's buttons.

        Arguments:
            parent_handle: Handle for the parent window
            expected_button_text: List of button text.

        """
        result = []

        def callback(hwnd, lParam):
            title = c_buffer(b" " * 256)
            windll.user32.GetWindowTextA(hwnd, title, 255)

            if title.value in expected_button_text:
                result.append(hwnd)
            return True

        windll.user32.EnumChildWindows(
            self.handle, EnumChildProc(callback), 0,
        )
        return result

    def get_button_names(self, expected_button_text):
        button_names = []
        handles = self.get_child_handles(expected_button_text)

        for hwnd in handles:
            title = c_buffer(b" " * 256)
            windll.user32.GetWindowTextA(hwnd, title, 255)
            button_names.append(title.value)

        return button_names

    def click(self, button_text):
        """Click a button in the alert."""
        child_handles = self.get_child_handles([button_text])
        windll.user32.SendMessageA(child_handles[0], BM_CLICK, 0, 0)

    def close(self):
        """Close the dialog, as opposed to clicking a button."""
        windll.user32.SendMessageA(self.handle, WM_CLOSE, 0, 0)
