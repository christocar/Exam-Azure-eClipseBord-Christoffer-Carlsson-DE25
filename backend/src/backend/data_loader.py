from pathlib import Path

import pandas as pd

DATA_PATH = Path("data") / "solar.csv"


def load_eclipses() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, dtype=str)

    # year can be negative (BC), so pandas can't parse it as a date
    df["year"] = df["Calendar Date"].str.split(" ").str[0].astype(int)

    # group the 19 type codes into the 4 main types
    df["type"] = df["Eclipse Type"].str[0]

    df["magnitude"] = pd.to_numeric(df["Eclipse Magnitude"], errors="coerce")

    return df[["Catalog Number", "Calendar Date", "year", "type", "magnitude"]]