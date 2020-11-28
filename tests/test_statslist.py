import pytest

from pandas_estat import read_statslist


class TestStatsList:
    @pytest.mark.parametrize("code", ["00100001"])
    def test_read_statslist(self, code):
        dataframe = read_statslist(code)
