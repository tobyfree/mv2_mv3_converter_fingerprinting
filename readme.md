# MV2 to MV3 comparison and pattern recognition

This work is the result and supplementary source code for the owners master's thesis.

A modular, scriptable pipeline to analyze browser extension manifests. It identifies structural changes between versions (V2 ↔ V3), extracts recurring patterns, compares malicious vs general traits, and scores extensions based on pattern weightings.

---

## Features

- Compare V2 and V3 manifest changes
- Extract tokenized and raw string patterns from changes
- Compare pattern frequency in general vs malicious datasets
- Generate an HTML report of the found patterns
- Score unseen V3 extensions based on risky patterns
- Supports multiprocessing and YAML-based config

---

## Project Structure

```text
manifest-pipeline/
├── data/                     # Raw input data (V2/V3)
│   ├── large-dataset/
│   │   ├── V2/
│   │   └── V3/
│   └── malicious-dataset/
│       └── V2/
├── results/                  # All outputs (CSV, JSON, HTML)
├── config.yaml               # All pipeline settings
├── run_pipeline.py           # Master controller script
├── change_extraction.py      # Step 1: Manifest diffing
├── pattern_extraction.py     # Step 2: Pattern extraction
├── pattern_comparison.py     # Step 3: General vs malicious analysis
├── pattern_applyer.py        # Step 4: Extension scoring
├── pattern_visualisation.py  # Step 5: Report generation
```

---

## Configuration (`config.yaml`)

All paths and flags are defined in `config.yaml` — edit this file to change inputs/outputs or enable parallel processing:

```yaml
paths:
  v2_general: "data/large-dataset/V2"
  v2_malicious: "data/malicious-dataset/V2"
  v3_dir: "data/large-dataset/V3"

outputs:
  diff_csv_general: "results/manifest_differences_general.csv"
  diff_csv_malicious: "results/manifest_differences_malicious.csv"
  summary_general: "results/general_summary.json"
  summary_malicious: "results/malicious_summary.json"
  comparison_json: "results/comparison_summary.json"
  score_output_csv: "results/maliciousness_scores_large_V3.csv"
  html_report: "results/report.html"

flags:
  parallel_score: true
```

---

## Running the Pipeline

```bash
python run_pipeline.py
```

This will:

1. Compare V2 and V3 manifests (for both datasets)
2. Extract patterns from change sets
3. Compare general vs malicious traits
4. Generate an HTML report
5. Score all V3 extensions

Each step prints real-time progress and handles dependencies automatically.

---

## Requirements

Install the following packages:

- pandas
- pyyaml
- tqdm

---

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, distribute, and even sublicense the code — just keep the license file included.

---