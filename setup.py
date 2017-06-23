"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from lxsartools import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'lx-sar-tools',
    version = __version__,
    description = 'lx-sar-tools (Lisbon SAR Tools) is a set of tools for SAR/InSAR processing.',
    long_description = long_description,
    url = 'https://github.com/vasconde/lx-sar-tools',
    author = 'Vasco Conde',
    author_email = 'vrconde@fc.ul.pt',
    license = 'GPL-v3',
    classifiers = [
        'Intended Audience :: Researchers',
        'Topic :: Utilities',
        'License :: GPL-v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'SAR',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt','numpy', 'scipy', 'matplotlib'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'lx-sar-tools=lxsartools.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
