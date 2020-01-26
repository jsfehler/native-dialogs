import sys


if sys.platform == "win32":
    # If older than Windows Vista, use a MessageBox instead
    try:
        from .win.taskdialog.taskdialog import alert
    except:
        from .win.messagebox import alert

elif sys.platform == 'darwin':
    from .osx import alert

elif sys.platform.startswith('linux'):
    from .linux import alert

else:
    raise ImportError('Current platform does not support NativeDialogs')


__all__ = [
    "alert",
]
