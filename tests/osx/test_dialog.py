from NativeDialogs import dialogs


def mock_run_applescript(script):
    """Don't actually run any applescript in the unit tests, ya dingbat.

    This function should return whatever type of object
    dialogs._run_applescript returns.

    Returns:
        tuple
    """
    return (1, "", "")


# Monkey patch
dialogs._run_applescript = mock_run_applescript


def test_alert_return_value():
    """When an alert is closed, Then the return value is correct."""

    result = dialogs.alert("text", "title")

    assert tuple == type(result)
