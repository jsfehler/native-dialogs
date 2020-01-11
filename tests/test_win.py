from ctypes import windll, WINFUNCTYPE, c_buffer, c_int
from multiprocessing import Process, Pipe
import time

from NativeDialogs import dialogs


EnumWindowsProc = WINFUNCTYPE(c_int, c_int, c_int)


def get_visible_window_handles():
    """Returns handles to windows with matching titles"""
    hwnds = []

    """Close the last window that was opened. We expect it to be the dialog."""
    def callback(hwnd, lparam, hwnds=hwnds):
        title = c_buffer(b" " * 256)
        windll.user32.GetWindowTextA(hwnd, title, 255)

        if windll.user32.IsWindowVisible(hwnd):
            hwnds.append(hwnd)

        return True

    windll.user32.EnumWindows(EnumWindowsProc(callback), 0)

    return hwnds


def create_alert(send_end):
    result = dialogs.alert("Sultry Text", "Charming Title")
    send_end.send(result)


def close_alert(handles):
    new_handles = get_visible_window_handles()

    # To find the handle for the alert, diff before and after opening it.
    diff = list(set(new_handles) - set(handles))

    # Close alert
    windll.user32.SendMessageA(diff[0], 0x0010, 0, 0)  # WM_CLOSE


def test_alert_return_value():
    """When an alert is closed, Then the return value is correct."""

    # dialog.alert() blocks until closed. Run it in a one process and
    # close it from another.
    current_handles = get_visible_window_handles()

    recv_end, send_end = Pipe(False)
    a = Process(target=create_alert, args=(send_end,))
    b = Process(target=close_alert, args=[current_handles])

    a.start()
    time.sleep(0.1)
    b.start()

    result = recv_end.recv()

    assert 1 == result
