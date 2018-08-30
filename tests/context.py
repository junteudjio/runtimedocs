# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import runtimedocs


try:
    # try block to test if in python 3
    from unittest import mock
    import builtins
    builtin_str = 'builtins'
except ImportError:
    # here in python 2
    import mock
    builtin_str = '__builtin__'

