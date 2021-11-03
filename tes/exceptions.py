# -*- coding: utf-8 -*-

"""
tes.exceptions
~~~~~~~~~~~~~~

This module contains the set of exceptions.
"""


class TESException(IOError):
    """There was an ambiguous exception that occurred while handling your request."""


class AuthErrorException(TESException, ValueError):
    """Authentication failed."""
