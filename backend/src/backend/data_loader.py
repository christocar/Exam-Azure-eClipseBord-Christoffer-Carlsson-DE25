from pathlib import Path

import pandas as pd

# relative to where the app is started from: repo root locally, /app in the container
DATA_PATH = Path("data") / "solar.csv"


def load_eclipses() -> pd.DataFrame:
    # read everything as strings, we do the conversions ourselves below
    df = pd.read_csv(DATA_PATH, dtype=str)

    # year can be negative (BC), so pandas can't parse it as a date
    # taking the year as an int instead, month and day don't matter over 5000 years
    df["year"] = df["Calendar Date"].str.split(" ").str[0].astype(int)

    # group the 19 type codes into the 4 main types (T, A, P, H)
    df["type"] = df["Eclipse Type"].str[0]

    # coerce turns bad values into NaN instead of raising
    df["magnitude"] = pd.to_numeric(df["Eclipse Magnitude"], errors="coerce")

    # only the columns the API actually serves
    return df[["Catalog Number", "Calendar Date", "year", "type", "magnitude"]]