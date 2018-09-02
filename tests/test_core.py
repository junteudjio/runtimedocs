# -*- coding: utf-8 -*-

import os
from io import StringIO
import logging

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
        assert mock_open.call_count > 0
    else:
        # otherwise the original function will not be decorated
        assert mock_open.call_count == 0


@pytest.mark.parametrize('verbosity', [0, 1])
@mock.patch('sys.stdout', new_callable=StringIO)
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_verbosity_level(mock_open, mock_stdout, verbosity, func):
    #arrange
    decorated_func = runtimedocs.core.runtimedocs(verbosity=verbosity)(func)

    #call
    decorated_func()

    #assert
    if verbosity == 0:
        assert mock_stdout.getvalue() == ''
    else:
        assert mock_stdout.getvalue() != ''

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


@pytest.mark.parametrize('timing_info', [True, False])
@mock.patch('runtimedocs.core.logging.Formatter', autospec=True)
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_timing_info_and_format(mock_open, mock_formatter_init, timing_info, func):
    # arrange
    decorated_func = runtimedocs.core.runtimedocs(timing_info=timing_info)(func)

    # call
    decorated_func()

    # assert
    if timing_info:
        mock_formatter_init.assert_called_once_with(fmt='%(asctime)s:  #%(message)s')
    else:
        mock_formatter_init.assert_called_once_with(fmt='#%(message)s')


@mock.patch('runtimedocs.core.logging.getLogger', autospec=True)
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_add_extra_handler(mock_open, mock_getLogger, func):
    # arrange
    dummy_handlers = [
        logging.FileHandler('dummy-handler-1.log'),
        logging.FileHandler('dummy-handler-2.log')
    ]
    # we pass verbosity=True to enforce that addHandler is also called for the streamHandler
    # so in total the addHanlder will be called 4 times:1 for the streamhandler / 1 for the default file handler
    # and 2 times for each of the extra dummy filehandlers
    decorated_func = runtimedocs.core.runtimedocs(verbosity=True, extra_logger_handlers=dummy_handlers)(func)

    # call
    decorated_func()

    # assert
    assert mock_getLogger.call_count == 1
    assert mock_getLogger().addHandler.call_count == 2 + len(dummy_handlers)

@pytest.mark.parametrize('func_return_value', ['bla', ('bla', 'foo')])
@mock.patch('runtimedocs.core.logging.getLogger', autospec=True)
@mock.patch('{builtin}.open'.format(builtin=builtin_str))
def test_multi_return_output(mock_open, mock_getLogger, func_return_value, func):
    # arrange
    func.return_value = func_return_value
    decorated_func = runtimedocs.core.runtimedocs()(func)

    # call
    decorated_func()

    # assert
    assert mock_getLogger.call_count == 1
    if isinstance(func_return_value, tuple):
        mock_getLogger().\
           info.assert_has_calls([mock.call('returned value is a tuple and could be a multi output return statement:')])
    else:
        mock_getLogger(). \
            info.assert_has_calls(
            [mock.call('single output return statement:')])


