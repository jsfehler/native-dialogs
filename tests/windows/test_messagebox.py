from multiprocessing import Process, Pipe
import time

from utils import get_visible_window_handles, close_alert

from NativeDialogs.dialogs.win import messagebox


def create_alert(send_end):
    result = messagebox.alert("Sultry Text", "Charming Title")
    send_end.send(result)


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
