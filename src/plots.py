from __future__ import annotations

import numpy as np
import polars as pl
import scipy.stats as stats
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter
from typing import Optional, Dict

from src.config import PLOTS_DIRECTORY_ABS_PATH


def plot_histogram_returns (

        pnl_df : Optional[pl.DataFrame] = None,
        statisctics : Optional[Dict[str, Optional[float]]] = None,

        portfolio_return_col : str = "Portfolio_Return",
        mean_daily : str = "mean_daily",
        vol_daily : str = "vol_daily"

    ) -> None :
    """
    """
    if pnl_df is None or pnl_df.is_empty() :

        print("[-] No PnL data available to plot histogram.")
        return None

    returns = pnl_df.select(pl.col(portfolio_return_col)).to_numpy().flatten()

    if statisctics is None or not statisctics :

        print("[-] No statistics available to plot histogram.")
        return None

    mu, sigma = statisctics[mean_daily], statisctics[vol_daily]
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))

    for a, log_scale in zip(ax, [False, True]) :

        a.hist(returns, bins=100, density=True, alpha=0.5, label="observed")

        x = np.linspace(returns.min(), returns.max(), 500)
        a.plot(x, stats.norm.pdf(x, mu, sigma), lw=2, label="normale N(μ, σ)")

        if log_scale :
            a.set_yscale("log")

        a.set_title("log scale" if log_scale else "normal scale")
        a.legend()

    plt.tight_layout()
    plt.show()

    return None


def historgram_returns_plot (
        
        pnl_df: Optional[pl.DataFrame] = None,
        statistics: Optional[Dict[str, float]] = None,

        portfolio_return_col: str = "Portfolio_Return",

        n_bins: int = 100,
        save: bool = True,

    ) -> None :
    """
    Histogram of daily portfolio returns vs a normal with the same mean and vol,
    on a linear scale (the centre) and a log scale (the tails).
    """
    if pnl_df is None or pnl_df.is_empty() :

        print("[-] No PnL data available to plot histogram."); return None
        return None

    returns = pnl_df.select(pl.col(portfolio_return_col)).to_numpy().flatten()

    if not statistics :
        
        print("[-] No statistics available to plot histogram."); return None
        return None
 
    mu, sigma = statistics["mean_daily"], statistics["vol_daily"]

    # 2. Shared bins, so both panels are comparable
    bin_edges = np.linspace(returns.min(), returns.max(), n_bins + 1)
    one_day_density = 1.0 / (len(returns) * (bin_edges[1] - bin_edges[0]))  # height of a 1-day bar
    
    x = np.linspace(returns.min(), returns.max(), 500)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, log_scale in zip(axes, [False, True]):
        # 3. Observed vs normal
        ax.hist(returns, bins=bin_edges, density=True, alpha=0.55,
                label=f"Observed daily returns (n = {len(returns):,})")

        ax.plot(x, stats.norm.pdf(x, mu, sigma), lw=2,
                label=f"Normal N(μ, σ), σ = {sigma:.2%}")

        # 4. ±4σ markers: beyond them, a normal says "almost never"
        for k in (-4, 4):
            ax.axvline(mu + k * sigma, color="grey", ls=":", lw=1)

        # 5. Axes and titles
        ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
        ax.set_xlabel("Daily portfolio return")

        if log_scale :

            ax.set_yscale("log")
            ax.set_ylim(0.5 * one_day_density, 3 * stats.norm.pdf(mu, mu, sigma))
            
            ax.set_ylabel("Density (log scale)")
            ax.set_title("Log scale: the tails\n(dotted = ±4σ; lowest bars = a single day)")
        
        else :

            ax.set_ylabel("Density")
            ax.set_title("Linear scale: the centre of the distribution")
        
        ax.legend(loc="upper left", fontsize=9, frameon=False)
        ax.grid(alpha=0.3)

    fig.suptitle(
        f"Daily portfolio returns vs normal  |  vol {statistics['vol_annual']:.1%}/yr, "
        f"skew {statistics['skew']:.2f}, excess kurtosis {statistics['excess_kurtosis']:.1f}")
    fig.tight_layout()

    # 6. Save (you imported PLOTS_DIRECTORY_ABS_PATH but never used it)
    if save:
        fig.savefig(f"{PLOTS_DIRECTORY_ABS_PATH}/returns_histogram.png", dpi=150)
    
    plt.show()

    return None