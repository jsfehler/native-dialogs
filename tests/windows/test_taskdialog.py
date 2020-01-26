from multiprocessing import Process, Pipe
import time

from utils import (
    get_visible_window_handles,
    close_alert,
    get_dialog_button_names,
)

from NativeDialogs.dialogs.win.taskdialog import taskdialog


def create_alert(send_end):
    result = taskdialog.alert("Sultry Text", "Charming Title")
    send_end.send(result)


def create_alert_custom_buttons(send_end):
    result = taskdialog.alert(
        "Sultry Text",
        title="Charming Title",
        buttons=("Heaven or Hell", "Let's Rock",),
    )
    send_end.send(result)


def get_button_text(handles, send_end):
    new_handles = get_visible_window_handles()

    # To find the handle for the alert, diff before and after opening it.
    diff = list(set(new_handles) - set(handles))

    result = get_dialog_button_names(diff[0])

    close_alert(handles)

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

    assert 2 == result


def test_alert_button_custom_text():
    """If an alert has buttons names customized, they should appear."""

    # dialog.alert() blocks until closed. Run it in a one process and
    # close it from another.
    current_handles = get_visible_window_handles()

    alert_recv, alert_end = Pipe(False)
    a = Process(target=create_alert_custom_buttons, args=(alert_end,))
    button_recv, button_end = Pipe(False)
    b = Process(target=get_button_text, args=[current_handles, button_end])

    a.start()
    time.sleep(0.1)
    b.start()

    _ = alert_recv.recv()
    result = button_recv.recv()
    assert b"Heaven or Hell" in result
    assert b"Let's Rock" in result
