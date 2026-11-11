from __future__ import annotations

import os
import polars as pl 
import numpy as np
import scipy.stats as stats

from typing import Optional, Dict

from src.config import DATA_SCHEMA_OVERRIDES, PORTFOLIO_VALUE_0, ACTIVE_WEIGHTS
from src.returns import compute_portfolio_pnl


def compute_return_statistics (

        pnl_df : Optional[pl.DataFrame] = None,

        return_column_name : str = "Portfolio_Return",
        trading_days : int = 252,

    ) -> Optional[Dict[str, float]] :
    """

    """
    pnl_df = compute_portfolio_pnl() if pnl_df is None else pnl_df

    if pnl_df is None or pnl_df.is_empty() :

        print("[-] No PnL data available to compute return statistics.")
        return None

    statistics = {

        "mean_daily" : None,
        "mean_annual" : None,
        "vol_daily" : None,
        "vol_annual" : None,
        "skew" : None,
        "excess_kurtosis" : None
    
    }

    portfolio_return = pnl_df.select(pl.col(return_column_name)).to_numpy().flatten()

    statistics["mean_daily"] = float(portfolio_return.mean())
    statistics["mean_annual"] = float(statistics["mean_daily"] * trading_days)

    statistics["vol_daily"] = float(portfolio_return.std(ddof=1))
    statistics["vol_annual"] = float(statistics["vol_daily"] * np.sqrt(trading_days))

    statistics["skew"] = float(stats.skew(portfolio_return))
    statistics["excess_kurtosis"] = float(stats.kurtosis(portfolio_return))
    
    return statistics

