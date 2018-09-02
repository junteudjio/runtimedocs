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


def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height

       copied from here:
       https://stackoverflow.com/questions/2654113/python-how-to-get-the-callers-method-name-in-the-called-method
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method

    ## Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return ".".join(name)


native_types_parsers_dict = {
    "<class 'type'>" : class_parser,
    "<class 'builtin_function_or_method'>": function_parser,
    "<class 'function'>": function_parser,
}
common_types_parsers_dict = ChainMap(extra_types_parsers_dict, native_types_parsers_dict)