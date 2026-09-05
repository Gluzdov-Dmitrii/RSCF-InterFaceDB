# Search runs

Each subdirectory represents one immutable search run and should contain:

- `run.json`: platform, endpoint, exact query, filters, UTC time, operator, code/prompt version and counts;
- `results.jsonl` or the platform's raw export;
- `sha256.txt` or hashes embedded in `run.json`;
- `errors.jsonl` when retrieval or parsing is incomplete.

Raw results are ignored by Git because they can be large and change frequently. Curated source metadata and screening decisions belong in `literature/metadata/` and `literature/screening/`.
