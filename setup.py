# -*- coding: utf-8 -*-
import codecs
import os.path
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as f:
    readme = f.read()


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


file_text = read(fpath('runtimedocs/__init__.py'))

if sys.version_info < (3,):
    reqs = [
        'mock==2.0.0',
        'chainmap==1.0.2',
        'funcsigs'
    ]
else:
    reqs = []


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
] + [
    ("Programming Language :: Python :: %s" % x)
    for x in "3 3.4 3.5 3.6 3.7".split()
]

setup(
    name='runtimedocs',
    version=grep('__version__'),
    description='Understanding how your code behaves at runtime made simple',
    long_description=readme,
    author='Junior Teudjio',
    author_email='jun.teudjio@gmail.com',
    url='https://github.com/junteudjio/runtimedocs',
    license='MIT',
    packages=['runtimedocs'],
    include_package_data=True,
    install_requires=reqs,
    classifiers=classifiers
)

