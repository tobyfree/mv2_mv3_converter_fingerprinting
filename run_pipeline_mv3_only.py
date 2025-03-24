#!/usr/bin/env python3
import subprocess
import yaml
import sys
import os

def run(command, name):
    print(f"\n🔄 {name}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {name}")
        sys.exit(result.returncode)
    print(f"✅ Done: {name}")

def load_config(path="config_mv3.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    validate_config(config, pipeline="mv3")

    v3_general = config["paths"]["v3_general"]
    v3_malicious = config["paths"]["v3_malicious"]
    v3_dir_to_score = config["paths"]["v3_dir_to_score"]

    summary_general = config["outputs"]["summary_general"]
    summary_malicious = config["outputs"]["summary_malicious"]
    comparison_json = config["outputs"]["comparison_json"]
    score_output_csv = config["outputs"]["score_output_csv"]
    html_report = config["outputs"]["html_report"]

    ratio_threshold = config["parameters"].get("ratio_threshold", 0.02)

    # Step 1a: Extract patterns from general MV3 dataset
    run(
        f"python pattern_extraction_mv3.py "
        f"--extensions_folder \"{v3_general}\" "
        f"--output_json \"{summary_general}\" "
        f"--ratio_threshold {ratio_threshold}",
        "Step 1a: Pattern Extraction (General)"
    )

    # Step 1b: Extract patterns from malicious MV3 dataset
    run(
        f"python pattern_extraction_mv3.py "
        f"--extensions_folder \"{v3_malicious}\" "
        f"--output_json \"{summary_malicious}\" "
        f"--ratio_threshold {ratio_threshold}",
        "Step 1b: Pattern Extraction (Malicious)"
    )

    # Step 2: Compare summaries
    run(
        f"python pattern_comparison.py "
        f"--general_json \"{summary_general}\" "
        f"--malicious_json \"{summary_malicious}\" "
        f"--output \"{comparison_json}\"",
        "Step 2: Compare Summaries"
    )

    # Step 3: Score general MV3 dataset
    run(
        f"python pattern_applyer.py "
        f"--comparison_json \"{comparison_json}\" "
        f"--extensions_folder \"{v3_dir_to_score}\" "
        f"--output_csv \"{score_output_csv}\"",
        "Step 3: Score General MV3 Dataset"
    )

    # Step 4: Generate report
    run(
        f"python pattern_visualisation.py "
        f"--input_json \"{comparison_json}\" "
        f"--output_html \"{html_report}\"",
        "Step 4: Generate HTML Report"
    )

    print("\n🎉 MV3-only pipeline completed successfully.")

def validate_config(config, pipeline="mv3"):
    required = {
        "paths": ["v3_general", "v3_malicious", "v3_dir_to_score"] if pipeline == "mv3" else ["v2_general", "v2_malicious", "v3_dir_to_score"],
        "outputs": [
            "summary_general", "summary_malicious",
            "comparison_json", "score_output_csv", "html_report"
        ],
        "flags": ["parallel_score"],
        "parameters": ["ratio_threshold"]
    }

    for section, keys in required.items():
        if section not in config:
            raise ValueError(f"Missing section in config: {section}")
        for key in keys:
            if key not in config[section]:
                raise ValueError(f"Missing key in config: {section}.{key}")

    if not isinstance(config["flags"]["parallel_score"], bool):
        raise TypeError("flags.parallel_score must be a boolean")
    if not isinstance(config["parameters"]["ratio_threshold"], float) and not isinstance(config["parameters"]["ratio_threshold"], int):
        raise TypeError("parameters.ratio_threshold must be a float or int")

if __name__ == "__main__":
    main()
