import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='ci_screen',
    version='0.0.1',
    author='Gary Johnson',
    author_email = 'gary@gjtt.com',
    description = 'Display jenkins info',
    license = 'MIT License',
    packages = ['ci_screen'],
    )
