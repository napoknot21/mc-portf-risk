from __future__ import annotations

import os
import polars as pl

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR_ROOT = Path(__file__).resolve().parent.parent


# Different paths

DATA_DIRECTORY_NAME = "data"
DATA_DIRECTORY_ABS_PATH = str(os.path.join(BASE_DIR_ROOT,DATA_DIRECTORY_NAME))

DATA_CSV_FILENAME = "data.csv"
DATA_EXCEL_FILENAME = "data.xlsx"

DATA_SCHEMA_OVERRIDES = {
    
    "Date" : pl.Date,
    "EFA" : pl.Float64,
    "GLD" : pl.Float64,
    "TLT" : pl.Float64

}


