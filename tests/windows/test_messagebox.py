from multiprocessing import Process, Pipe
import time

from utils import get_visible_window_handles, AlertManager

from NativeDialogs.dialogs.win import messagebox


def create_alert(send_end):
    result = messagebox.alert("Sultry Text", "Charming Title")
    send_end.send(result)


def close_alert(current_handles):
    manager = AlertManager(current_handles)
    manager.close()


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

    assert 1 == result
