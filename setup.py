from setuptools import setup


setup(
    name='tracker',
    version='0.0.1',
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
