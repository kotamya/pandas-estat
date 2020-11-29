import io
import re

import pandas as pd

from pandas_estat.appid import get_appid
from pandas_estat.base import BaseReader
from pandas_estat.exceptions import EStatError



def read_statslist(code, limit=None, updated_date=None, start_position=None, **kwargs):
    """
    統計表情報を取得します。

    Parameters
    ----------
    - code : str
        政府統計コードです。次のページから検索できます。
        https://www.e-stat.go.jp/api/api-info/api-data
        数値 5 桁: 作成機関で検索
        数値 8 桁: 政府統計コードで検索
        e-Stat API の `statsCode` に対応します。
    - limit : int, default None
        データの取得行数を指定して下さい。省略時は 10 万件です。
        データ件数が指定した limit 値より少ない場合、全件を取得します。
        データ件数が指定した limit 値より多い場合（継続データが存在する）は、
        受信したデータの<NEXT_KEY>タグに継続データの開始行が設定されます。
        e-Stat API の `limit` に対応します。
    - start_position : int, default None
        データの取得行数を指定して下さい。省略時は 10 万件です。
        データ件数が指定した limit 値より少ない場合、全件を取得します。
        データ件数が指定した limit 値より多い場合（継続データが存在する）は、
        受信したデータの<NEXT_KEY>タグに継続データの開始行が設定されます。
        e-Stat API の `startPosition` に対応します。
    - updated_date : str, default None
        更新日付を指定します。指定された期間で更新された統計表の情報を提供します。
        以下のいずれかの形式で指定して下さい。
        * `YYYY`: 単年検索
        * `YYYYMM`: 単月検索
        * `YYYYMMDD`: 単日検索
        * `YYYYMMDD-YYYYMMDD`: 範囲検索
        e-Stat API の `updatedDate` に相当します。
    - **kwargs
        e-Stat API から取得した CSV データをパースする `pandas.read_csv` に与えるパラメータです。

    Returns
    -------
    dataframe : pandas.DataFrame
        統計表情報
    """
    dataframe = StatsListReader(code, limit=limit, updated_date=updated_date, start_position=start_position).read(**kwargs)
    return dataframe


class StatsListReader(BaseReader):
    """
    統計表情報を取得します。

    Parameters
    ----------
    - code : str
        政府統計コードです。
        数値 5 桁: 作成機関で検索
        数値 8 桁: 政府統計コードで検索
        次のページから検索できます。
        https://www.e-stat.go.jp/api/api-info/api-data
        e-Stat API の `statsCode` に対応します。
    - limit : int, default None
        データの取得行数を指定して下さい。省略時は 10 万件です。
        データ件数が指定した limit 値より少ない場合、全件を取得します。
        データ件数が指定した limit 値より多い場合（継続データが存在する）は、
        受信したデータの<NEXT_KEY>タグに継続データの開始行が設定されます。
        e-Stat API の `limit` に対応します。
    - start_position : int, default None
        データの取得開始位置（1 から始まる行番号）を指定して下さい。省略時は先頭から取得します。
        統計データを複数回に分けて取得する場合等、継続データを取得する開始位置を指定するために指定します。
        前回受信したデータの <NEXT_KEY> タグの値を指定します。
        e-Stat API の `startPosition` に対応します。
    - updated_date : str, default None
        更新日付を指定します。指定された期間で更新された統計表の情報を提供します。
        以下のいずれかの形式で指定して下さい。
        * `YYYY`: 単年検索
        * `YYYYMM`: 単月検索
        * `YYYYMMDD`: 単日検索
        * `YYYYMMDD-YYYYMMDD`: 範囲検索
        e-Stat API の `updatedDate` に相当します。
    - version : str, default "3.0"
        API 仕様バージョンです。
        https://www.e-stat.go.jp/api/api-info/api-spec
    - lang : {"J", "E"}, default "J"
        取得するデータの言語です。
        "J" (日本語) または "E" (英語) で指定してください。
        `lang`
    - appid : str, optional
        アプリケーション ID です。
        指定しない場合、`pandas_estat.set_appid(...)` で指定した値か、環境変数 `ESTAT_APPID` を用います。
        次のページから取得できます。
        https://www.e-stat.go.jp/api/
        `appId`

    TODO
    ----
    * Fetch all rows by concatination
    """

    query = "getSimpleStatsList"
    table_tag = "STAT_INF"

    def __init__(
        self,
        code,
        limit=None,
        start_position=None,
        updated_date=None,
        version="3.0",
        lang="J",
        appid=None,
    ):
        self.code = code
        self.limit = limit
        self.start_position = start_position
        self.updated_date = updated_date
        self.version = version
        self.lang = lang
        self.appid = get_appid(appid)

        if self.appid is None:
            raise ValueError("アプリケーション ID が指定されていません。")
        if not (isinstance(code, str) and re.fullmatch(r"(\d{5}|\d{8})", code)):
            raise ValueError(
                "政府統計コードは 5 桁か 8 桁の数字を str 型で指定してください。\n"
                "e-Stat 提供データ: https://www.e-stat.go.jp/api/api-info/api-data"
            )

        if lang != "J":
            raise NotImplementedError  # TODO

    @property
    def params(self) -> dict:
        """
        リクエスト URL に与えるパラメタ群
        """
        params = {"appId": self.appid, "statsCode": self.code}

        if self.limit is not None:
            params["limit"] = self.limit
        if self.start_position is not None:
            params["startPosition"] = self.start_position
        if self.updated_date is not None:
            params["updatedDate"] = self.updated_date
        if self.lang is not None:
            params["lang"] = self.lang

        return params

    def read(self, **kwargs) -> pd.DataFrame:
        """
        統計表を取得します。

        Parameters
        ----------
        - **kwargs
            e-Stat API から取得した CSV データをパースする `pandas.read_csv` に与えるパラメータです。

        Returns
        -------
        dataframe : pandas.DataFrame
            統計表
        """
        response = self.get()
        response_parsed = self._parse_response_text(response.text)

        if "TABLE" not in response_parsed:
            msg = (
                f'{response_parsed["ERROR_MSG"]}'
                f'(STATUS: {response_parsed["STATUS"]})'
            )
            raise EStatError(msg)

        if "dtype" not in kwargs:
            # TODO better dtypes
            kwargs["dtype"] = str

        dataframe = pd.read_csv(io.StringIO(response_parsed["TABLE"]), **kwargs)

        return dataframe