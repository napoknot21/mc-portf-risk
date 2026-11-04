from __future__ import annotations

import os
import polars as pl


from src.data import load_csv_data_file


dataframe = load_csv_data_file()

print(dataframe)
