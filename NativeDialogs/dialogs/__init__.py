import sys


if sys.platform == "win32":
    from .win import alert

elif sys.platform == 'darwin':
    from .osx import alert

elif sys.platform.startswith('linux'):
    from .linux import alert

else:
    raise ImportError('Current platform does not support NativeDialogs')


__all__ = [
    "alert",
]
