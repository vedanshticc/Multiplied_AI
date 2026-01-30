import json
import pandas as pd

def json_to_df(json_file) -> pd.DataFrame:
    data = json.load(json_file)
    df = pd.json_normalize(data)

    # Standardize column names
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    return df
