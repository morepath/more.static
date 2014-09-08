import os
from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.txt').read())

setup(name='more.static',
      version='0.3',
      description="BowerStatic integration for Morepath",
      long_description=long_description,
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      keywords='morepath bowerstatic bower',
      license="BSD",
      url="http://pypi.python.org/pypi/more.static",
      namespace_packages=['more'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'morepath >= 0.4',
        'bowerstatic >= 0.4',
        ],
      extras_require = dict(
        test=['pytest >= 2.0',
              'pytest-cov',
              'WebTest >= 2.0.14'],
        ),
      )
