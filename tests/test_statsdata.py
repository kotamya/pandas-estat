import pytest

from pandas_estat import read_statsdata


class TestStatsData:

    @pytest.mark.parametrize("code", ["0003348423"])
    def test_read_statsdata(self, code):
        dataframe = read_statsdata(code)
