# Pandas e-Stat

[政府統計総合窓口 e-Stat](https://www.e-stat.go.jp/) の統計データを `pandas.DataFrame` 形式で取得します。

## インストール

```sh
pip install pandas_estat
```

## 使い方

### アプリケーション ID の取得

まず、[e-Stat API 機能](https://www.e-stat.go.jp/api/) にユーザ登録し、アプリケーション ID を取得します。

取得したアプリケーション ID は、環境変数 `ESTAT_APPID` に設定するか、次のように設定します。

```python
import pandas_estat

pandas_estat.set_appid(...)  # Your application id
```

### 統計データ一覧の取得

まず、統計データ一覧を取得します。

APIで提供する統計データは、[e-Stat 提供データ](https://www.e-stat.go.jp/api/api-info/api-data) から確認できます。
表示されている統計一覧が、現在 API が提供している統計データです。

<!-- screen shot -->

例として、景気ウオッチャー調査の統計データを取得します。

```python
from pandas_estat import read_statslist

read_statslist("00100001")
# ...
```

第一行目 `TABLE_INF` が統計表 ID です。

### 統計データ一覧の取得

統計表 ID `0003348423` に該当する統計データを取得します。

```python
from pandas_estat import read_statslist

read_statslist("0003348423")
# ...
```

## クレジット

このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。

## 謝辞

* [sinhrks/japandas](https://github.com/sinhrks/japandas)
