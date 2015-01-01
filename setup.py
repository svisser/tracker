import ast
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('tracker/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='tracker',
    version=version,
    description="Command-line utility for tracking objects",
    url='https://github.com/svisser/tracker',
    author='Simeon Visser',
    author_email='simeonvisser@gmail.com',
    license='MIT',
    install_requires=[
        'click==3.3',
    ],
    packages=['tracker'],
)
