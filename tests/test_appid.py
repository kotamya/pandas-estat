import pytest
from unittest.mock import patch

import os

from pandas_estat.appid import get_appid
from pandas_estat.appid import set_appid
from pandas_estat.appid import _global_appid


class TestAppID:
    """
    Test Application ID.
    """

    @pytest.fixture(scope="function", autouse=True)
    def reset_global_appid(self):
        set_appid(None)

    def test_local_appid(self): #, env_appid, global_appid):
        """
        Local App ID is prioritized over env, global
        """
        with patch("os.environ", {"ESTAT_APPID": "ENV_APPID"}):
            set_appid("GLOBAL_APPID")
            assert get_appid("LOCAL_APPID") == "LOCAL_APPID"

    def test_global_appid(self):
        """
        Global App ID is prioritized over env.
        """
        with patch("os.environ", {"ESTAT_APPID": "ENV_APPID"}):
            set_appid("GLOBAL_APPID")
            assert get_appid() == "GLOBAL_APPID"

    def test_env_appid(self):
        """
        Environment App ID is used if none of local & global are not set.
        """
        with patch("os.environ", {"ESTAT_APPID": "ENV_APPID"}):
            assert get_appid() == "ENV_APPID"
