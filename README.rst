native-dialogs
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

Why not use tkinter, GTK, Qt, wxWidgets, etc?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cross-platform, but not always present. Also, they won't run inside Ren'Py.

What about EasyDialogs?
~~~~~~~~~~~~~~~~~~~~~~~

Removed in python 3 and won't run on macOS Catalina.

Why not use pywin32, PyObjC, or python-xlib?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It wouldn't be zero-dependency then, would it?
