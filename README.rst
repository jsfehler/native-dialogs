NativeDialogs
==============
Zero-dependency, 100% cross-platform API for opening native dialog windows from Python.

Supported Platforms:

- Windows

- OSX

- Linux

Usage
-----

.. code-block:: python

    from NativeDialogs import dialogs


    dialogs.alert(
        text="Brittle bones, packed in decaying flesh.",
        title="I see you.",
        buttons=('Bring It On', 'Oh Hell No'),
    )


How does it work?
-----------------

- Windows >= Vista: ctypes + Windows API to open a TaskDialog.
- Windows <= XP: ctypes + Windows API to open a MessageBoxA.
- OSX: Applescript to open an Alert.
- Linux: ctypes + Xlib to open a window (Styled to look like a dialog).

Running the tests
-----------------

Testing is done using tox and pytest.

Due to the nature of this package, you can't run all the tests on one operating system.
Use windows/osx/linux environments to filter the tests.


.. code-block:: bash

    tox -e windows

FAQ
---

Is this a full featured GUI library?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lord, I hope not. Sufficiently complex use cases should roll their own tools.

Only a subset of any particular platform's dialog abilities are exposed in the
goal of providing a consistent API.

NativeDialogs is for situations where you:

1 - Reliably need an alert message on multiple platforms

2 - Have limited options for including dependencies


Why not use GUI libraries like tkinter, GTK, Qt, wxWidgets, etc?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cross-platform, but not always present.
Also, they won't run from inside game engines like `Ren'Py <https://renpy.org/>`_.


What about EasyDialogs from the standard library?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not cross-platform, removed in python 3, and won't run on macOS Catalina.


But Linux doesn't have a native dialog window?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Including an .so file to open a custom window is as close as you can get.
No GTK or Zenity here.


Why not use pywin32, PyObjC, or python-xlib?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It wouldn't be zero-dependency then, would it? Silly billy.


Can you add an input, file chooser, etc?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you build a Linux version from scratch using C and Xlib, then yeah, sure. Good luck, bucko.
