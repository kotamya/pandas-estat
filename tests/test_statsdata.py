import pytest
from unittest.mock import patch

from pandas_estat import set_appid
from pandas_estat import read_statsdata
from pandas_estat.statsdata import StatsDataReader
from pandas_estat.exceptions import EStatError


class TestStatsData:
    """
    Test stats list.

    Assuming os.environ["ESTAT_APPID"] is set to valid app id.
    """

    @pytest.fixture(scope="function", autouse=True)
    def reset_global_appid(self):
        set_appid(None)

    @pytest.mark.parametrize("code", ["0003348423"])
    def test_read_statsdata(self, code):
        dataframe = read_statsdata(code)
        # TODO assert data content is correct

    def test_error_no_appid(self):
        """
        Raise ValueError if Application ID is unavailable
        """
        with patch("os.environ", {}):
            with pytest.raises(ValueError):
                # アプリケーション ID が指定されていません。
                reader = StatsDataReader("0003348423")

            with pytest.raises(ValueError):
                # アプリケーション ID が指定されていません。
                dataframe = read_statsdata("0003348423")

    def test_error_invalid_code_0(self):
        """
        Raise ValueError if code is not str
        """
        with pytest.raises(ValueError):
            reader = StatsDataReader(3348423)
            # 政府統計コードは str 型で指定してください。

        with pytest.raises(ValueError):
            dataframe = read_statsdata(3348423)
            # 政府統計コードは str 型で指定してください。

    def test_error_estat_invalid_id(self):
        set_appid("INVALID_APPID")

        with pytest.raises(EStatError):
            dataframe = read_statsdata("0003348423")

        # TODO Test other e-Stat errors

    def test_params(self):
        set_appid("APPID")
        reader = StatsDataReader("0003348423")  # , limit=42, start_position=420)

        assert reader.params == {
            "appId": "APPID",
            "statsDataId": "0003348423",
            "lang": "J",
            # "limit": 42,
            # "startPosition": 420,
        }
