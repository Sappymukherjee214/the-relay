import hashlib
import json
import os
import urllib.request
import fitz  # PyMuPDF

PAPERS = [
    {
        "id": "attention",
        "title": "Attention Is All You Need",
        "arxiv_id": "1706.03762",
        "version": "v7",
        "url": "https://arxiv.org/pdf/1706.03762v7",
        "filename": "attention_is_all_you_need_v7.pdf",
    },
    {
        "id": "moshi",
        "title": "Moshi: a speech-text foundation model for real-time dialogue",
        "arxiv_id": "2410.00037",
        "version": "v1",
        "url": "https://arxiv.org/pdf/2410.00037v1",
        "filename": "moshi_v1.pdf",
    },
    {
        "id": "dynamic_chunking",
        "title": "Dynamic Chunking for End-to-End Hierarchical Sequence Modeling",
        "arxiv_id": "2507.07955",
        "version": "v2",
        "url": "https://arxiv.org/pdf/2507.07955v2",
        "filename": "dynamic_chunking_v2.pdf",
    },
]


def download_and_process():
    os.makedirs("data/papers", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    extracted_docs = []

    for paper in PAPERS:
        pdf_path = os.path.join("data/papers", paper["filename"])
        print(f"Downloading {paper['title']} from {paper['url']}...")

        req = urllib.request.Request(
            paper["url"],
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )

        with urllib.request.urlopen(req) as response, open(pdf_path, "wb") as out_file:
            content = response.read()
            out_file.write(content)

        sha256_hash = hashlib.sha256(content).hexdigest()
        paper["sha256"] = sha256_hash
        print(f"Saved {pdf_path} (SHA-256: {sha256_hash})")

        # Extract text using PyMuPDF
        doc = fitz.open(pdf_path)
        chunk_counter = 0
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

            for para in paragraphs:
                chunk_counter += 1
                chunk_id = f"{paper['id']}_p{page_num}_c{chunk_counter}"

                section_title = "General"
                lines = para.split("\n")
                if (
                    len(lines[0]) < 80
                    and (lines[0].isupper() or lines[0].istitle())
                    and not lines[0].endswith(".")
                ):
                    section_title = lines[0]
                    para_text = "\n".join(lines[1:]) if len(lines) > 1 else lines[0]
                else:
                    para_text = para

                if not para_text.strip():
                    continue

                extracted_docs.append(
                    {
                        "paper_id": paper["id"],
                        "paper_title": paper["title"],
                        "arxiv_id": paper["arxiv_id"],
                        "version": paper["version"],
                        "page_number": page_num,
                        "section_title": section_title,
                        "paragraph_text": para_text.strip(),
                        "chunk_id": chunk_id,
                    }
                )
        print(f"Extracted chunks for {paper['title']} ({len(doc)} pages).")

    output_path = "data/processed/extracted_papers.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_docs, f, indent=2, ensure_ascii=False)

    metadata_path = "data/processed/papers_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(PAPERS, f, indent=2, ensure_ascii=False)

    print(f"Extraction complete! Saved to {output_path}")


if __name__ == "__main__":
    download_and_process()
