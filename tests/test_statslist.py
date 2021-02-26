import os
from unittest.mock import patch

import pandas as pd
import pytest

from pandas_estat import read_statslist
from pandas_estat import set_appid
from pandas_estat.exceptions import EStatError
from pandas_estat.statslist import StatsListReader

with open(os.path.dirname(__file__) + "/codes_statslist.txt") as f:
    codes = f.read().splitlines()
    codes = [code for code in codes if not code.startswith("# ")]


class TestStatsList:
    """
    Test stats list.

    Assuming os.environ["ESTAT_APPID"] is set to valid app id.
    """

    @pytest.fixture(scope="function", autouse=True)
    def reset_global_appid(self):
        set_appid(None)

    def assert_statslist(self, dataframe):
        assert isinstance(dataframe, pd.DataFrame)

        # 参照:
        # 政府統計の総合窓口（e-Stat）API 仕様【バージョン 3.0】
        # 4.2.4. CSV 形式出力サンプル
        # https://www.e-stat.go.jp/api/sites/default/files/uploads/2019/07/API-specVer3.0.pdf
        expected_columns = pd.Index(
            [
                "TABLE_INF",
                "STAT_CODE",
                "STAT_NAME",
                "GOV_ORG_CODE",
                "GOV_ORG_NAME",
                "TABULATION_CATEGORY",
                "TABULATION_SUB_CATEGORY1",
                "TABULATION_SUB_CATEGORY2",
                "TABULATION_SUB_CATEGORY3",
                "TABULATION_SUB_CATEGORY4",
                "TABULATION_SUB_CATEGORY5",
                "TABULATION_CATEGORY_EXPLANATION",
                "TABULATION_SUB_CATEGORY_EXPLANATION1",
                "TABULATION_SUB_CATEGORY_EXPLANATION2",
                "TABULATION_SUB_CATEGORY_EXPLANATION3",
                "TABULATION_SUB_CATEGORY_EXPLANATION4",
                "TABULATION_SUB_CATEGORY_EXPLANATION5",
                "NO",
                "TITLE",
                "TABLE_EXPLANATION",
                "TABLE_CATEGORY",
                "TABLE_SUB_CATEGORY1",
                "TABLE_SUB_CATEGORY2",
                "TABLE_SUB_CATEGORY3",
                "CYCLE",
                "SURVEY_DATE",
                "OPEN_DATE",
                "SMALL_AREA",
                "COLLECT_AREA",
                "OVERALL_TOTAL_NUMBER",
                "UPDATED_DATE",
                "MAIN_CATEGORY_CODE",
                "MAIN_CATEGORY",
                "SUB_CATEGORY_CODE",
                "SUB_CATEGORY",
            ]
        )
        pd.testing.assert_index_equal(dataframe.columns, expected_columns)

    @pytest.mark.parametrize("code", codes)
    def test_read_statslist(self, code):
        dataframe = StatsListReader(code).read()
        self.assert_statslist(dataframe)

        dataframe = read_statslist(code)
        self.assert_statslist(dataframe)

    def test_limit(self):
        # 452 statistics in total
        dataframe = StatsListReader("00200603", limit=5).read()
        assert len(dataframe.index) == 5

        dataframe = read_statslist("00200603", limit=5)
        assert len(dataframe.index) == 5

    def test_updated_date(self):
        reader = StatsListReader("00200603", updated_date="20200101")
        assert reader.params["updatedDate"] == "20200101"

    def test_start_position(self):
        dataframe = read_statslist("00200603", start_position=5)
        dataframe_expected = read_statslist("00200603").iloc[4:].reset_index(drop=True)
        pd.testing.assert_frame_equal(dataframe, dataframe_expected)

    def test_lang(self):
        with pytest.raises(NotImplementedError):
            dataframe = read_statslist("00200603", lang="E")
        with pytest.raises(ValueError):
            dataframe = read_statslist("00200603", lang="j")

    def test_error_no_appid(self):
        """
        Raise ValueError if Application ID is unavailable
        """
        with patch("os.environ", {}):
            with pytest.raises(ValueError):
                reader = StatsListReader("00100001")
                # アプリケーション ID が指定されていません。

            with pytest.raises(ValueError):
                dataframe = read_statslist("00100001")
                # アプリケーション ID が指定されていません。

    def test_error_invalid_code_0(self):
        """
        Raise ValueError if code is not str
        """
        with pytest.raises(ValueError):
            reader = StatsListReader(100001)
            # 政府統計コードは 5 桁か 8 桁の数字を str 型で指定してください。

    def test_error_invalid_code_1(self):
        """
        Raise ValueError if code is invalid
        """
        # not digit
        with pytest.raises(ValueError):
            reader = StatsListReader("0010000a")
            # 政府統計コードは 5 桁か 8 桁の数字を str 型で指定してください。

        # not 5/8-digit
        with pytest.raises(ValueError):
            reader = StatsListReader("001000019")
            # 政府統計コードは 5 桁か 8 桁の数字を str 型で指定してください。

    def test_error_estat_invalid_id(self):
        set_appid("INVALID_APPID")

        with pytest.raises(EStatError):
            dataframe = read_statslist("00100001")

        # TODO Test other e-Stat errors

    def test_params(self):
        set_appid("APPID")
        reader = StatsListReader("00100000")  # , limit=42, start_position=420)

        assert reader.params == {
            "appId": "APPID",
            "statsCode": "00100000",
            "lang": "J",
            # "limit": 42,
            # "startPosition": 420,
        }
