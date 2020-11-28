# -*- coding: utf-8 -*-
'''Importing the required version'''
try:
  from ._version import VERSION as __version__
except ImportError:
  __version__ = 'unknown'
