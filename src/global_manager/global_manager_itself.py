from typing import TypeVar, Generic, Optional
import threading
import abc

__all__ = (
    'GlobalManager',
)

T = TypeVar('T')


class GlobalManager(Generic[T], metaclass=abc.ABCMeta):
    """Base class for your context managers"""

    _thread_storage = threading.local()

    @classmethod
    def _get_qualified_name(cls) -> str:
        return f'{cls.__module__}.{cls.__qualname__}'

    @classmethod
    def _get_thread_storage_name(cls) -> str:
        return cls._get_qualified_name().replace('.', '__')

    def __init__(self, value: T) -> None:
        self._value: T = value

    def _set_current_context(self, value: Optional[T]) -> None:
        setattr(self._thread_storage, self._get_thread_storage_name(), value)

    def _swap(self) -> None:
        current_context: Optional[T] = self.get_current_context()
        current_value: T = self._value
        self._value: Optional[T] = current_context
        self._set_current_context(value=current_value)

    def __enter__(self):
        self._swap()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._swap()

    @classmethod
    def get_current_context(cls) -> Optional[T]:
        result = getattr(cls._thread_storage, cls._get_thread_storage_name(), None)
        return result
