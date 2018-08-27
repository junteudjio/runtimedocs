import inspect
from collections import ChainMap, OrderedDict

# try to import the runtimedocs_types_parsers plugin package to have more parsers for commonly used libraries like:
# numpy, pandas, scipy, etc ...
try:
    from runtimedocs_types_parsers import extra_types_parsers_dict
except ImportError:
    extra_types_parsers_dict = dict()


def get_type(arg):
    return str(type(arg))

def default_type_parser(arg, max_stringify=1000):
    parsed = OrderedDict(type=get_type(arg))
    if hasattr(arg, '__len__'):
        parsed['len'] = len(arg)
    if hasattr(arg, 'keys'):
        parsed['keys'] = str(arg.keys())
    parsed['value'] = repr(arg)[:max_stringify]
    return parsed


def function_parser(arg):
    parsed = OrderedDict(type=get_type(arg))
    parsed['name'] = arg.__name__
    parsed['signature'] = str(inspect.signature(arg))
    parsed['fullargspec'] = str(inspect.getfullargspec(arg))
    parsed['isbuiltin'] = inspect.isbuiltin(arg)
    #parsed['doc'] = inspect.getdoc(arg)
    return parsed

def class_parser(arg):
    parsed = function_parser(arg)
    parsed['inheritance_tree'] = inspect.getmro(arg)
    return parsed


native_types_parsers_dict = {
    "<class 'type'>" : class_parser,
    "<class 'builtin_function_or_method'>": function_parser,
    "<class 'function'>": function_parser,
}
common_types_parsers_dict = ChainMap(extra_types_parsers_dict, native_types_parsers_dict)