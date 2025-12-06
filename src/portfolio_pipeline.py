import sys
import os

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import yfinance as yf
import pyomo.environ as pyo
from pyomo.environ import (
    ConcreteModel, Set, Var, NonNegativeReals, Binary,
    Objective, Constraint, ConstraintList, minimize, SolverFactory, TerminationCondition
)

def BDM_Project(tickers, start_date, end_date, initial_return_range=(0.005, 0.03), step=0.001, max_assets=5):
    output_dir = "BDM_Outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Data
    price_data = {}
    for t in tickers:
        try:
            df = yf.download(t, start=start_date, end=end_date, interval="1d", progress=False, auto_adjust=False)
            if not df.empty and 'Adj Close' in df.columns:
                price_data[t] = df['Adj Close']
            else:
                print(f"Warning: no valid data for {t}")
        except Exception as e:
            print(f"Failed {t}: {e}")
    if not price_data:
        print("No valid data retrieved.")
        return None

    prep_data = pd.concat(price_data.values(), axis=1)
    prep_data.columns = list(price_data.keys())
    if prep_data.empty or prep_data.isnull().all().all():
        print("No valid adjusted close data available. Aborting.")
        return None

    # Returns and matrices
    daily_returns = prep_data.pct_change().dropna()
    log_returns = np.log(prep_data / prep_data.shift(1)).dropna()
    monthly_returns = prep_data.resample('ME').ffill().pct_change().dropna()
    avg_return = monthly_returns.mean()
    cov_matrix = monthly_returns.cov()
    cor_matrix = monthly_returns.corr()

    # Plots
    (1 + daily_returns).cumprod().plot(figsize=(15, 10))
    plt.title('Cumulative Percentage Returns Over Time')
    plt.xlabel('Date'); plt.ylabel('Cumulative Return'); plt.grid(True); plt.tight_layout()
    plt.savefig(f"{output_dir}/cumulative_returns.png"); plt.close()

    n = len(tickers)
    cols = math.ceil(math.sqrt(n)); rows = math.ceil(n / cols)
    daily_returns.plot(subplots=True, grid=True, layout=(rows, cols), figsize=(4 * cols, 3 * rows))
    plt.suptitle('Daily Simple Returns'); plt.tight_layout()
    plt.savefig(f"{output_dir}/daily_returns.png"); plt.close()

    monthly_returns.plot(figsize=(15, 6), title='Monthly Returns')
    plt.grid(True); plt.tight_layout()
    plt.savefig(f"{output_dir}/monthly_returns.png"); plt.close()

    plt.figure(figsize=(15, 12))
    sns.heatmap(cov_matrix, annot=True, cmap='coolwarm', fmt=".4f", center=0)
    plt.title('Covariance Matrix of Monthly Returns'); plt.tight_layout()
    plt.savefig(f"{output_dir}/covariance_heatmap.png"); plt.close()

    plt.figure(figsize=(15, 12))
    sns.heatmap(cor_matrix, annot=True, cmap='coolwarm', fmt=".4f", center=0)
    plt.title('Correlation Matrix of Monthly Returns'); plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png"); plt.close()

    # Model
    def build_model(target_return):
        m = ConcreteModel()
        m.assets = Set(initialize=tickers)
        m.x = Var(m.assets, domain=NonNegativeReals, bounds=(0, 1))
        m.y = Var(m.assets, domain=Binary)

        def portfolio_variance(m):
            return sum(m.x[i] * cov_matrix.loc[i, j] * m.x[j] for i in m.assets for j in m.assets)
        m.obj = Objective(rule=portfolio_variance, sense=minimize)

        m.total_allocation = Constraint(expr=sum(m.x[i] for i in m.assets) == 1)
        m.target_return = Constraint(expr=sum(m.x[i] * avg_return[i] for i in m.assets) >= target_return)

        bigM = 1.0
        m.link_binary = ConstraintList()
        for i in m.assets:
            m.link_binary.add(m.x[i] <= bigM * m.y[i])

        m.max_assets = Constraint(expr=sum(m.y[i] for i in m.assets) <= max_assets)
        return m

    def solve_and_extract(m):
        SolverFactory("bonmin").solve(m)
        solution = {i: m.x[i].value or 0.0 for i in m.assets}
        port_return = sum(solution[i] * avg_return[i] for i in m.assets)
        port_variance = sum(solution[i] * cov_matrix.loc[i, j] * solution[j] for i in m.assets for j in m.assets)
        port_risk = float(np.sqrt(port_variance))
        return solution, port_return, port_risk

    # Frontier
    min_r, max_r = initial_return_range
    current_r = min_r
    results = []
    max_concentration_reached = False

    while not max_concentration_reached and current_r <= max_r + 0.1:
        m = build_model(target_return=current_r)
        result = SolverFactory("bonmin").solve(m)
        if result.solver.termination_condition != TerminationCondition.optimal:
            print(f"Skipping return target {current_r:.4f} — infeasible.")
            current_r += step
            continue
        try:
            solution, port_return, port_risk = solve_and_extract(m)
            clean_weights = {t: solution.get(t, 0.0) for t in tickers}
            results.append({
                "target_return": current_r,
                "actual_return": port_return,
                "risk": port_risk,
                "weights": clean_weights
            })
            nonzero_weights = [w for w in clean_weights.values() if w >= 0.01]
            if len(nonzero_weights) == 1 and abs(nonzero_weights[0] - 1.0) < 0.01:
                max_concentration_reached = True
        except Exception as e:
            print(f"Error at return {current_r:.4f}: {e}")
        current_r += step

    if not results:
        print("No feasible portfolios found.")
        return None

    frontier_df = pd.DataFrame(results).dropna().sort_values("risk")
    plt.figure(figsize=(8, 5))
    plt.plot(frontier_df["risk"], frontier_df["actual_return"], marker='o', linestyle='-', color='blue')
    plt.title("Efficient Frontier")
    plt.xlabel("Portfolio Risk (Standard Deviation)")
    plt.ylabel("Expected Return")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/efficient_frontier.png"); plt.close()

    alloc_data = []
    for r in results:
        weights = {t: r["weights"].get(t, 0.0) for t in tickers}
        alloc_data.append(weights)
    alloc_df = pd.DataFrame(alloc_data, index=[r["risk"] for r in results]).sort_index()

    plt.figure(figsize=(12, 6))
    for col in alloc_df.columns:
        plt.plot(alloc_df.index, alloc_df[col], label=col)
    plt.title("Asset Allocation vs. Portfolio Risk (Spaghetti Plot)")
    plt.xlabel("Portfolio Risk (Standard Deviation)")
    plt.ylabel("Weight")
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/allocation_spaghetti.png"); plt.close()

    # Allocation bar charts with % labels
    def plot_allocation(weights_dict, title, filename):
        if not weights_dict:
            print(f"Skipping {title} — no weights found.")
            return
        plt.figure(figsize=(10, 6))
        bars = plt.bar(weights_dict.keys(), weights_dict.values())
        plt.title(title)
        plt.xlabel("Assets")
        plt.ylabel("Weight")
        plt.xticks(rotation=45)
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    h,
                    f"{h:.1%}",
                    ha="center",
                    va="bottom",
                    fontsize=9
                )
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{filename}")
        plt.close()

    conservative = frontier_df.iloc[0]
    balanced = frontier_df.iloc[len(frontier_df)//2]
    high_risk = frontier_df.iloc[-1]

    plot_allocation(conservative["weights"], "Conservative Portfolio Allocation", "alloc_conservative.png")
    plot_allocation(balanced["weights"], "Balanced Portfolio Allocation", "alloc_balanced.png")
    plot_allocation(high_risk["weights"], "High-Risk Portfolio Allocation", "alloc_highrisk.png")

    # Save outputs
    daily_returns.to_csv(f"{output_dir}/daily_returns.csv")
    log_returns.to_csv(f"{output_dir}/log_returns.csv")
    monthly_returns.to_csv(f"{output_dir}/monthly_returns.csv")
    cov_matrix.to_csv(f"{output_dir}/covariance_matrix.csv")
    cor_matrix.to_csv(f"{output_dir}/correlation_matrix.csv")
    frontier_df.to_csv(f"{output_dir}/efficient_frontier.csv", index=False)
    alloc_df.to_csv(f"{output_dir}/allocations.csv")

    print(f"All outputs saved to folder: {output_dir}")

    return {
        "daily_returns": daily_returns,
        "log_returns": log_returns,
        "monthly_returns": monthly_returns,
        "covariance_matrix": cov_matrix,
        "correlation_matrix": cor_matrix,
        "efficient_frontier": frontier_df,
        "allocations": alloc_df
    }
    
