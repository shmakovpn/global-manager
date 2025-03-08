class TestInit:
    def test__version(self):
        from global_manager import __version__
        assert __version__ == '1.0.4'
