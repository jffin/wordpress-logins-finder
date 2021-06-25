"""
Config and Typing module.
Config is for carrying configuration constants.
Types is for carrying complex types.
"""
import os
import re
from types import TracebackType
from typing import Type, Union, Tuple, Optional, Any, List


def strip_scheme(url: str) -> str:
    return re.sub(r'^https?://', '', url)


def targets_to_check(target: str) -> List[str]:
    target_urls: List[str] = [
        f'{target}/blog/wp-json/wp/v2/users',
        f'{target}/blog/?rest_route=/wp/v2/users',
        f'{target}/wp-json/wp/v2/users',
        f'{target}/section/news?rest_route=/wp/v2/users',
        f'{target}/section/news?rest_route=/wp/v2/usErs',
    ]
    target_urls.extend([f'/wp-json/wp/v2/users/{i}' for i in range(1, 1000)])
    target_urls.append(f'{target}/wp-json/wp/v2/users?search=admin@{strip_scheme(target)}')
    return target_urls


class Config:
    """Config class with bunch of constants"""

    TIMEOUT: int = 5
    TIMEOUT_DEFAULT: int = 60
    LIMIT_OF_ATTEMPTS_TO_RETRY: int = os.environ.get('LIMIT_OF_ATTEMPTS_TO_RETRY', 5)
    SIMULTANEOUS_CONCURRENT_TASKS: int = 51
    REQUESTS_RETRIES_NUM_TO_REMOVE: int = 1

    ERRORS_STATUS_CODES: List[int] = [400, 403, 404, 500, ]

    DEFAULT_DEBUGGING: bool = os.environ.get('DEFAULT_DEBUGGING', False)

    USER_AGENT: str = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                      ' Chrome/85.0.4183.102 Safari/537.36'

    RESULT_FILE_NAME: str = os.environ.get('RESULT_FILE_NAME', 'results.json')


class Types:
    """Types with bunch of complex types"""
    EXC_INFO: Type = Union[Tuple[type, BaseException, Optional[TracebackType]], tuple[None, None, None]]
    ASYNCIO_GATHER: Type = Tuple[
        Union[BaseException, Any], Union[BaseException, Any],
        Union[BaseException, Any], Union[BaseException, Any], Union[BaseException, Any]
    ]
