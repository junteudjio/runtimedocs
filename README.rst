
runtimedocs decorator helps you understand how your code behaves at runtime.

It provides detailed information about:
 - what was the expected signature of a function/class.
 - where was the function/class declared in and called from.
 - what was the actual signature used when calling that function/class at run time.
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
force_enable_runtimedocs: boolean
    DEFAULT = False
    In case the environment variable DISABLE_RUNTIMEDOCS is set to True, setting this flag to True
    allows you to activate the decorator for a specific function/class.
verbosity: int
    DEFAULT = 0
    When set to 0, it means the runtimedocs information won't be printed on the terminal
    This allows you to still see your usual printed messages easily.
    When set to a value > 0, it means rundimedocs will also print on the terminal what its been saved in the
    runtimedocs log file of the decorated function.
timing_info: bool
    DEFAULT = True
    True, means you want to keep track and log the time at which the decorated function was called
default_type_parser: function
    DEFAULT = runtimedocs.helpers.default_type_parser
    default way to parse the input parameters and returned values.
    This will take as input for instance one the arguments been passed in to the decorated function and return
    an OrderDict with keys: type, value. But also len and keys when relevant.
max_stringify: int
    DEFAULT = 1000
    this value is used by the default_type_parser function to chunk the length of the string returned
    by repr of the arg been parsed. ie:  value_of_arg_been_parsed = repr(arg_been_parsed)[:max_stringify]
prefix_module_name_to_logger_name: bool
    DEFAULT = True
    True, means that runtimedocs decorator will save the information for a specific function/class been decorated
    in a file called: current_module_name.decorated_function_name.rundimedocs.log
    if False that file is called: decorated_function_name.rundimedocs.log
custom_logger_name: str
    DEFAULT = None
    if a string is specified, this will be the name of the logger and runtimedocs will save information in a file
    called:  custom_logger_name.runtimedocs.log no matter what's the value of prefix_module_name_to_logger_name
extra_logger_handlers: list
    DEFAULT = None
    runtimedocs decorator uses the builting logging module to create log information.
    So this argument allows you to specify additional [file]handlers to where to save the runtime information
    being extracted. This could be useful for example to centralized all the logged info in a single file or
    group of files since by default every function in every module has its own log file.
    Note that, this allows you to add additional handlers, not overrides the default one.
common_types_parsers_dict: dict
    DEFAULT = helpers.common_types_parsers_dict
    this parameter allows you to bypass the default_type_parser for certain specific builtin python types
    it is a dictionary with keys representing the type as str and the parsing functions as values.
    If the runtimedocs_types_parsers plugin is installed then additional parsers for third-parties types
    are available and will bypass the default_type_parser.
    For instance if the plugin is installed, new parsers are avalaible for numpy, scipy, pandas
    enabling runtimedocs to print even more relevant information like: shape, dim, mean, std, etc ...
custom_types_parsers_dict: dict
    DEFAULT = None
    similarly to common_types_parsers_dict but for your own custom types.
    For instance if your program makes uses of a objects from a class you want to parse in a given way then do:
    custom_types_parsers_dict = {"<class 'MyClassName'>" : my_class_parser_func } where  my_class_parser_func
    returns an OrderDict with keys like: type, value, my_size, etc...
    Another use of it, is if you want to parse nested lists, the default_type_parser can do that but by overriding
    the parsing function for the type: "<class'list'>" you have more control on how \ you want to parse the nested
    lists.

Returns
-------
the decorated object.


