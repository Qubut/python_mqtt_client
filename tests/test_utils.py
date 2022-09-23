import pytest
import src.mqtt_measuring.utils as utils


class Testutils:
    f_not_found = './NotFound'
    f_dummy = './tests/mqtt_measuring/resources/DUMMYFILE'
    p_not_found = './NotPath'
    p = './tests/mqtt_measuring/resources'

    def test_check_file_returns_false(self):
        assert utils.check_file(self.f_not_found) == False

    def test_check_file_returns_true(self):
        assert utils.check_file(self.f_dummy) == True

    def test_check_path_returns_false(self):
        assert utils.check_path(self.p_not_found) == False

    def test_check_path_returns_true(self):
        assert utils.check_path(self.p) == True

    def test_get_size_raises_exception(self):
        with pytest.raises(FileNotFoundError) as e:
            utils.get_size(self.f_not_found)

    def test_get_size(self):
        assert utils.get_size(self.f_dummy) >= 1024
