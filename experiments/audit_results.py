import pandas as pd
import numpy as np

def audit_results():
    df = pd.read_csv("results.csv")
    print("=== INDEPENDENT AUDIT OF RESULTS.CSV ===")
    print(f"Total rows: {len(df)}")

    # Check mandatory columns
    expected_cols = [
        "request_id", "scenario", "source", "start_time",
        "first_token_ms", "total_ms", "status", "retries",
        "tokens_in", "tokens_out", "retrieval_setting", "answer_grade"
    ]
    assert list(df.columns) == expected_cols, f"Column mismatch: {df.columns}"
    print("Column check: PASSED")

    # Check unique request IDs
    assert df["request_id"].is_unique, "Duplicate request IDs found!"
    print("Unique request IDs check: PASSED")

    # Check allowed values
    valid_statuses = {"ok", "rate_limited", "timeout", "error"}
    assert set(df["status"].unique()).issubset(valid_statuses), f"Invalid status found: {df['status'].unique()}"
    print("Status values check: PASSED")

    valid_sources = {"real", "stand-in"}
    assert set(df["source"].unique()).issubset(valid_sources), f"Invalid source found: {df['source'].unique()}"
    print("Source values check: PASSED")

    # Recalculate metrics per scenario
    for scenario in df["scenario"].unique():
        s_df = df[df["scenario"] == scenario]
        ok_df = s_df[s_df["status"] == "ok"]

        succ_pct = (len(ok_df) / len(s_df)) * 100
        rate_pct = (len(s_df[s_df["status"] == "rate_limited"]) / len(s_df)) * 100
        timeout_pct = (len(s_df[s_df["status"].isin(["timeout", "error"])]) / len(s_df)) * 100

        print(f"\nScenario: {scenario}")
        print(f"  Count: {len(s_df)}")
        print(f"  Success %: {succ_pct:.1f}%")
        print(f"  Rate-limited %: {rate_pct:.1f}%")
        print(f"  Timeout/Error %: {timeout_pct:.1f}%")
        print(f"  Mean Retries: {s_df['retries'].mean():.2f}")
        if len(ok_df) > 0:
            print(f"  TTFT p50: {ok_df['first_token_ms'].quantile(0.5):.2f} ms")
            print(f"  Total p50: {ok_df['total_ms'].quantile(0.5):.2f} ms")
            print(f"  Total p95: {ok_df['total_ms'].quantile(0.95):.2f} ms")
            print(f"  Tokens out mean: {ok_df['tokens_out'].mean():.1f}")

if __name__ == "__main__":
    audit_results()
