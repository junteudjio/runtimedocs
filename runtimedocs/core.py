import os
import sys
import time
import inspect
from functools import wraps, partial
import logging
import platform

try:
    from collections import ChainMap

    signature_func = inspect.signature
except ImportError:
    from chainmap import ChainMap
    from funcsigs import signature

    signature_func = lambda x: str(signature(x))

from runtimedocs import helpers
from runtimedocs.helpers import get_type

HOSTNAME = platform.node()


def runtimedocs(force_enable_runtimedocs=False, verbosity=0, timing_info=True,
                default_type_parser=helpers.default_type_parser, max_stringify=1000,
                prefix_module_name_to_logger_name=True, custom_logger_name=None, extra_logger_handlers=None,
                common_types_parsers_dict=helpers.common_types_parsers_dict, custom_types_parsers_dict=None
                ):
    '''
    runtimedocs decorator helps you understand how your code behaves at runtime.
         It provides detailed information about:
         - what was the expected signature of a function/class.
         - what was the actual signature used when calling that function/class at run time.
         - where was the function/class declared in and called from.
         - what's the hostname of the machine running the code.
         - what are the types, names, values of the input parameters and returned values of that function.
         - when relevant also add specific information like their : len, signature, inheritance_tree, etc ...
         - what were the positional/key-word arguments at call time.
         - has the function exited successfully or ran into an exception.
         - how long it took to run in case of success.
         - display what was the exception otherwise and raises it back to not side-effect your program.

      All these information are saved in a file usually named as follows: module_name.function_name.rundimedocs.log
      Additionally they can be printed on the terminal if the verbosity level is set to 1.
      You can easily toggle the runtimedocs decorator off by setting the env variable DISABLE_RUNTIMEDOCS to True.

    Parameters
    ----------
    force_enable_runtimedocs: bool | DEFAULT = False
        In case the environment variable DISABLE_RUNTIMEDOCS is set to True, setting this flag to True 
        allows you to activate the decorator for a specific function/class.
    verbosity: int | DEFAULT = 0
        When set to 0, it means the runtimedocs information won't be printed on the terminal
        This allows you to still see your usual printed messages easily.
        When set to a value > 0, it means rundimedocs will also print on the terminal what its been saved in the 
        runtimedocs log file of the decorated function.
    timing_info: bool | DEFAULT = True
        True, means you want to keep track and log the time at which the decorated function was called
    default_type_parser: function | DEFAULT = runtimedocs.helpers.default_type_parser
        default way to parse the input parameters and returned values.
        This will take as input for instance one the arguments been passed in to the decorated function and return
        an OrderDict with keys: type, value. But also len and keys when relevant.
    max_stringify: int | DEFAULT = 1000
        this value is used by the default_type_parser function to chunk the length of the string returned 
        by repr of the arg been parsed. ie:  value_of_arg_been_parsed = repr(arg_been_parsed)[:max_stringify]
    prefix_module_name_to_logger_name: bool | DEFAULT = True
        True, means that runtimedocs decorator will save the information for a specific function/class been decorated
        in a file called: current_module_name.decorated_function_name.rundimedocs.log
        if False that file is called: decorated_function_name.rundimedocs.log
    custom_logger_name: str | DEFAULT = None
        if a string is specified, this will be the name of the logger and runtimedocs will save information in a file
        called:  custom_logger_name.runtimedocs.log no matter what's the value of prefix_module_name_to_logger_name
    extra_logger_handlers: list | DEFAULT = None
        runtimedocs decorator uses the builting logging module to create log information.
        So this argument allows you to specify additional [file]handlers to where to save the runtime information
        being extracted. This could be useful for example to centralized all the logged info in a single file or
        group of files since by default every function in every module has its own log file.
        Note that, this allows you to add additional handlers, not overrides the default one.
        Also each handler of the list could be a string or a custom instance of logging.FileHandler()
    common_types_parsers_dict: dict | DEFAULT = helpers.common_types_parsers_dict
        this parameter allows you to bypass the default_type_parser for certain specific builtin python types
        it is a dictionary with keys representing the type as str and the parsing functions as values.
        If the runtimedocs_types_parsers plugin is installed then additional parsers for third-parties types
        are available and will bypass the default_type_parser.
        For instance if the plugin is installed, new parsers are avalaible for numpy, scipy, pandas
        enabling runtimedocs to print even more relevant information like: shape, dim, mean, std, etc ...
    custom_types_parsers_dict: dict | DEFAULT = None
        similarly to common_types_parsers_dict but for your own custom types.
        For instance if your program makes uses of a objects from a class you want to parse in a given way then do:
        custom_types_parsers_dict = {"<class 'MyClassName'>" : my_class_parser_func } where  my_class_parser_func
        returns an OrderDict with keys like: type, value, my_size, etc...
        Another use of it, is if you want to parse nested lists, the default_type_parser can do that but by overriding
        the parsing function for the type: "<class'list'>" you have more control on how \ you want to parse the nested
        lists.

    Returns
    -------
    wrapper: function
        the decorated function/class.
    '''

    extra_logger_handlers = extra_logger_handlers if extra_logger_handlers else []
    custom_types_parsers_dict = custom_types_parsers_dict if custom_types_parsers_dict else {}

    # when looking for a parser to parse a value first look at the custom parsers provided by the user of the package
    # if not found then search in the common types parsers provided natively by the package
    # or the runtimedocs-typesparsers plugin
    # if the type is not found there too then we use the default parser.
    types_parsers = ChainMap(custom_types_parsers_dict, common_types_parsers_dict)

    def parse_arg(arg):
        parse_func = types_parsers.get(get_type(arg), partial(default_type_parser, max_stringify=max_stringify))
        return parse_func(arg)

    def print_arg(arg, logger):
        for key, val in parse_arg(arg).items():
            logger.info('\t {key} = {val}'.format(key=key, val=val))
        logger.info('-' * 5)

    def decorate(func):
        # if the DISABLE_RUNTIMEDOCS env var is True AND the force_enable_runtimedocs flag is False then return the
        # original non-decorated function.
        if bool(os.environ.get('DISABLE_RUNTIMEDOCS', False)) and not force_enable_runtimedocs:
            return func

        if not custom_logger_name or not isinstance(custom_logger_name, str):
            if prefix_module_name_to_logger_name:
                logger_name = '{module_name}.{func_name}'.format(module_name=__name__, func_name=func.__name__)
            else:
                logger_name = '{func_name}'.format(func_name=func.__name__)
        else:
            logger_name = custom_logger_name

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        if timing_info:
            formatter = logging.Formatter('%(asctime)s:  #%(message)s')
        else:
            formatter = logging.Formatter('#%(message)s')

        if verbosity > 0:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        file_handler = logging.FileHandler('{}.runtimedocs.log'.format(logger_name))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        for handler in extra_logger_handlers:
            if isinstance(handler, str):
                file_handler = logging.FileHandler(handler)
                file_handler.setLevel(logging.INFO)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            else:
                logger.addHandler(handler)

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info('#' * 100)
            logger.info('calling [{}] declared inside module [{}]'.format(func.__name__, func.__module__))
            logger.info('caller name: [{}]'.format(helpers.caller_name()))
            logger.info('ran inside: hostname=[{}]'.format(HOSTNAME))
            logger.info('-' * 100)

            # getting the signature information
            args_types = [get_type(el) for el in args]
            kwargs_types = [(str(k), get_type(v)) for k, v in kwargs.items()]

            all_args_str = ', '.join(args_types + ['{}={}'.format(k, v) for k, v in kwargs_types])

            logger.info('declared signature = {func_name}{signature}'.format(
                func_name=func.__name__,
                signature=signature_func(func)
            ))
            logger.info('called   signature = {func_name}({all_args_str})'.format(
                func_name=func.__name__,
                all_args_str=all_args_str
            ))
            logger.info('-' * 100)

            # get details info about the function paramters
            n_args = len(args)
            n_kwargs = len(kwargs)

            logger.info('Number of positional paramters: {}'.format(n_args))
            for i, arg in enumerate(args):
                logger.info('\t#{}:'.format(i))
                print_arg(arg, logger)

            logger.info('Number of key word paramters: {}'.format(n_kwargs))
            for i, (arg_name, arg) in enumerate(kwargs.items()):
                logger.info('\t{}:'.format(arg_name))
                print_arg(arg, logger)

            logger.info('-' * 100)

            # get details about the return values or the eventual exception raised
            try:
                tic = time.time()
                res = func(*args, **kwargs)
                tac = time.time()
            except Exception as e:
                logger.error('!!!EXCEPTION!!! [{}] ran into an exception before exiting:'.format(func.__name__))
                logger.error('\n')
                logger.error(e, exc_info=True)
                raise e
            else:
                logger.info('[{}] ran successfully in [{}]seconds and its returned value has these specs:'.format(
                    func.__name__,
                    str(round(tac - tic, 4))
                )
                )
                if isinstance(res, tuple):
                    logger.info('returned value is a tuple and could be a multi output return statement:')
                    for i, el in enumerate(res):
                        logger.info('\t#{}:'.format(i))
                        print_arg(el, logger)
                else:
                    logger.info('single output return statement:')
                    print_arg(res, logger)
                return res

        return wrapper

    return decorate

# if __name__ == '__main__':
#     @runtimedocs(verbosity=1, timing_info=False)
#     def myadd(a, b, f=sum, not_used=None):
#         return f([a, b])
#
#
#     myadd(1, 2, f=sum)
