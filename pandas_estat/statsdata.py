import io

import pandas as pd

from pandas_estat.appid import get_appid
from pandas_estat.base import BaseReader
from pandas_estat.exceptions import EStatError


def read_statsdata(code):
    """
    統計データを取得します。

    Parameters
    ----------
    - code : str
        統計表 ID です。統計表情報 (`read_statslist`) から検索できます。

        e-Stat API の `statsDataId` に相当します。

    Returns
    -------
    dataframe : pandas.DataFrame
        統計データ
    """
    dataframe = StatsDataReader(code).read()
    return dataframe


class StatsDataReader(BaseReader):
    """
    統計データを取得します。

    Parameters
    ----------
    - code : str
        統計表 ID です。統計表情報から検索できます。
    - limit : int, default None
        データの取得行数を指定して下さい。省略時は 10 万件です。
        データ件数が指定した limit 値より少ない場合、全件を取得します。
        データ件数が指定した limit 値より多い場合（継続データが存在する）は、
        受信したデータの<NEXT_KEY>タグに継続データの開始行が設定されます。
    - start_position : int, default None
        データの取得開始位置（1 から始まる行番号）を指定して下さい。省略時は先頭から取得します。
        統計データを複数回に分けて取得する場合等、継続データを取得する開始位置を指定するために指定します。
        前回受信したデータの <NEXT_KEY> タグの値を指定します。
    - from_date : str
        更新日付を指定します。指定された期間で更新された統計表の情報）を提供します。
    - to_date : str
        更新日付を指定します。指定された期間で更新された統計表の情報）を提供します。
    - version : str, default "3.0"
        API 仕様バージョンです。
        https://www.e-stat.go.jp/api/api-info/api-spec
    - lang : {"J", "E"}, default "J"
        取得するデータの言語です。
        "J" (日本語) または "E" (英語) で指定してください。
    - appid : str, optional
        アプリケーション ID です。
        指定しない場合、`pandas_estat.set_appid(...)` で指定した値か、環境変数 `ESTAT_APPID` を用います。
        次のページから取得できます。
        https://www.e-stat.go.jp/api/

    TODO
    ----
    * Fetch all rows by concatination
    """

    getparam = "getSimpleStatsData"
    table_tag = "VALUE"

    def __init__(
        self,
        code,
        limit=None,
        start_position=None,
        from_date=None,
        to_date=None,
        version="3.0",
        lang="J",
        appid=None,
    ):
        self.code = code
        self.limit = limit
        self.start_position = start_position
        self.from_date = from_date
        self.to_date = to_date
        self.version = version
        self.lang = lang
        self.appid = get_appid(appid)

        if self.appid is None:
            raise ValueError("アプリケーション ID が指定されていません。")
        if not isinstance(code, str):
            raise ValueError("統計表 ID は str 型で指定してください。")

        if limit is not None:
            raise NotImplementedError  # TODO
        if start_position is not None:
            raise NotImplementedError  # TODO
        if from_date is not None:
            raise NotImplementedError  # TODO
        if to_date is not None:
            raise NotImplementedError  # TODO
        if lang != "J":
            raise NotImplementedError  # TODO

    @property
    def params(self) -> dict:
        params = {"appId": self.appid, "statsDataId": self.code}

        if self.limit is not None:
            params["limit"] = self.limit
        if self.start_position is not None:
            params["startPosition"] = self.start_position
        # TODO from_date, to_date
        if self.lang is not None:
            params["lang"] = self.lang

        return params

    def read(self) -> pd.DataFrame:
        """
        統計データを取得します。

        Returns
        -------
        dataframe : pandas.DataFrame
            統計データ
        """
        response = self.get()
        response_parsed = self._parse_response_text(response.text)

        if "TABLE" not in response_parsed:
            msg = (
                f'{response_parsed["ERROR_MSG"]}'
                f'(STATUS: {response_parsed["STATUS"]})'
            )
            raise EStatError(msg)

        # TODO better dtypes
        # TODO give kwargs
        dataframe = pd.read_csv(io.StringIO(response_parsed["TABLE"]), dtype=str)

        return dataframe
