#!/usr/bin/env python
# coding=utf-8

"""
Module to format multiline Exception into regular string
"""

import os
import logging

from .constants import Types


class OneLineExceptionFormatter(logging.Formatter):
    """
    Exception Formatter class
    To format multiline Exception into regular string
    """

    def formatException(self, exc_info: Types.EXC_INFO) -> str:
        """
        Method to format Exception into string
        :param exc_info: Types.EXC_INFO - exception info
        :return: str - formatted string
        """
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record: logging.LogRecord) -> str:
        """
        Method to format record
        :param: logging.LogRecord - record:
        :return: str
        """
        # noinspection StrFormat
        result = super().format(record)
        if record.exc_text:
            result = result.replace('\n', '')
        return result

    @classmethod
    def logger_initialisation(cls, debug: bool = False) -> None:
        """
        Method for logger initialisation
        :param debug: bool - debug mod turn on or turn off
        """
        debug_level: bool = debug and 'DEBUG' or 'INFO'
        handler: logging.StreamHandler = logging.StreamHandler()
        formatter: OneLineExceptionFormatter = cls(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        root: logging.Logger = logging.getLogger('chardet.charsetprober')
        root.setLevel(os.environ.get('LOGLEVEL', debug_level))
        root.addHandler(handler)
