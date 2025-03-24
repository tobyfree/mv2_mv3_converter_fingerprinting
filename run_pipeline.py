#!/usr/bin/env python3
import subprocess
import sys
import os
import yaml

def run_script(command, step_name):
    print(f"\n🔄 {step_name}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Step failed: {step_name}")
        sys.exit(result.returncode)
    print(f"✅ Done: {step_name}")

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        print(f"❌ Config file not found: {path}")
        sys.exit(1)
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    validate_config(config)

    v2_general = config["paths"]["v2_general"]
    v2_malicious = config["paths"]["v2_malicious"]
    v3_dir = config["paths"]["v3_dir"]

    diff_csv_general = config["outputs"]["diff_csv_general"]
    diff_csv_malicious = config["outputs"]["diff_csv_malicious"]
    summary_general = config["outputs"]["summary_general"]
    summary_malicious = config["outputs"]["summary_malicious"]
    comparison_json = config["outputs"]["comparison_json"]
    score_output_csv = config["outputs"]["score_output_csv"]
    html_report = config["outputs"]["html_report"]

    parallel_score = config.get("flags", {}).get("parallel_score", False)

    # Step 1a: Compare Manifests (General)
    run_script(
        f"python change_extraction.py "
        f"--input_dir \"{v2_general}\" "
        f"--output_csv \"{diff_csv_general}\"",
        "Step 1a: Compare Manifests (General)"
    )

    # Step 1b: Compare Manifests (Malicious)
    run_script(
        f"python change_extraction.py "
        f"--input_dir \"{v2_malicious}\" "
        f"--output_csv \"{diff_csv_malicious}\"",
        "Step 1b: Compare Manifests (Malicious)"
    )

    # Step 2a: Extract Patterns (General)
    run_script(
        f"python pattern_extraction.py "
        f"--csv_file \"{diff_csv_general}\" "
        f"--output_json \"{summary_general}\"",
        "Step 2a: Extract Patterns (General)"
    )

    # Step 2b: Extract Patterns (Malicious)
    if os.path.exists(diff_csv_malicious):
        run_script(
            f"python pattern_extraction.py "
            f"--csv_file \"{diff_csv_malicious}\" "
            f"--output_json \"{summary_malicious}\"",
            "Step 2b: Extract Patterns (Malicious)"
        )
    else:
        print(f"⚠️ Skipping malicious extraction — file not found: {diff_csv_malicious}")
        return

    # Step 3: Compare Pattern Summaries
    run_script(
        f"python pattern_comparison.py "
        f"--general_json \"{summary_general}\" "
        f"--malicious_json \"{summary_malicious}\" "
        f"--output \"{comparison_json}\"",
        "Step 3: Compare Pattern Summaries"
    )

    # Step 4: Score V3 Extensions
    run_script(
        f"python pattern_applyer.py "
        f"--comparison_json \"{comparison_json}\" "
        f"--extensions_folder \"{v3_dir}\" "
        f"--output_csv \"{score_output_csv}\"",
        "Step 4: Score Extensions (Parallel)" if parallel_score else "Step 4: Score Extensions"
    )

    # Step 5: Generate HTML Report
    run_script(
        f"python pattern_visualisation.py "
        f"--input_json \"{comparison_json}\" "
        f"--output_html \"{html_report}\"",
        "Step 5: Generate HTML Report"
    )

    print("\n🎉 All done! Full pipeline completed successfully.")

def validate_config(cfg):
    required = {
        "paths": ["v2_general", "v2_malicious", "v3_dir"],
        "outputs": [
            "diff_csv_general", "diff_csv_malicious",
            "summary_general", "summary_malicious",
            "comparison_json", "score_output_csv", "html_report"
        ],
        "flags": ["parallel_score"]
    }

    for section, keys in required.items():
        if section not in cfg:
            raise ValueError(f"Missing section in config: {section}")
        for key in keys:
            if key not in cfg[section]:
                raise ValueError(f"Missing config key: {section}.{key}")

    # Optional: type checking
    if not isinstance(cfg["flags"]["parallel_score"], bool):
        raise TypeError("flags.parallel_score must be a boolean")

if __name__ == "__main__":
    main()
