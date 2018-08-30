import pytest

from .context import mock, builtin_str

@pytest.fixture(scope='function')
def func():
    def dummy(*agrs, **kwargs):
        pass
    f = mock.create_autospec(spec=dummy, name='fixture_function_to_decorate')
    return f

@pytest.fixture(scope='function', autouse=True)
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def mocked_open(mock_open):
    # mock_file = mock.Mock()
    # mock_file.write.return_value = None
    # mock_file.read.return_value = None
    # mock_open.return_value = mock_file
    return mock_open
