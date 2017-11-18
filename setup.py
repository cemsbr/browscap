"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from codecs import open as codecs_open  # consistent encoding
from os import path

# Always prefer setuptools over distutils
from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with codecs_open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESC = f.read()

setup(
    name='browscapy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1a1',

    description='Fast and low-memory parser for browscap.org',
    long_description=LONG_DESC,

    # The project's main homepage.
    url='https://github.com/cemsbr/browscapy',

    # Author details
    author='Carlos Eduardo Moreira dos Santos',
    author_email='cems@cemshost.com.br',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
    ],

    # What does your project relate to?
    keywords='browscap browser user agent mobile device detection',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['browscapy'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev]
    extras_require={
        'dev': [
            'bandit',
            'coverage',
            'eradicate',
            'mypy',
            'pip-tools',
            'rstcheck',
            'safety',
            'tox',
            'yala'
        ],
    },

    test_suite='tests',
    zip_safe=True
)
