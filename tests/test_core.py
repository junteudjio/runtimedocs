# -*- coding: utf-8 -*-

import os
import pytest

from .context import mock, builtin_str, runtimedocs
from .fixtures import func

@pytest.mark.parametrize('force_enable_runtimedocs', [True, False])
@mock.patch.dict(os.environ, {'DISABLE_RUNTIMEDOCS': '1'})
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_disable_runtimedocs_env_var(mock_open, force_enable_runtimedocs, func):
    #arrange
    decorated_func = runtimedocs.core.runtimedocs(force_enable_runtimedocs=force_enable_runtimedocs)(func)

    #call
    decorated_func()

    #assert
    if force_enable_runtimedocs:
        #if DISABLE_RUNTIMEDOCS and force_enable_runtimedocs is True then we should call the runtimedocs decorator
        #and that decorator uses the logging module which should write at least one file to the file system.
        mock_open.assert_called()
    else:
        # otherwise the original function will not be decorated
        mock_open.assert_not_called()


@pytest.mark.parametrize('verbosity', [0, 1])
@mock.patch('sys.stdout')
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_verbosity_level(mock_open, mock_stdout, verbosity, func):
    #arrange
    decorated_func = runtimedocs.core.runtimedocs(verbosity=verbosity)(func)

    #call
    decorated_func()

    #assert
    if verbosity == 0:
        mock_stdout.assert_not_called
    else:
        mock_stdout.assert_called

@pytest.mark.parametrize('exception_to_raise', [ValueError, ZeroDivisionError, NameError])
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_runtimedocs_reraises_catched_exceptions(mock_open, exception_to_raise, func):
    # arrange
    func.side_effect = exception_to_raise
    decorated_func = runtimedocs.core.runtimedocs()(func)

    # call & assert
    with pytest.raises(exception_to_raise):
        decorated_func()


@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_custom_logger_name(mock_open, func):
    # arrange
    decorated_func = runtimedocs.core.runtimedocs(custom_logger_name='custom_logger_name')(func)

    # call
    decorated_func()

    # assert
    saved_filepath = os.path.join(os.getcwd(), 'custom_logger_name.runtimedocs.log')
    mock_open.assert_called_once_with(saved_filepath, 'a', encoding=None)





