#!/usr/bin/env python

import os
from setuptools import find_packages, setup
import flyenv


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(name='flyenv',
      version=flyenv.__version__,
      description='a tool helps manage environment variable portably and safely',
      long_description=README,
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Topic :: Internet :: WWW/HTTP',
      ],
      keywords='flyenv help environment variable management',
      author='luojiebin',
      author_email='luo.jiebin@foxmail.com',
      url='https://github.com/luojiebin/flyenv',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'flyenv = flyenv.flyenv:command_line_runner',
          ]
      },
      include_package_data=True,
      install_requires=[
          'pycrypto',
      ],
      )
