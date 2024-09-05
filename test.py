from main import *
from yankesSearch import *

import pandas


def join(filenames):
    frames = []

    for item in filenames:
        df = pandas.read_csv(item)

        frames.append(df)

    return pandas.concat(frames)

def final():
    filenames = [
        "praktekmandiri_updategmaps1050-1101.csv",
        "praktekmandiri_updategmaps1100-1151.csv",
        "praktekmandiri_updategmaps1150-1200.csv",
    ]

    df = join(filenames)

    df.to_csv("praktekmandiri1050-1200.csv", index=False)




if __name__ == "__main__":
    filename = "praktekmandiri.csv"
    googleSearch(filename, 0, 51)

    # search(filename)

    # final()

