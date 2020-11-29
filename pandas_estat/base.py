import re

import requests


class BaseReader:
    regex_code = r""
    query = ""  # e.g. getSimpleStatsList
    table_tag = ""

    @property
    def url(self):
        return f"https://api.e-stat.go.jp/rest/{self.version}/app/{self.query}"

    @property
    def params(self):
        """
        query parameters
        """

    def get(self):
        """
        GET response from e-Stat API.

        Returns
        -------
        response : requests.Response
        """
        return requests.get(self.url, params=self.params)

    def read(self):
        """
        get table
        """

    def _parse_response_text(self, text):
        """
        Parse response.text into `dict`.

        Parameters
        ----------
        - rext : str
            Response text.
        - table_tag : str
            "STAT_INF"
            "VALUE"

        Returns
        -------
        parsed_response_text : dict
            * STATUS
            * ERROR_MSG
            * DATE
            * TABLE
        """
        lines = text.split("\n")

        parsed = {}
        for i, line in enumerate(lines):
            match = re.match(r"\"([A-Z_]+)\",\"([^\"]+)\"", line)

            if match:
                key, value = match.group(1), match.group(2)
                parsed[key] = value
            elif line == f'"{self.table_tag}"':
                value = "\n".join(lines[i + 1 :])
                parsed["TABLE"] = value
                break

        return parsed
