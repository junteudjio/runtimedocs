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

with open('LICENSE') as f:
    license = f.read()

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

setup(
    name='runtimedocs',
    version=grep('__version__'),
    description='Understanding how your code behaves at runtime made simple',
    long_description=readme,
    author='Junior Teudjio',
    author_email='jun.teudjio@gmail.com',
    url='https://github.com/junteudjio/runtimedocs',
    license=license,
    packages=['runtimedocs'],
    include_package_data=True,
    install_requires=reqs,
    classifiers=[
        "Development Status :: 5 - Production/Stable"
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

