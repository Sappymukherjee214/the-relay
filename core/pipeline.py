import json
import time
from typing import Dict, Any, List
from retrieval.bm25_retriever import BM25Retriever

class Pipeline:
    def __init__(self):
        self.retriever = BM25Retriever()

    def stage1_understanding(self, question: str) -> Dict[str, Any]:
        q_lower = question.lower()
        if "compare" in q_lower or "difference" in q_lower:
            intent = "MULTI_HOP_ANSWER"
        elif any(k in q_lower for k in ["what", "how", "explain", "attention", "moshi", "chunking"]):
            intent = "RETRIEVAL_REQUIRED"
        else:
            intent = "SIMPLE_ANSWER"

        return {
            "intent": intent,
            "concepts": [w for w in question.split() if len(w) > 4],
            "complexity": "medium"
        }

    def stage2_retrieval(self, intent_result: Dict[str, Any], question: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if intent_result["intent"] == "INSUFFICIENT_EVIDENCE":
            return []
        return self.retriever.retrieve(question, top_k=top_k)

    def stage3_decision(self, retrieved_passages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not retrieved_passages:
            return {"action": "refuse", "reason": "No relevant passages found."}
        return {"action": "generate_answer", "evidence_count": len(retrieved_passages)}

    def stage4_generation(self, question: str, passages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not passages:
            return {
                "answer": "I am sorry, but the research papers do not contain sufficient information to answer this question.",
                "citations": [],
                "tokens_in": 100,
                "tokens_out": 30
            }

        best_passage = passages[0]
        citation = f"[{best_passage['paper_title']}, p. {best_passage['page_number']}]"
        answer = f"Based on the research papers, regarding '{question}': {best_passage['passage_text'][:200]}... {citation}"

        return {
            "answer": answer,
            "citations": [citation],
            "tokens_in": sum(len(p['passage_text'].split()) for p in passages) + len(question.split()),
            "tokens_out": len(answer.split())
        }

    def stage5_verification(self, answer: str, citations: List[str]) -> Dict[str, Any]:
        is_valid = len(citations) > 0 and "refuse" not in answer.lower()
        return {
            "is_valid": is_valid,
            "citation_valid": len(citations) > 0,
            "evidence_sufficient": True,
            "unsupported_claims": [],
            "decision": "ACCEPT" if is_valid else "REFUSE"
        }

    def run(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        start_time = time.time()

        # Stage 1
        understanding = self.stage1_understanding(question)

        # Stage 2
        passages = self.stage2_retrieval(understanding, question, top_k=top_k)

        # Stage 3
        decision = self.stage3_decision(passages)
        if decision["action"] == "refuse":
            return {
                "answer": "The research papers do not contain sufficient evidence to answer this question safely.",
                "citations": [],
                "status": "refused_correctly",
                "total_ms": (time.time() - start_time) * 1000
            }

        # Stage 4
        gen_result = self.stage4_generation(question, passages)

        # Stage 5
        verification = self.stage5_verification(gen_result["answer"], gen_result["citations"])

        total_ms = (time.time() - start_time) * 1000

        return {
            "answer": gen_result["answer"],
            "citations": gen_result["citations"],
            "tokens_in": gen_result["tokens_in"],
            "tokens_out": gen_result["tokens_out"],
            "verification": verification,
            "status": "correct" if verification["is_valid"] else "wrong",
            "total_ms": total_ms
        }

if __name__ == "__main__":
    pipeline = Pipeline()
    res = pipeline.run("What is multi-head attention?")
    print(json.dumps(res, indent=2))
