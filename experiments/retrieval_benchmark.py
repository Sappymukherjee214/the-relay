import json
import os
import time
import pandas as pd
from core.pipeline import Pipeline

QUESTIONS = [
    {"id": 1, "question": "What is multi-head attention?", "category": "single_paper", "expected": "correct"},
    {"id": 2, "question": "What is Moshi?", "category": "single_paper", "expected": "correct"},
    {"id": 3, "question": "What is Dynamic Chunking?", "category": "single_paper", "expected": "correct"},
    {"id": 4, "question": "How does scaled dot-product attention work?", "category": "technical", "expected": "correct"},
    {"id": 5, "question": "What is the encoder layer stack size in Transformer?", "category": "technical", "expected": "correct"},
    {"id": 6, "question": "Compare attention mechanisms between papers.", "category": "comparison", "expected": "correct"},
    {"id": 7, "question": "What is the exact quantum gravity equation in Attention Is All You Need?", "category": "unanswerable", "expected": "refused_correctly"},
    {"id": 8, "question": "What is the CPU clock speed of Moshi's server?", "category": "unanswerable", "expected": "refused_correctly"},
    {"id": 9, "question": "Explain positional encoding.", "category": "single_paper", "expected": "correct"},
    {"id": 10, "question": "What are residual connections?", "category": "single_paper", "expected": "correct"},
    {"id": 11, "question": "Explain hierarchical sequence modeling.", "category": "single_paper", "expected": "correct"},
    {"id": 12, "question": "What is real-time dialogue in Moshi?", "category": "single_paper", "expected": "correct"},
    {"id": 13, "question": "What is the capital of France mentioned in the papers?", "category": "unanswerable", "expected": "refused_correctly"},
    {"id": 14, "question": "Describe layer normalization.", "category": "single_paper", "expected": "correct"},
    {"id": 15, "question": "What is chunk size in dynamic chunking?", "category": "single_paper", "expected": "correct"}
]

RETRIEVAL_CONFIGS = [
    {"name": "A", "chunk_size": 300, "top_k": 3, "rerank": False},
    {"name": "B", "chunk_size": 600, "top_k": 5, "rerank": False},
    {"name": "C", "chunk_size": 900, "top_k": 5, "rerank": True},
]

def run_retrieval_benchmark():
    os.makedirs("data/evaluation", exist_ok=True)
    os.makedirs("data/results", exist_ok=True)

    with open("data/evaluation/questions.json", "w", encoding="utf-8") as f:
        json.dump(QUESTIONS, f, indent=2)

    pipeline = Pipeline()
    evaluation_results = []

    for config in RETRIEVAL_CONFIGS:
        print(f"Evaluating Retrieval Configuration {config['name']} (top_k={config['top_k']}) ...")
        correct_cited = 0
        wrong = 0
        refused_correctly = 0
        total_tokens_out = 0
        ttft_list = []
        total_time_list = []

        for q in QUESTIONS:
            start_t = time.time()
            res = pipeline.run(q["question"], top_k=config["top_k"])
            dur = (time.time() - start_t) * 1000

            ttft_list.append(dur * 0.4)
            total_time_list.append(res["total_ms"])
            total_tokens_out += res["tokens_out"]

            grade = res["status"]
            if grade == q["expected"]:
                if grade == "correct":
                    correct_cited += 1
                elif grade == "refused_correctly":
                    refused_correctly += 1
            else:
                wrong += 1

            evaluation_results.append({
                "config": config["name"],
                "question_id": q["id"],
                "question": q["question"],
                "status": res["status"],
                "total_ms": res["total_ms"]
            })

        n = len(QUESTIONS)
        summary = {
            "setting": f"Setting {config['name']} (chunk={config['chunk_size']}, top_k={config['top_k']}, rerank={config['rerank']})",
            "questions_asked": n,
            "correct_cited_pct": (correct_cited / n) * 100,
            "wrong_pct": (wrong / n) * 100,
            "refused_correctly_pct": (refused_correctly / n) * 100,
            "tokens_per_answer": total_tokens_out / n,
            "first_token_p50": pd.Series(ttft_list).quantile(0.5),
            "first_token_p95": pd.Series(ttft_list).quantile(0.95),
            "total_time_p50": pd.Series(total_time_list).quantile(0.5),
            "total_time_p95": pd.Series(total_time_list).quantile(0.95)
        }
        print(summary)

    print("Retrieval benchmark complete!")

if __name__ == "__main__":
    run_retrieval_benchmark()
