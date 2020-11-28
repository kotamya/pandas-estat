# Pandas e-Stat

[![python versions](https://img.shields.io/pypi/pyversions/pandas-estat.svg)](https://pypi.org/project/pandas-estat/)
[![version](https://img.shields.io/pypi/v/pandas-estat.svg)](https://pypi.org/project/pandas-estat/)
<!-- [![build status](https://travis-ci.com/simaki/pandas-estat.svg?branch=master)](https://travis-ci.com/simaki/pands-estat) -->
<!-- [![codecov](https://codecov.io/gh/simaki/pandas_estat/branch/master/graph/badge.svg)](https://codecov.io/gh/simaki/pandas_estat) -->
[![dl](https://img.shields.io/pypi/dm/pandas_estat)](https://pypi.org/project/pandas_estat/)
[![LICENSE](https://img.shields.io/github/license/simaki/pandas-estat)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[政府統計総合窓口 e-Stat](https://www.e-stat.go.jp/) の統計データを `pandas.DataFrame` 形式で取得します。

## インストール

```sh
pip install pandas-estat
```

## 使い方

### アプリケーション ID の取得

Pandas e-Stat を利用するには、e-Stat API 機能のアプリケーション ID が必要です。
[e-Stat API 機能](https://www.e-stat.go.jp/api/) にユーザ登録し、アプリケーション ID を取得してください。

アプリケーション ID は、環境変数 `ESTAT_APPID` に設定するか、次のように設定します。

```python
import pandas_estat

pandas_estat.set_appid("YOUR_APPLICATION_ID")
```

### 統計表情報の取得

統計表情報を取得します。

e-Stat API が提供する統計データは、[e-Stat 提供データ](https://www.e-stat.go.jp/api/api-info/api-data) から確認できます。
表示されている統計一覧が、現在 API が提供している統計データです。

<!-- screen shot -->

例として、景気ウォッチャー調査 (政府統計コード `00100001`) の統計表情報を取得します。
関数 `read_statslist` は、政府統計コードから統計表情報を `pandas.DataFrame` 形式で取得します。

```python
from pandas_estat import read_statslist

dataframe = read_statslist("00100001")
dataframe
#     TABLE_INF STAT_CODE  ... SUB_CATEGORY_CODE SUB_CATEGORY
# 0  0003348423  00100001  ...                06           景気
# 1  0003348424  00100001  ...                06           景気
# 2  0003348425  00100001  ...                06           景気
# 3  0003348426  00100001  ...                06           景気
# 4  0003348427  00100001  ...                06           景気
```

第一列目の `TABLE_INF` が統計表 ID です。

### 統計データの取得

例として、景気ウォッチャー調査のうち、統計表 ID `0003348423` に該当する統計データを取得します。
関数 `read_statsdata` は、統計表 ID から統計データを `pandas.DataFrame` 形式で取得します。

```python
from pandas_estat import read_statsdata

dataframe = read_statsdata("0003348423")
dataframe
#   tab_code 表章項目 cat01_code  分野  ...   時間軸(月次) unit value annotation
# 0      140   ＤＩ        100  合計  ...   2019年2月  NaN  47.5        NaN
# 1      140   ＤＩ        100  合計  ...   2019年1月  NaN  45.6        NaN
# 2      140   ＤＩ        100  合計  ...  2018年12月  NaN  46.8        NaN
# 3      140   ＤＩ        100  合計  ...  2018年11月  NaN  49.5        NaN
# 4      140   ＤＩ        100  合計  ...  2018年10月  NaN  48.6        NaN
```

## クレジット

このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。

## 謝辞

* [sinhrks/japandas](https://github.com/sinhrks/japandas)
