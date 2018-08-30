# -*- coding: utf-8 -*-

import pytest

from .context import  runtimedocs

@pytest.mark.parametrize('value,expected_type', [
    (1, "<class 'int'>"),
    ('a', "<class 'str'>"),
    (lambda:None, "<class 'function'>"),
    ([], "<class 'list'>"),
    ((1,), "<class 'tuple'>"),
    ({}, "<class 'dict'>"),
])
def test_get_type(value, expected_type):
    assert runtimedocs.helpers.get_type(value) == expected_type


@pytest.mark.parametrize('value,expected_type', [
    (1, "<class 'int'>"),
    ('a', "<class 'str'>"),
    ([], "<class 'list'>"),
    ((1,), "<class 'tuple'>"),
    ({}, "<class 'dict'>"),
])
def test_default_type_parser(value, expected_type):
    parsed = runtimedocs.helpers.default_type_parser(value)
    assert 'value' in parsed
    if expected_type == "<class 'dict'>":
        assert 'keys' in parsed
    if expected_type in ["<class 'list'>", "<class 'tuple'>", "<class 'dict'>"]:
        assert 'len' in parsed


def test_function_parser():
    parsed = runtimedocs.helpers.function_parser(lambda:None)
    assert 'name' in parsed
    assert 'signature' in parsed
    assert 'fullargspec' in parsed
    assert 'isbuiltin' in parsed

def test_class_parser():
    class MyClass(object):
        pass
    parsed = runtimedocs.helpers.class_parser(MyClass)
    assert 'name' in parsed
    assert 'signature' in parsed
    assert 'fullargspec' in parsed
    assert 'isbuiltin' in parsed
    assert 'inheritance_tree' in parsed