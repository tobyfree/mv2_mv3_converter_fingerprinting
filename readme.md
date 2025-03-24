![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

# MV2 to MV3 comparison and pattern recognition

This work is the result and supplementary source code for the owners master's thesis.

A modular, scriptable pipeline to analyze browser extension manifests converter (EMC) from manifest version 2 to manifest version 3 by the extension manifest converter by GoogleChromeLabs https://github.com/GoogleChromeLabs/extension-manifest-converter. 

It identifies structural changes between versions (V2 ↔ V3), extracts recurring patterns, compares malicious vs general traits, and scores extensions based on pattern weightings.

---

## Prerequisites

The extensions in the datasets need to be extracted and in folder structure, ideally named uniquely. We recommend using the extension-id.

All extensions have to be sorted by manifest.json version. Into V2 and V3 folders. All V2 extensions have to be present in a V3 variant in a subfolder called "converted" as can be seen by the Folder Structure.

---

## Quickstart

```bash
git clone https://github.com/tobyfree/mv2_mv3_converter_fingerprinting.git
cd manifest-pipeline
pip install -r requirements.txt
cp config.yaml config.local.yaml  # optional, if using a template
python run_pipeline.py --config config.yaml
```

---

## Features

- Compare V2 and V3 manifest changes
- Extract tokenized and raw string patterns from changes
- Compare pattern frequency in general vs malicious datasets
- Generate an HTML report of the found patterns
- Score unseen V3 extensions based on risky patterns
- Supports multiprocessing and YAML-based config
- Each script is executable individually if the whole pipeline is not necessary

---

## Folder Structure

```text
manifest-pipeline/
├── data/                     # Raw input data (V2/V3)
│   ├── large-dataset/
│   │   ├── V2/               # Original V2 used as "benign" baseline
│   │   │   └── converted/    # Converted from V2 to V3 by EMC
│   │   └── V3/               # Original V3 to be scored and used for MV3 only analysis
│   └── malicious-dataset/
│       ├── V2/               # Original V2 used as "malicious" baseline
│       │    └── converted/   # Converted from V2 to V3 by EMC
│       └── V3/               # Original V3 to be used for MV3 only analysis
├── results/                  # All outputs (CSV, JSON, HTML)
├── config.yaml               # All pipeline settings
├── run_pipeline.py           # Master controller script
├── change_extraction.py      # Step 1: Manifest diffing
├── pattern_extraction.py     # Step 2: Pattern extraction
├── pattern_comparison.py     # Step 3: General vs malicious analysis
├── pattern_applyer.py        # Step 4: Extension scoring
└── pattern_visualisation.py  # Step 5: Report generation
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
python run_pipeline.py --config config.yaml
```

This will:

1. Compare V2 and V3 manifests (for both datasets)
2. Extract patterns from change sets
3. Compare general vs malicious traits
4. Generate an HTML report
5. Score all V3 extensions

Each step prints real-time progress and handles dependencies automatically.

---

## Alternative Pipeline: MV3-Only Comparison

This variation of the pipeline skips Manifest V2 entirely and analyzes the structure of MV3 extensions only.

### Goal

- Compare general vs malicious MV3 manifests directly
- Extract discriminative patterns
- Score unknown MV3 extensions for malicious confidence

### Running the MV3-Only Pipeline

```bash
python run_pipeline_mv3_only.py --config config_mv3.yaml
```
Edit `config_mv3.yaml` to update input/output paths and thresholds.

###  MV3 Config Structure (`config_mv3.yaml`)

```yaml
paths:
  v3_general: "data/large-dataset/V3"
  v3_malicious: "data/malicious-dataset/V3"
  v3_dir_to_score: "data/large-dataset/V3"

outputs:
  summary_general: "results/general_summary_mv3.json"
  summary_malicious: "results/malicious_summary_mv3.json"
  comparison_json: "results/comparison_summary_mv3.json"
  score_output_csv: "results/maliciousness_scores_mv3.csv"
  html_report: "results/report_mv3.html"

flags:
  parallel_score: false

parameters:
  ratio_threshold: 0.02
```
  
## Requirements

Install the following packages:

- pandas
- pyyaml
- tqdm

Recommended:

```bash
pip install -r requirements.txt
```

---
## Supplementary code

Code within the supplementary tools are used in creating datasets that are already meant to be done before this script.

---

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, distribute, and even sublicense the code — just keep the license file included.

---
