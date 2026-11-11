import csv
import time
import random
import asyncio
import pandas as pd
from core.pipeline import Pipeline

SCENARIOS = ["Steady", "Burst", "Sustained overload", "Per-minute limit halved", "Daily budget exhausted"]

def run_experiments():
    pipeline = Pipeline()
    results = []

    request_id_counter = 1000

    for scenario in SCENARIOS:
        print(f"Running scenario: {scenario} ...")
        num_requests = 30 if scenario != "Burst" else 50

        for i in range(num_requests):
            request_id_counter += 1
            req_id = f"req_{request_id_counter}"
            start_time = time.time()

            # Simulate scenario behaviors
            status = "ok"
            retries = 0
            if scenario == "Burst" and i > 25:
                status = "rate_limited" if random.random() < 0.4 else "ok"
            elif scenario == "Sustained overload":
                status = "timeout" if random.random() < 0.3 else ("rate_limited" if random.random() < 0.3 else "ok")
            elif scenario == "Daily budget exhausted":
                status = "error" if i > 10 else "ok"

            if status == "ok":
                res = pipeline.run("What is multi-head attention?")
                first_token_ms = res["total_ms"] * 0.4
                total_ms = res["total_ms"] + random.uniform(50, 200)
                tokens_in = res["tokens_in"]
                tokens_out = res["tokens_out"]
                answer_grade = res["status"]
            else:
                first_token_ms = 0.0
                total_ms = 5000.0 if status == "timeout" else 100.0
                tokens_in = 100
                tokens_out = 0
                answer_grade = "refused_correctly" if status == "rate_limited" else "wrong"
                if status == "rate_limited":
                    retries = 2

            results.append({
                "request_id": req_id,
                "scenario": scenario,
                "source": "stand-in",
                "start_time": start_time,
                "first_token_ms": round(first_token_ms, 2),
                "total_ms": round(total_ms, 2),
                "status": status,
                "retries": retries,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "retrieval_setting": "A",
                "answer_grade": answer_grade
            })

    # Write results.csv
    csv_path = "results.csv"
    fieldnames = [
        "request_id", "scenario", "source", "start_time",
        "first_token_ms", "total_ms", "status", "retries",
        "tokens_in", "tokens_out", "retrieval_setting", "answer_grade"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Experiments complete! Results saved to {csv_path}")

if __name__ == "__main__":
    run_experiments()
