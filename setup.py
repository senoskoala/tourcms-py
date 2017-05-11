#!/usr/bin/env python
from setuptools import setup
import package_info


setup(name='tourcms',
      version=package_info.__version__,
      description="Python wrapper class for TourCMS Rest API",
      long_description="A simple wrapper for connecting to the TourCMS Marketplace API (http://www.tourcms.com/support/api/mp/). This wrapper mirrors the TourCMS PHP library. See https://github.com/prio/tourcms for more details.",
      author=package_info.__author__,
      author_email='jonathan@jonharrington.org',
      url='https://github.com/prio/tourcms',
      download_url='https://github.com/prio/tourcms',
      license=package_info.__license__,
      platforms=['all'],
      install_requires=[
          'dicttoxml==1.7.4',
      ],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
      py_modules=['tourcms'],
      )

