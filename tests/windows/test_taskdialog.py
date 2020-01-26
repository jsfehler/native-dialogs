from multiprocessing import Process, Pipe
import time

from utils import (
    get_visible_window_handles,
    AlertManager,
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


def close_alert(current_handles):
    manager = AlertManager(current_handles)
    manager.close()


def accept_alert(current_handles):
    manager = AlertManager(current_handles)
    manager.click(b'OK')


def get_button_text(current_handles, send_end):
    manager = AlertManager(current_handles)
    result = manager.get_button_names((b"Heaven or Hell", b"Let's Rock",))

    manager.close()

    send_end.send(result)


def test_alert_return_value(request):
    """When an alert is closed, Then the return value is correct."""
    connections = []

    def close_connections():
        for c in connections:
            c.close()

    request.addfinalizer(close_connections)

    # dialog.alert() blocks until closed. Run it in a one process and
    # close it from another.
    current_handles = get_visible_window_handles()

    recv_end, send_end = Pipe(False)
    connections.append(recv_end)
    connections.append(send_end)
    a = Process(target=create_alert, args=(send_end,))
    b = Process(target=close_alert, args=[current_handles])

    a.start()
    time.sleep(0.1)
    b.start()

    result = recv_end.recv()

    assert 2 == result


def test_alert_accept(request):
    """When an alert is accepted, Then the return value is correct."""
    connections = []

    def close_connections():
        for c in connections:
            c.close()

    request.addfinalizer(close_connections)
    # dialog.alert() blocks until closed. Run it in a one process and
    # close it from another.
    current_handles = get_visible_window_handles()

    recv_end, send_end = Pipe(False)
    connections.append(recv_end)
    connections.append(send_end)
    a = Process(target=create_alert, args=(send_end,))
    b = Process(target=accept_alert, args=[current_handles])

    a.start()
    time.sleep(0.1)
    b.start()

    result = recv_end.recv()

    assert 0 == result


def test_alert_button_custom_text(request):
    """If an alert has buttons names customized, they should appear."""
    connections = []

    def close_connections():
        for c in connections:
            c.close()

    request.addfinalizer(close_connections)
    # dialog.alert() blocks until closed. Run it in a one process and
    # close it from another.
    current_handles = get_visible_window_handles()

    alert_recv, alert_end = Pipe(False)
    connections.append(alert_recv)
    connections.append(alert_end)
    a = Process(target=create_alert_custom_buttons, args=(alert_end,))
    button_recv, button_end = Pipe(False)
    connections.append(button_recv)
    connections.append(button_end)
    b = Process(target=get_button_text, args=[current_handles, button_end])

    a.start()
    time.sleep(0.1)
    b.start()

    _ = alert_recv.recv()
    result = button_recv.recv()
    assert b"Heaven or Hell" in result
    assert b"Let's Rock" in result
