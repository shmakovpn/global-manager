import abc
import asyncio
import time
import threading
import global_manager.global_manager_itself as tm


class OneContextManager(tm.GlobalManager[int]):
    @classmethod
    def get_one_value(cls) -> int:
        """This is a good practice to rename `get_current_context` method to something with business meaning"""
        return super().get_current_context()


class TwoContextManager(tm.GlobalManager[int]):

    @classmethod
    def get_two_value(cls) -> int:
        """This is a good practice to rename `get_current_context` method to something with business meaning"""
        return super().get_current_context()


class TestGlobalManager:
    def test_inheritance(self):
        assert len(tm.GlobalManager.mro()) == 3
        assert type(tm.GlobalManager) == abc.ABCMeta

    def test__init(self):
        manager = OneContextManager(11)
        assert manager._value == 11

    def test__swap(self):
        return
        log = []

        class OneContextThread(threading.Thread):
            def run(self) -> None:
                with OneContextManager(2):
                    log.append('Thread with OneContextManager(value=2).__enter__')
                    assert OneContextManager.get_current_context() == 2

                    with TwoContextManager(22):
                        assert TwoContextManager.get_current_context() == 22
                        assert OneContextManager.get_current_context() == 2

                        with OneContextManager(222):
                            assert OneContextManager.get_current_context() == 222
                            assert TwoContextManager.get_current_context() == 22

                        assert OneContextManager.get_current_context() == 2
                        assert TwoContextManager.get_current_context() == 22

                    time.sleep(0.5)
                    log.append('Thread with OneContextManager(value=2).__exit__')

        class TwoContextThread(threading.Thread):
            def run(self) -> None:
                with TwoContextManager(1):
                    log.append('Thread with OneContextManager(value=1).__enter__')
                    assert TwoContextManager.get_current_context() == 1

                    with TwoContextManager(11):
                        assert TwoContextManager.get_current_context() == 11

                    assert TwoContextManager.get_current_context() == 1

                    time.sleep(0.51)
                    log.append('Thread with TwoContextManager(value=1).__exit__')

        async def do_test11():
            assert OneContextManager.get_current_context() is None

            async with OneContextManager(value=3):
                log.append('async with OneContextManager(value=3).__aenter__')
                assert OneContextManager.get_current_context() == 3

                t = OneContextThread()
                t.start()

                async with TwoContextManager(value=33):
                    assert TwoContextManager.get_current_context() == 33
                    assert OneContextManager.get_current_context() == 3

                    async with OneContextManager(value=333):
                        assert OneContextManager.get_current_context() == 333
                        assert TwoContextManager.get_current_context() == 33

                    assert OneContextManager.get_current_context() == 3
                    assert TwoContextManager.get_current_context() == 33

                await asyncio.sleep(0.3)
                assert OneContextManager.get_current_context() == 3
                log.append('async with OneContextManager(value=3).__aexit__')

                await asyncio.sleep(0.1)  # wait for __exit__ in the thread
                assert OneContextManager.get_current_context() == 3

        async def do_test12():
            assert OneContextManager.get_current_context() is None

            async with OneContextManager(value=4):
                log.append('async with OneContextManager(value=4).__aenter__')
                assert OneContextManager.get_current_context() == 4
                await asyncio.sleep(0.1)
                assert OneContextManager.get_current_context() == 4
                log.append('async with OneContextManager(value=4).__aexit__')

        async def do_test21():
            assert TwoContextManager.get_current_context() is None

            async with TwoContextManager(value=5):
                log.append('async with TwoContextManager(value=5).__aenter__')
                assert TwoContextManager.get_current_context() == 5

                t = TwoContextThread()
                t.start()

                await asyncio.sleep(0.3)
                assert TwoContextManager.get_current_context() == 5
                log.append('async with TwoContextManager(value=5).__aexit__')

        async def do_test22():
            assert TwoContextManager.get_current_context() is None

            async with TwoContextManager(value=6):
                log.append('async with TwoContextManager(value=6).__aenter__')
                assert TwoContextManager.get_current_context() == 6
                await asyncio.sleep(0.2)
                assert TwoContextManager.get_current_context() == 6
                log.append('async with TwoContextManager(value=6).__aexit__')

        async def do_test():
            await asyncio.gather(do_test11(), do_test12(), do_test21(), do_test22())

        asyncio.run(do_test())
        time.sleep(0.2)

        assert log  # see log if something wrong
