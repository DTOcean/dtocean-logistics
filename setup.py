# -*- coding: utf-8 -*-

import os
import sys

from distutils.cmd import Command
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)
        
class CleanPyc(Command):

    description = 'clean *.pyc'
    user_options = []
    exclude_list = ['.egg', '.git', '.idea', '__pycache__']
     
    def initialize_options(self):
        pass
     
    def finalize_options(self):
        pass
     
    def run(self):
        print "start cleanup pyc files."
        for pyc_path in self.pickup_pyc():
            print "remove pyc: {0}".format(pyc_path)
            os.remove(pyc_path)
        print "the end."

    def is_exclude(self, path):
        for item in CleanPyc.exclude_list:
            if path.find(item) != -1:
                return True
        return False
     
    def is_pyc(self, path):
        return path.endswith('.pyc')
     
    def pickup_pyc(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for fname in files:
                if self.is_exclude(root):
                    continue
                if not self.is_pyc(fname):
                    continue
                yield os.path.join(root, fname)

setup(name='dtocean-logistics',
      version='1.1.dev1',
      description='Logistics module for the DTOcean tools',
      author=('Paulo Chainho, '
              'Boris Teillant, '
              'Pedro Vicente, '
              'Mathew Topper, '
              'Adam Collin'),
      author_email=('paulo@wavec.org, '
                    'boris.teillant@wavec.org, '
                    'pedro.vicente@wavec.org, '
                    'damm_horse@yahoo.co.uk, '
                    'acollin@staffmail.ed.ac.uk'),
      license="GPLv3",
      packages=find_packages(),
      install_requires=[
          'geopy',
          'networkx',
          'matplotlib',
          'numpy',
          'pandas',
          'polite>=0.9',
          'scipy',
          'utm',
          'xlrd'
      ],
      package_data={'dtocean_logistics': ['config/*.ini']},
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass = {'test': PyTest,
                  'cleanpyc': CleanPyc
                  },
      )
