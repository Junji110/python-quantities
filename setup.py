"""
Class description.
Hack hack hack.

I said two lines. At least.
I made some beautfication in the documentation.

"""
from distutils.cmd import Command
from distutils.core import setup
from distutils.command.sdist import sdist as _sdist
from distutils.command.build import build as _build
import os

import sys

print('Path to the Python executable', sys.executable())

class data(Command):

    description = "Convert the NIST databas of constants"

    user_options = []

    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        with open('quantities/constants/NIST_codata.txt') as f:
            data = f.read()
        data = data.split('\n')[10:-1]

        with open('quantities/constants/_codata.py', 'w') as f:
            f.write('# THIS FILE IS AUTOMATICALLY GENERATED\n')
            f.write('# ANY CHANGES MADE HERE WILL BE LOST\n\n')
            f.write('physical_constants = {}\n\n')
            for line in data:
                name = line[:55].rstrip().replace('mag.','magnetic')
                name = name.replace('mom.', 'moment')
                val = line[55:77].replace(' ','').replace('...','')
                prec = line[77:99].replace(' ','').replace('(exact)', '0')
                unit = line[99:].rstrip().replace(' ', '*').replace('^', '**')
                d = "{'value': %s, 'precision': %s, 'units': '%s'}" \
                    %(val, prec, unit)
                f.write("physical_constants['%s'] = %s\n"%(name, d))


class sdist(_sdist):

    def run(self):
        self.run_command('data')
        _sdist.run(self)


class build(_build):

    def run(self):
        self.run_command('data')
        _build.run(self)


class test(Command):

    """Run the test suite."""

    description = "Run the test suite"

    user_options = [('verbosity=', 'V', 'set test report verbosity')]

    def initialize_options(self):
        self.verbosity = 0

    def finalize_options(self):
        try:
            self.verbosity = int(self.verbosity)
        except ValueError:
            raise ValueError('verbosity must be an integer.')

    def run(self):
        import sys
        if sys.version.startswith('2.6') or sys.version.startswith('3.1'):
            import unittest2 as unittest
        else:
            import unittest
        suite = unittest.TestLoader().discover('.')
        unittest.TextTestRunner(verbosity=self.verbosity+1).run(suite)


packages = []
for dirpath, dirnames, filenames in os.walk('quantities'):
    if '__init__.py' in filenames:
        packages.append('.'.join(dirpath.split(os.sep)))
    else:
        del(dirnames[:])

with open('quantities/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line)

setup(
    author = 'Darren Dale',
    author_email = 'dsdale24@gmail.com',
#    classifiers = """Development Status :: 4 - Beta
#        Environment :: Console
#        Intended Audience :: Developers
#        Intended Audience :: Education
#        Intended Audience :: End Users/Desktop
#        Intended Audience :: Science/Research
#        License :: OSI Approved :: BSD License
#        Operating System :: OS Independent
#        Programming Language :: Python
#        Topic :: Education
#        Topic :: Scientific/Engineering
#        """,
    cmdclass = {
        'build': build,
        'data': data,
        'sdist': sdist,
        'test': test,
        },
    description = "Support for physical quantities with units, based on numpy",
    download_url = "http://pypi.python.org/pypi/quantities",
    keywords = ['quantities', 'units', 'physical', 'constants'],
    license = 'BSD',
    long_description = """Quantities is designed to handle arithmetic and
    conversions of physical quantities, which have a magnitude, dimensionality
    specified by various units, and possibly an uncertainty. See the tutorial_
    for examples. Quantities builds on the popular numpy library and is
    designed to work with numpy ufuncs, many of which are already
    supported. Quantities is actively developed, and while the current features
    and API are stable, test coverage is incomplete so the package is not
    suggested for mission-critical applications.

    .. _tutorial: http://packages.python.org/quantities/user/tutorial.html
    """,
    name = 'quantities',
    packages = packages,
    platforms = 'Any',
    requires = [
        'python (>=2.6.0)',
        'numpy (>=1.4.0)',
        ],
    url = 'http://packages.python.org/quantities',
    version = __version__,
)
