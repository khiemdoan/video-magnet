

__author__ = 'KhiemDH'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

import inspect
import logging
from functools import wraps
from logging import Logger
from typing import Callable, ParamSpec, TypeVar

Param = ParamSpec('Param')
RetType = TypeVar('RetType')
OriginalFunc = Callable[Param, RetType]
DecoratedFunc = Callable[Param, RetType]
logger = logging.Logger(__file__)


def ignore_exception(func) -> Callable[[OriginalFunc], DecoratedFunc]:
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as ex:
                if isinstance(logger, Logger):
                    logger.exception(ex)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                if isinstance(logger, Logger):
                    logger.exception(ex)
    return wrapper


def ignore_exception_with_logger(logger: Logger):
    def inner(func) -> Callable[[OriginalFunc], DecoratedFunc]:
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as ex:
                    if isinstance(logger, Logger):
                        logger.exception(ex)
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    if isinstance(logger, Logger):
                        logger.exception(ex)
        return wrapper
    return inner
