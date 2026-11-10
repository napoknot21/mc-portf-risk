from __future__ import annotations

import os
import polars as pl


from src.data import load_csv_data_file
from src.returns import compute_daily_log_returns


def main () -> None :
    """

    """
    
    dataframe = load_csv_data_file()
    print(dataframe)

    log_returns = compute_daily_log_returns(dataframe)
    print(log_returns)

    return 0


if __name__ == "__main__" :
    main()
    
