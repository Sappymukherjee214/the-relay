import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_charts():
    os.makedirs("submission/figures", exist_ok=True)
    df = pd.read_csv("results.csv")

    # Chart 1: TTFT distribution across scenarios
    plt.figure(figsize=(8, 5))
    scenarios = df["scenario"].unique()
    ttft_data = [df[df["scenario"] == s]["first_token_ms"] for s in scenarios]
    plt.boxplot(ttft_data, labels=scenarios)
    plt.title("TTFT Distribution Across Load Scenarios")
    plt.ylabel("First Token Latency (ms)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("submission/figures/ttft_distribution.png")
    plt.close()

    # Chart 2: Success rate across scenarios
    success_rates = []
    for s in scenarios:
        s_df = df[df["scenario"] == s]
        succ = (len(s_df[s_df["status"] == "ok"]) / len(s_df)) * 100
        success_rates.append(succ)

    plt.figure(figsize=(8, 5))
    plt.bar(scenarios, success_rates, color='skyblue')
    plt.title("Success Percentage Across Scenarios")
    plt.ylabel("Success Rate (%)")
    plt.ylim(0, 105)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("submission/figures/success_rate.png")
    plt.close()

    print("Charts generated successfully under submission/figures/")

if __name__ == "__main__":
    generate_charts()
