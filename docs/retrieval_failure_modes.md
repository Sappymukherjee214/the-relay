# Retrieval Failure Modes

## 1. Technical Terminology Overlap

- **Failure Mode**: Terms like "attention" appear across multiple papers with different underlying neural architectures (self-attention vs. recurrent audio-text modeling in Moshi).
- **Mitigation**: Stage 1 request understanding combined with paper-specific section filtering.

## 2. Distributed Information across Distant Sections

- **Failure Mode**: Encoder/decoder stack specifications in Attention Is All You Need are separated across Section 3.1 and tables in Section 5.
- **Mitigation**: Top-K retrieval expansion and multi-chunk assembly.

## 3. Unsupported Cross-Paper Assumptions

- **Failure Mode**: Assuming dynamic chunking applies directly to speech token streams in Moshi without explicit evidence.
- **Mitigation**: Strict stage 5 citation verification and safe refusal behavior.
