import inspect
from collections import OrderedDict

try:
    from collections import ChainMap
    signature_func = inspect.signature
except ImportError:
    from chainmap import ChainMap
    from funcsigs import signature
    signature_func = lambda x: str(signature(x))

# try to import the runtimedocs_types_parsers plugin package to have more parsers for commonly used libraries like:
# numpy, pandas, scipy, etc ...
try:
    from runtimedocs_types_parsers import extra_types_parsers_dict
except ImportError:
    extra_types_parsers_dict = dict()


def get_type(arg):
    '''helper function the get the type of an abject as a string.'''
    return str(type(arg))

def default_type_parser(arg, max_stringify=1000):
    '''
    default type parser which basically return the repr string of the object.
    Parameters
    ----------
    arg: object to parse
    max_stringify: how long at max should be the returned string after doing repr(arg)

    Returns
    -------
    parsed: OrderedDict('value', ['keys'], ['len'])
        value: is repr(arg)[:max_stringify]
        keys: is the the keys in the parsed object and only added to parsed if the object is a dict
        len: is the the length of the parsed object and only added to parsed if the object is an iterable
    '''
    parsed = OrderedDict(type=get_type(arg))
    if hasattr(arg, '__len__'):
        parsed['len'] = len(arg)
    if hasattr(arg, 'keys'):
        parsed['keys'] = str(arg.keys())
    parsed['value'] = repr(arg)[:max_stringify]
    return parsed


def function_parser(arg):
    '''
    type parser for user defined and builtin functions.
    Parameters
    ----------
    arg: function to parse

    Returns
    -------
    parsed: OrderedDict('value', 'signature', 'fullargspec', 'isbuiltin')
    '''
    parsed = OrderedDict(type=get_type(arg))
    parsed['name'] = arg.__name__
    parsed['signature'] = str(signature_func(arg))
    try:
        parsed['fullargspec'] = str(inspect.getfullargspec(arg))
    except Exception as e:
        parsed['fullargspec'] = str(inspect.getargspec(arg))
    parsed['isbuiltin'] = inspect.isbuiltin(arg)
    #parsed['doc'] = inspect.getdoc(arg)
    return parsed

def class_parser(arg):
    '''
    type parser for user defined and builtin classes.
    Parameters
    ----------
    arg: class to parse

    Returns
    -------
    parsed: OrderedDict('value', 'signature', 'fullargspec', 'isbuiltin', 'inheritance_tree)
    '''
    parsed = function_parser(arg)
    parsed['inheritance_tree'] = inspect.getmro(arg)
    return parsed


native_types_parsers_dict = {
    "<class 'type'>" : class_parser,
    "<class 'builtin_function_or_method'>": function_parser,
    "<class 'function'>": function_parser,
}
common_types_parsers_dict = ChainMap(extra_types_parsers_dict, native_types_parsers_dict)