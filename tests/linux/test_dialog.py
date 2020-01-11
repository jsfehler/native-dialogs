from NativeDialogs.dialogs.linux import _get_file_path


def test_get_file_path():
    result = _get_file_path('foo.bar')
    assert 'foo.bar' in result
