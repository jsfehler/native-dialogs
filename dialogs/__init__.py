import sys


if sys.platform == "win32":
    from .win import *

elif sys.platform == 'darwin':
    from .osx import *

elif sys.platform == 'linux':
    from .linux import *

else:
    raise ImportError('Current platform does not support NativeDialogs')


__all__ = [
    "alert",
]
