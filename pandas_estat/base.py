import abc
import io
import re

import pandas as pd
import requests

from .exceptions import EStatError


class BaseReader(abc.ABC):
    """
    Base class of all readers in `pandas-estat`.
    `StatsListReader` and `StatsDataReader` subclass this.

    Attributes
    ----------
    - QUERY : str
        e-Stat API のリクエスト URL におけるクエリパラメータです。(参照: parameter `url`)
        例えば、統計表情報は `getSimpleStatsList`, 統計データは `getSimpleStatsList` です。
        参照: e-Stat API v3.0 仕様 2. API の利用方法
    - TABLE_TAG : str
        表データを示すタグ名です。
        例えば、統計表情報は `STAT_INF`, 統計データは `VALUE` です。
        参照: e-Stat API v3.0 仕様 4. API の出力データ

    References
    ----------
    e-Stat API v3.0 仕様
    https://www.e-stat.go.jp/api/sites/default/files/uploads/2019/07/API-specVer3.0.pdf
    """

    QUERY = NotImplemented
    TABLE_TAG = NotImplemented

    @property
    def url(self) -> str:
        """
        e-Stat API のリクエスト URL です。
        参照: e-Stat API v3.0 仕様 2. API の利用方法

        Returns
        -------
        - url : str
        """
        return f"https://api.e-stat.go.jp/rest/{self.version}/app/{self.QUERY}"

    @property
    @abc.abstractmethod
    def params(self) -> dict:
        """
        e-Stat API のパラメータ群を `dict` 形式で返します。
        参照: e-Stat API v3.0 仕様 2. API の利用方法
        参照: e-Stat API v3.0 仕様 3. API パラメータ

        Returns
        -------
        params : dict
        """

    def read(self, **kwargs) -> pd.DataFrame:
        """
        e-Stat API から表データを取得し、`pandas.DataFrame` 形式で返します。

        Parameters
        ----------
        - **kwargs
            e-Stat API から取得した CSV データをパースする `pandas.read_csv` に与えるパラメータです。

        Returns
        -------
        dataframe : pandas.DataFrame
            表データ
        """
        response = self.get()
        response_parsed = self._parse_response_text(response.text)

        if "TABLE" not in response_parsed:
            message = response_parsed.get("ERROR_MSG", "")
            status = response_parsed.get("STATUS", "")
            raise EStatError(f"{message} (STATUS: {status})")

        if "dtype" not in kwargs:
            kwargs["dtype"] = str

        dataframe = pd.read_csv(io.StringIO(response_parsed["TABLE"]), **kwargs)

        return dataframe

    def get(self) -> requests.Response:
        """
        e-Stat API からレスポンスを GET し、`requests.Response` 形式で返します。

        Returns
        -------
        response : requests.Response
        """
        return requests.get(self.url, params=self.params)

    def _parse_response_text(self, text) -> dict:
        """
        e-Stat API からのレスポンスのテキストをパースし、`dict` 形式で返します。
        表データのキーは `TABLE` とし、他の値のキーは e-Stat API のタグ名とします。
        参照: e-Stat API v3.0 仕様 4. API の出力データ

        Parameters
        ----------
        - text : str
            レスポンスのテキストです。

        Returns
        -------
        parsed_response_text : dict
            辞書にパースされたレスポンスのテキストです。
            キーの例は `TABLE`, `DATE`, `STATUS`, `ERROR_MSG` などです。
        """
        lines = text.splitlines()

        parsed = {}
        for i, line in enumerate(lines):
            match = re.match(r"\"([A-Z_]+)\",\"([^\"]+)\"", line)
            if match:
                key, value = match.group(1), match.group(2)
                parsed[key] = value
            elif line == f'"{self.TABLE_TAG}"':
                key, value = "TABLE", "\n".join(lines[i + 1 :])
                parsed[key] = value
                break

        return parsed
