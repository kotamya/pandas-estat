import sys

sys.path.append("..")

import pandas_estat


def print_as_comment(obj):
    print("\n".join(f"# {line}" for line in str(obj).splitlines()))


if __name__ == "__main__":
    import pandas as pd
    import pandas_estat

    from pandas_estat import read_statslist

    statslist = read_statslist("00200544")  # サービス産業動向調査
    print(">>> statslist")
    print_as_comment(statslist)

    # ---

    print('>>> statslist[["TABLE_INF", "CYCLE"]]')
    print_as_comment(statslist[["TABLE_INF", "CYCLE"]])

    # ---

    statslist = statslist[statslist.CYCLE == "月次"]
    print('>>> statslist[["TABLE_INF", "TITLE"]]')
    print_as_comment(statslist[["TABLE_INF", "TITLE"]])

    # ---

    from pandas_estat import read_statsdata

    dataframe = read_statsdata("0003191203")  # 事業活動の産業（中分類）別売上高（月次）【2013年1月～】
    print(">>> dataframe")
    print_as_comment(dataframe)

    print('>>> set(dataframe["事業活動の産業"])')
    print_as_comment(set(dataframe["事業活動の産業"]))

    # ---

    dataframe = dataframe[dataframe["事業活動の産業"] == "76飲食店"]
    dataframe = dataframe[dataframe["時間軸（月次）"].str.endswith("月")]
    dataframe["時間軸（月次）"] = pd.to_datetime(dataframe["時間軸（月次）"], format="%Y年%m月")
    dataframe = dataframe.sort_values("時間軸（月次）")

    print('>>> dataframe[["時間軸（月次）", "value", "unit"]]')
    print_as_comment(dataframe[["時間軸（月次）", "value", "unit"]])

    # ---

    import matplotlib.pyplot as plt
    import seaborn

    seaborn.set_style("whitegrid")

    x = dataframe["時間軸（月次）"].values
    y = dataframe["value"].values.astype(float) / 10e3  # 十億円

    plt.figure(figsize=(12, 4))
    plt.plot(x, y)
    plt.title("Restaurants Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue [bn JPY]")
    plt.savefig("restaurants.png", dpi=300, bbox_inches = 'tight', pad_inches=0.1)
    # plt.show()
