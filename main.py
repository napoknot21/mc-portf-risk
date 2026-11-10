from __future__ import annotations

import os
import polars as pl


from src.data import load_csv_data_file
from src.returns import compute_daily_log_returns, compute_portfolio_pnl


def main () -> None :
    """

    """
    
    dataframe = load_csv_data_file()
    print(dataframe)

    log_returns = compute_daily_log_returns(dataframe)
    print(log_returns)

    pnl_df = compute_portfolio_pnl(dataframe, log_returns=log_returns)

    print(pnl_df)

    return 0


if __name__ == "__main__" :
    main()

