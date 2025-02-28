from typing import TypeVar, Generic, Optional
import contextvars
import threading
import abc

__all__ = (
    'GlobalManager',
)

T = TypeVar('T')


class GlobalManager(Generic[T], metaclass=abc.ABCMeta):
    """Base class for your context managers"""
    _storage: Optional[contextvars.ContextVar] = None  # convextvars storage

    def __init__(self, value: T) -> None:
        self._value: Optional[T] = value
        if self.__class__._storage is None:
            self.__class__._storage = contextvars.ContextVar(self.__class__._get_storage_name(), default=None)

    @classmethod
    def _get_qualified_name(cls) -> str:
        return f'{cls.__module__}.{cls.__qualname__}'

    @classmethod
    def _get_storage_name(cls) -> str:
        return cls._get_qualified_name().replace('.', '__')

    def _set_current_context(self, value: Optional[T]) -> None:
        if self._storage is not None:
            self._storage.set(value)

        return None

    def _swap(self) -> None:
        current_context: Optional[T] = self.get_current_context()
        current_value: Optional[T] = self._value
        self._value = current_context
        self._set_current_context(value=current_value)

    def __enter__(self):
        self._swap()
        return self

    async def __aenter__(self):
        self._swap()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._swap()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._swap()

    @classmethod
    def get_current_context(cls) -> Optional[T]:
        if cls._storage is not None:
            return cls._storage.get()

        return None
