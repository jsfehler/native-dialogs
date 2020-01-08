NativeDialogs
==============
Zero-dependency, cross-platform API for opening native dialog windows from Python.

Supported Platforms:

- Windows

- OSX

- Linux

Usage
-----

.. code-block:: python

   from NativeDialogs import dialog


   dialog.alert('Dialog text', 'Dialog title')

How does it work?
-----------------

- Windows: ctypes + Windows API to open a MessageBoxA
- OSX: Applescript to open an Alert
- Linux: ctypes + Xlib to open a window styled to look like a MessageBox

FAQ
---

Why not use GUI libraries like tkinter, GTK, Qt, wxWidgets, etc?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cross-platform, but not always present. Also, they won't run inside game engines like `Ren'Py <https://renpy.org/>`_.


What about EasyDialogs from the standard library?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not cross-platform, removed in python 3 and won't run on macOS Catalina.


But Linux doesn't have a native dialog window?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Including an .so file to open a custom window is as close as you can get.


Why not use pywin32, PyObjC, or python-xlib?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It wouldn't be zero-dependency then, would it? Silly billy. Sufficiently complex use cases will have to roll their own tools..

