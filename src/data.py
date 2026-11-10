from __future__ import annotations

import os
import polars as pl

from typing import Optional, Dict

from src.config import DATA_DIRECTORY_ABS_PATH, DATA_CSV_FILENAME, DATA_SCHEMA_OVERRIDES



def load_csv_data_file (

        filename : Optional[str] = None,
        dir_abs_path : Optional[str] = None,

        schema_overrides : Optional[Dict] = None

    ) -> Optional[pl.DataFrame] :
    """

    """
    filename = DATA_CSV_FILENAME if filename is None else filename
    dir_abs_path = DATA_DIRECTORY_ABS_PATH if dir_abs_path is None else dir_abs_path

    data_file = os.path.join(dir_abs_path, filename)

    if data_file is None :

        print("[-] No data file path provided to load CSV data file.")
        return None

    if not os.path.exists(data_file) :
        
        print("[-] Data file not found.")
        return None

    schema_overrides = DATA_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides

    dataframe = pl.read_csv(data_file, schema_overrides=schema_overrides)

    return dataframe
