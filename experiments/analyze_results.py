import pandas as pd
import numpy as np

def analyze():
    df = pd.read_csv("results.csv")
    print("=== RESULTS SUMMARY ===")
    print(f"Total requests: {len(df)}")

    # Table 2a and 2b aggregation
    for scenario in df["scenario"].unique():
        s_df = df[df["scenario"] == scenario]
        ok_df = s_df[s_df["status"] == "ok"]

        succeeded_pct = (len(ok_df) / len(s_df)) * 100
        rate_limited_pct = (len(s_df[s_df["status"] == "rate_limited"]) / len(s_df)) * 100
        timeout_pct = (len(s_df[s_df["status"].isin(["timeout", "error"])]) / len(s_df)) * 100

        print(f"\nScenario: {scenario}")
        print(f"  Requests sent: {len(s_df)}")
        print(f"  Succeeded %: {succeeded_pct:.1f}%")
        print(f"  Rate-limited %: {rate_limited_pct:.1f}%")
        print(f"  Timeout/Error %: {timeout_pct:.1f}%")
        if len(ok_df) > 0:
            print(f"  First token p50 (ms): {ok_df['first_token_ms'].quantile(0.5):.1f}")
            print(f"  Total p50 (ms): {ok_df['total_ms'].quantile(0.5):.1f}")
            print(f"  Avg retries: {s_df['retries'].mean():.2f}")
            print(f"  Tokens/answer: {ok_df['tokens_out'].mean():.1f}")

if __name__ == "__main__":
    analyze()
