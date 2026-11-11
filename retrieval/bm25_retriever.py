import json
import os
from pathlib import Path
from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, corpus_path: str = None):
        if corpus_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            corpus_path = base_dir / "data" / "processed" / "extracted_papers.json"

        corpus_path = Path(corpus_path)
        if not corpus_path.exists():
            raise FileNotFoundError(f"Corpus not found at {corpus_path}. Run paper_downloader first.")

        with open(corpus_path, "r", encoding="utf-8") as f:
            self.docs = json.load(f)

        self.corpus_texts = [doc["paragraph_text"] for doc in self.docs]
        self.tokenized_corpus = [text.lower().split() for text in self.corpus_texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query: str, top_k: int = 3):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            doc = self.docs[idx]
            results.append({
                "passage_text": doc["paragraph_text"],
                "paper_title": doc["paper_title"],
                "paper_id": doc["paper_id"],
                "page_number": doc["page_number"],
                "section_heading": doc["section_title"],
                "chunk_id": doc["chunk_id"],
                "retrieval_score": float(scores[idx])
            })
        return results

if __name__ == "__main__":
    retriever = BM25Retriever()
    res = retriever.retrieve("Multi-Head Attention", top_k=2)
    print(json.dumps(res, indent=2))
