=========================================================
runtimedocs:  understand how your code behaves at runtime
=========================================================

.. image:: https://travis-ci.com/junteudjio/runtimedocs.svg
   :alt: build status
   :target: https://travis-ci.org/junteudjio/runtimedocs

.. image:: https://coveralls.io/repos/github/junteudjio/runtimedocs/badge.svg
   :alt: coverage
   :target: https://coveralls.io/github/junteudjio/runtimedocs?branch=develop


.. image:: https://img.shields.io/pypi/v/runtimedocs.svg
   :target: https://pypi.org/pypi/runtimedocs
   :alt: downloads

.. image:: https://img.shields.io/pypi/pyversions/runtimedocs.svg
   :target: https://pypi.org/pypi/runtimedocs
   :alt: downloads

Documentation: `runtimedocs.readthedocs.org <http://runtimedocs.readthedocs.org/en/latest/>`_
---------------------------------------------------------------------------------------------

-----
What?
-----
runtimedocs is a Python library that offers a sensible, customizable, human-friendly way to get a sense of what really happens during a function call. It implements a decorator which wraps your function/class and prints its runtime behavior and also saves it to a log file usually named as follows: module_name.function_name.rundimedocs.log.

----
Why?
----
If you ever found yourself in one or more of these situations then runtimedocs could really help:

- you would like to know which function called your function(the one you decorated using runtimedocs).
- you would like to know what were the positional and key-word arguments received by your function at runtime.
- you want to write docstrings for a (legacy)function with unclear parameters naming and would like to know more about them to help you get started. For instance if that function expect a parameter named "x", you are much more advanced if you know that during runtime "x" is usually of type=list, of value=['bar', 'foo'], of len=2.
- likewise, you may want to debug a function but ignore what are its expected input parameters and returned values (ie: their types and values). A good idea could be to decorate that function in your running environment and runtimedocs will log both the successfull and failling calls along with their inputs(types, and values) so you can know which  paramters actually break your functiom.
- you would like to know if a function is multi output(eg: return foo, bla) or single output(eg: return foo). along with the types and values of the returned variables.
- your function runs well on a given host but breaks on another, runtimedocs tells you the hostname of the computer running your function.

--------
Features
--------

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

----------
Quickstart
----------

.. code-block:: bash

    $ pip install runtimedocs

.. code-block:: python

    >>> from runtimedocs import runtimedocs

    >>> #decorate the function/class of your choice
    >>> @runtimedocs(verbosity=1, timing_info=False) #verbosity=1 means also print the logs on terminal. timing_info=False means don't log time.
    ... def myadd(a, b, f=sum):
    ...     return f([a, b])
    ...
    >>> @runtimedocs(verbosity=1, timing_info=False)
    ... def mysum(elements):
    ...     return sum(elements)
    ...
    >>> #call the decorated function and see the runtime documentation printed on the terminal and saved to a file called: __main__.myadd.runtimedocs.log
    >>> myadd(1, 2)
    ####################################################################################################
    #calling [myadd] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = myadd(a, b, f=<built-in function sum>, not_used=None)
    #called   signature = myadd(<class 'int'>, <class 'int'>, f=<class 'builtin_function_or_method'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 2
    #    #0:
    #     type = <class 'int'>
    #     value = 1
    #-----
    #    #1:
    #     type = <class 'int'>
    #     value = 2
    #-----
    #Number of key word paramters: 1
    #    f:
    #     type = <class 'builtin_function_or_method'>
    #     name = sum
    #     signature = (iterable, start=0, /)
    #     fullargspec = FullArgSpec(args=['iterable', 'start'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={})
    #     isbuiltin = True
    #-----
    #----------------------------------------------------------------------------------------------------
    #[myadd] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----

    >>> mysum([1, 2]) #logs printed and saved to a file called: __main__.mysum.runtimedocs.log
    #####################################################################################################
    #calling [mysum] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = mysum(elements)
    #called   signature = mysum(<class 'list'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 1
    #    #0:
    #     type = <class 'list'>
    #     len = 2
    #     value = [1, 2]
    #-----
    #Number of key word paramters: 0
    #----------------------------------------------------------------------------------------------------
    #[mysum] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----

    >>> mysum(el for el in [1,2])
    ######################################################################################################
    #calling [mysum] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = mysum(elements)
    #called   signature = mysum(<class 'generator'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 1
    #    #0:
    #     type = <class 'generator'>
    #     value = <generator object <genexpr> at 0x107b664f8>
    #-----
    #Number of key word paramters: 0
    #----------------------------------------------------------------------------------------------------
    #[mysum] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----


------------
User's Guide
------------


Disabling runtimedocs
=====================

Disable runtimedocs globally:

.. code-block:: python

    >>> import os
    >>> #set the DISABLE_RUNTIMEDOCS to '1' which will casted to True (like any other non-empty string).
    >>> os.environ['DISABLE_RUNTIMEDOCS'] = '1'
    >>> #with DISABLE_RUNTIMEDOCS env variable set to True, runtimedocs decorator doesn't wrap your function, so calling these functions wont't print or save any log file.
    >>> myadd(1, 2)
    >>> mysum([1, 2])

Disable runtimedocs globally but force enable locally:

.. code-block:: python

    >>> import os
    >>> #set the DISABLE_RUNTIMEDOCS to '1' which will casted to True (like any other non-empty string).
    >>> os.environ['DISABLE_RUNTIMEDOCS'] = '1'
    >>> @runtimedocs(verbosity=1, timing_info=False, force_enable_runtimedocs=True)
    ... def mysum(elements):
    ...     return sum(elements)
    ...
    >>> myadd(1, 2) #no logs for myadd
    >>> mysum([1, 2]) #force_enable_runtimedocs is set to True for mysum so runtimedocs will log the function call.
    #####################################################################################################
    #calling [mysum] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = mysum(elements)
    #called   signature = mysum(<class 'list'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 1
    #    #0:
    #     type = <class 'list'>
    #     len = 2
    #     value = [1, 2]
    #-----
    #Number of key word paramters: 0
    #----------------------------------------------------------------------------------------------------
    #[mysum] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----

Customizations
==============

Customized how runtimedocs parse a given type:

.. code-block:: python

    >>> from collections import OrderedDict
    >>> # define the function to parse a type as you like, preferably return an orderdict to see them printed in the order you want.
    >>> def my_custom_list_parser_func(L):
    ...    return OrderedDict(
    ...        bar = 'bar',
    ...        foo = 'foo',
    ...        mylist_type = type(L),
    ...        mylist_len = len(L),
    ...        mylist_repr =repr(L))
    ...
    >>> custom_parsers_dict = {"<class 'list'>": my_custom_list_parser_func}
    >>> @runtimedocs(verbosity=1, timing_info=False, custom_types_parsers_dict=custom_parsers_dict)
    ... def mysum(elements):
    ...     return sum(elements)
    ...
    >>> mysum([1,2])
    #####################################################################################################
    #calling [mysum] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = mysum(elements)
    #called   signature = mysum(<class 'list'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 1
    #    #0:
    #     bar = bar
    #     foo = foo
    #     mylist_type = <class 'list'>
    #     mylist_len = 2
    #     mylist_repr = [1, 2]
    #-----
    #Number of key word paramters: 0
    #----------------------------------------------------------------------------------------------------
    #[mysum] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----

Aggregate all the logs for multiple functions in a same file:

.. code-block:: python

    >>> import logging
    >>> file_handler = logging.FileHandler('aggregation.runtimedocs.log')

    >>> @runtimedocs(extra_logger_handlers=[file_handler])
    >>> def myadd(a, b, f=sum, not_used=None):
    ...     return f([a, b])
    ...
    >>> #even faster, you can also directly pass the string as an extra_hanlder
    >>> @runtimedocs(extra_logger_handlers=[file_handler])
    >>> def mysum(elements):
    ...     return sum(elements)
    ...
    >>> # after running these two functions 3 log files will be created: 2 for each function as usual and a 3rd one for the agregated logs
    >>> mysum([1,2])
    >>> myadd(1, 2, f=sum)
    >>> # content of aggregation.runtimedocs.log :
    #####################################################################################################
    #calling [myadd] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = myadd(a, b, f=<built-in function sum>, not_used=None)
    #called   signature = myadd(<class 'int'>, <class 'int'>, f=<class 'builtin_function_or_method'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 2
    #    #0:
    #     type = <class 'int'>
    #     value = 1
    #-----
    #    #1:
    #     type = <class 'int'>
    #     value = 2
    #-----
    #Number of key word paramters: 1
    #    f:
    #     type = <class 'builtin_function_or_method'>
    #     name = sum
    #     signature = (iterable, start=0, /)
    #     fullargspec = FullArgSpec(args=['iterable', 'start'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={})
    #     isbuiltin = True
    #-----
    #----------------------------------------------------------------------------------------------------
    #[myadd] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----
    #####################################################################################################
    #calling [mysum] declared inside module [__main__]
    #caller name: [runtimedocs.core]
    #ran inside: hostname=[Juniors-MBP.lan]
    #----------------------------------------------------------------------------------------------------
    #declared signature = mysum(elements)
    #called   signature = mysum(<class 'list'>)
    #----------------------------------------------------------------------------------------------------
    #Number of positional paramters: 1
    #    #0:
    #     type = <class 'list'>
    #     len = 2
    #     value = [1, 2]
    #-----
    #Number of key word paramters: 0
    #----------------------------------------------------------------------------------------------------
    #[mysum] ran successfully in [0.0]seconds and its returned value has these specs:
    #single output return statement:
    #     type = <class 'int'>
    #     value = 3
    #-----

Documentation/Api
-----------------

Further documentation can be found at `runtimedocs.readthedocs.org <http://runtimedocs.readthedocs.org/en/latest/>`_


Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/junteudjio/runtimedocs/issues>`_ to submit bugs or request features.


Todos
-----

Add changes to handle Python2.


Contributing
------------

Contributions are welcome, especially with custom type parsers.  See `runtimedocs_types_parsers <https://github.com/junteudjio/runtimedocs_types_parsers>`_ for what's currently supported.


License
-------

Copyright Junior Teudjio Mbativou, 2018.

Distributed under the terms of the `MIT`_ license, runtimedocs is a free and open source software.

.. _`MIT`: https://github.com/junteudjio/runtimedocs/blob/master/LICENSE