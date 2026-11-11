from __future__ import annotations

import os
import polars as pl

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR_ROOT = Path(__file__).resolve().parent.parent

# Portfolio variables

PORTFOLIO_VALUE_0 = 1_000_000.00

ACTIVE_WEIGHTS = {

    "EFA" : 0.15,
    "GLD" : 0.15,
    "SPY" : 0.40,
    "TLT" : 0.30,

}

# Different paths

DATA_DIRECTORY_NAME = "data"
DATA_DIRECTORY_ABS_PATH = str(os.path.join(BASE_DIR_ROOT,DATA_DIRECTORY_NAME))

DATA_CSV_FILENAME = "data.csv"
DATA_EXCEL_FILENAME = "data.xlsx"

DATA_SCHEMA_OVERRIDES = {
    
    "Date" : pl.Date,
    "EFA" : pl.Float64,
    "GLD" : pl.Float64,
    "SPY" : pl.Float64,
    "TLT" : pl.Float64

}


# Plots and images paths

PLOTS_DIRECTORY_NAME = "imgs"
PLOTS_DIRECTORY_ABS_PATH = str(os.path.join(BASE_DIR_ROOT,PLOTS_DIRECTORY_NAME))


