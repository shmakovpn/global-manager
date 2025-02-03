import abc
import time
import threading
from unittest.mock import patch
import global_manager.global_manager_itself as tm
from reverse_patch import ReversePatch


class OneContextManager(tm.GlobalManager[int]):
    @classmethod
    def get_one_value(cls) -> int:
        """This is a good practice to rename `get_current_context` method to something with business meaning"""
        return super().get_current_context()


class SomeThread(threading.Thread):
    def run(self) -> None:
        manager = OneContextManager[int](value=0)
        # noinspection PyProtectedMember
        assert manager._set_current_context(value=35) is None
        # noinspection PyProtectedMember
        assert manager._thread_storage.foo == 35
        assert OneContextManager.get_current_context() == 35


class SomeContextThread(threading.Thread):
    def run(self) -> None:
        with OneContextManager[int](2):
            assert OneContextManager.get_current_context() == 2
            time.sleep(0.1)


class TestGlobalManager:
    def test_inheritance(self):
        assert len(tm.GlobalManager.mro()) == 3
        assert type(tm.GlobalManager) == abc.ABCMeta

    def test__get_qualified_name(self):
        assert OneContextManager._get_qualified_name() \
               == OneContextManager.__module__ + '.' + OneContextManager.__qualname__

    def test__get_thread_storage_name(self):
        with ReversePatch(func=OneContextManager._get_thread_storage_name) as rp:
            rp.args.cls._get_qualified_name.return_value = 'foo.bar'
            assert rp.c(*rp.args) == 'foo__bar'

    def test__init(self):
        manager = OneContextManager(11)
        assert manager._value == 11

    def test_set_and_get_current_context(self):
        with patch.object(OneContextManager, '_get_thread_storage_name', return_value='foo') as m:
            m.return_value = 'foo'
            manager = OneContextManager(value=0)
            assert manager._set_current_context(value=34) is None
            assert manager._thread_storage.foo == 34
            assert OneContextManager.get_current_context() == 34

            t = SomeThread()
            t.start()
            t.join()

            assert manager._thread_storage.foo == 34
            assert OneContextManager.get_current_context() == 34

    def test__swap(self):
        assert OneContextManager.get_current_context() is None

        with OneContextManager(value=3):
            assert OneContextManager.get_current_context() == 3

            with OneContextManager(value=4):
                assert OneContextManager.get_current_context() == 4

            assert OneContextManager.get_current_context() == 3

            t = SomeContextThread()
            t.start()
            time.sleep(0.01)  # wait for __enter__ in the thread
            assert OneContextManager.get_current_context() == 3

        time.sleep(0.13)  # wait for __exit__ in the thread
        assert OneContextManager.get_current_context() is None



