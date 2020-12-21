import os


class _GlobalAppID:
    """
    Singleton object to configure global app id.

    Parameters
    ----------
    - value : str
        Application ID.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value


_global_appid = _GlobalAppID(None)


def set_appid(appid) -> None:
    _global_appid.value = appid


def get_appid(appid=None) -> str:
    """
    Get Application ID.

    The Parameter `appid`, global app ID in `_GlobalAppID`, and
    environment variable `ESTAT_APPID` are referenced in order.
    If these are all None, return None.

    Parameters
    ----------
    - appid : str, optional
        If given, just return this.

    Returns
    -------
    appid : str or None
        Application ID.
    """
    if appid is not None:
        return appid
    elif _global_appid.value is not None:
        return _global_appid.value
    elif "ESTAT_APPID" in os.environ:
        return os.environ["ESTAT_APPID"]
    else:
        return None
