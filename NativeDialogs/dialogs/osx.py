from subprocess import Popen, PIPE


def _run_applescript(script):
    """Runs applescript and returns the result.

    Returns:
        tuple
    """
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(bytes(script, encoding='utf8'))
    return (p.returncode, stdout, stderr)


def alert(text, title='', buttons=('OK',)):
    script = 'display alert "{}" message "{}" buttons {{}}'.format(title, text, buttons)
    return _run_applescript(script)
