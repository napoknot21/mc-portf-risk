from __future__ import annotations

import polars as pl
import numpy as np

from typing import Optional, Dict

from src.config import DATA_SCHEMA_OVERRIDES, PORTFOLIO_VALUE_0, ACTIVE_WEIGHTS
from src.data import load_csv_data_file


def compute_daily_log_returns (

        dataframe : Optional[pl.DataFrame] = None,

        schema_overrides : Optional[Dict] = None,
        date_column_name : str = "Date"

    ) -> Optional[pl.DataFrame] :
    """

    """
    schema_overrides = DATA_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides
    dataframe = load_csv_data_file(schema_overrides=schema_overrides) if dataframe is None else dataframe

    if dataframe is None or dataframe.is_empty() :
        
        print("[-] No data available to compute daily log returns.")
        return None

    # log return needs at least 2 dates
    if dataframe.shape[0] < 2 :
        
        print("[-] Not enough data available to compute daily log returns.")
        return None

    tickets = [column for column in dataframe.columns if column != date_column_name]

    log_returns = dataframe.select(

        pl.col(date_column_name),
        *[
            (pl.col(column) / pl.col(column).shift(1)).log().alias(f"Log_{column}")
            for column in tickets
        ],

    ).slice(1)

    log_returns = log_returns.cast({f"Log_{column}": pl.Float64 for column in tickets})

    return log_returns



def compute_portfolio_pnl (

        dataframe : Optional[pl.DataFrame] = None,
        schema_overrides : Optional[Dict] = None,

        log_returns : Optional[pl.DataFrame] = None,

        portfolio_value_0 : Optional[float] = None,
        active_weights : Optional[Dict] = None,

        date_column_name : str = "Date",
        portf_columns_name : str = "Portfolio_Return",
        pnl_column_name : str = "PnL"

    ) -> Optional[pl.DataFrame] :
    """

    """
    schema_overrides = DATA_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides
    dataframe = load_csv_data_file(schema_overrides=schema_overrides) if dataframe is None else dataframe

    if dataframe is None or dataframe.is_empty() :

        print("[-] No data available to compute portfolio PnL.")
        return None

    portfolio_value_0 = PORTFOLIO_VALUE_0 if portfolio_value_0 is None else portfolio_value_0
    active_weights = ACTIVE_WEIGHTS if active_weights is None else active_weights

    if _check_weights_sum(active_weights) is False :

        print("[-] Active weights do not sum to 1. Cannot compute portfolio PnL.")
        return None

    log_returns = compute_daily_log_returns(dataframe) if log_returns is None else log_returns

    if log_returns is None or log_returns.is_empty() :

        print("[-] No log returns available to compute portfolio PnL.")
        return None

    # 1. Contribution of each ticker, in decimal: w_i * (exp(r_i) - 1)
    contribution_columns = [f"Contrib_{ticker}" for ticker in active_weights]

    weighted_simple_returns = [

        (weight * (pl.col(f"Log_{ticker}").exp() - 1)).alias(f"Contrib_{ticker}")
        for ticker, weight in active_weights.items()

    ]

    pnl_df = log_returns.select(pl.col(date_column_name), *weighted_simple_returns)

    pnl_df = pnl_df.with_columns(pl.sum_horizontal(contribution_columns).alias(portf_columns_name))
    
    pnl_df = pnl_df.with_columns((portfolio_value_0 * pl.col(portf_columns_name)).alias(pnl_column_name))

    return pnl_df


def _check_weights_sum (active_weights : Optional[Dict] = None) -> bool :
    """
    This function checs if the sum of active's weight is 1
    """
    active_weights = ACTIVE_WEIGHTS if active_weights is None else active_weights
    weights_sum = sum(active_weights.values())

    return bool(np.isclose(weights_sum, 1.0))
