import os
from typing import Optional


class _GlobalAppID:
    """Singleton object to configure global app id.

    Args:
        value (str): Application ID.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance._appid = None
        return cls._instance

    def set_appid(self, appid: Optional[str]) -> None:
        self._appid = appid

    def get_appid(self) -> Optional[str]:
        return self._appid


_global_appid = _GlobalAppID()


def set_appid(appid: Optional[str]) -> None:
    """アプリケーション ID を設定します。

    Args:
        appid (str): 設定するアプリケーション ID です。
    """
    _global_appid.set_appid(appid)


def get_appid(appid: Optional[str] = None) -> Optional[str]:
    """Get Application ID.

    The Parameter `appid`, global app ID in `_GlobalAppID`, and
    environment variable `ESTAT_APPID` are referenced in order.
    If these are all None, return None.

    Args:
        appid (str, optional): If given, just return this.

    Returns:
        str, optional
    """
    if appid is not None:
        return appid
    elif _global_appid.get_appid() is not None:
        return _global_appid.get_appid()
    elif "ESTAT_APPID" in os.environ:
        return os.environ["ESTAT_APPID"]
    else:
        return None
