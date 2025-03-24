#!/usr/bin/env python3
import os
import json
import csv
import re
from pathlib import Path

import yaml
from tqdm import tqdm
import argparse
from collections import Counter

# ========================
# Flattening & Tokenizing
# ========================
def flatten_manifest(manifest, parent_key="", sep="."):
    items = {}
    key_mapping = {
        "browser_action": "action",
        "page_action": "action",
        "background.scripts": "background.service_worker"
    }
    for k, v in manifest.items():
        k = key_mapping.get(k, k)
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_manifest(v, new_key, sep=sep))
        elif isinstance(v, list):
            patterns = [f"{new_key}: {str(elem).lower().strip()}" for elem in v]
            items[new_key] = patterns
        else:
            items[new_key] = f"{new_key}: {str(v).lower().strip()}"
    return items

def tokenize(text):
    return re.findall(r"\b[\w-]+\b", text)

# ========================
# Load Pattern Weights
# ========================
def load_pattern_scores(comparison_json_file):
    with open(comparison_json_file, "r", encoding="utf-8") as f:
        comp_data = json.load(f)

    pattern_weights = {}
    for section in ["token_comparison", "raw_value_comparison"]:
        section_data = comp_data.get(section, {})
        for col, patterns in section_data.items():
            for pat, stats in patterns.items():
                gen_ratio = stats.get("general_ratio", 0.0)
                mal_ratio = stats.get("malicious_ratio", 0.0)
                abs_diff = stats.get("absolute_diff", 0.0)
                rel_diff = stats.get("relative_diff", 0.0)
                if mal_ratio > gen_ratio:
                    weight = abs_diff * rel_diff
                    pattern_weights[pat] = pattern_weights.get(pat, 0) + weight
    return pattern_weights

# ========================
# Scoring
# ========================
def score_manifest(manifest_file, pattern_weights):
    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"Error loading manifest {manifest_file}: {e}")
        return None

    flat = flatten_manifest(manifest)
    patterns_in_manifest = set()
    for value in flat.values():
        if isinstance(value, list):
            patterns_in_manifest.update(value)
        else:
            patterns_in_manifest.add(value)

    score = sum(weight for pat, weight in pattern_weights.items() if pat in patterns_in_manifest)
    return score

# ========================
# Folder Processing
# ========================
def process_extensions_folder(extensions_folder, pattern_weights, output_csv):
    results = []
    for ext_name in tqdm(os.listdir(extensions_folder), desc="Scoring extensions", unit="ext"):
        ext_path = os.path.join(extensions_folder, ext_name)
        if os.path.isdir(ext_path):
            manifest_path = os.path.join(ext_path, "manifest.json")
            if os.path.exists(manifest_path):
                confidence = score_manifest(manifest_path, pattern_weights)
                if confidence is not None:
                    results.append({
                        "extension_id": ext_name,
                        "malicious_confidence": round(confidence, 4)
                    })
            else:
                print(f"Manifest not found for extension: {ext_name}")

    fieldnames = ["extension_id", "malicious_confidence"]
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Results written to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

# ========================
# Main with argparse
# ========================


def main(args=None):
    parser = argparse.ArgumentParser(description="Score extensions for malicious confidence.")
    parser.add_argument("--comparison_json", help="Path to comparison summary JSON")
    parser.add_argument("--extensions_folder", help="Path to folder of extension subfolders")
    parser.add_argument("--output_csv", help="Output CSV path")
    parser.add_argument("--config", help="Optional path to config.yaml")
    parsed = parser.parse_args(args)

    # Load config if provided
    config = {}
    if parsed.config:
        config_path = Path(parsed.config)
        if not config_path.exists():
            parser.error(f"Config file not found: {parsed.config}")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    # Use CLI args if provided, otherwise fallback to config
    comparison_json = parsed.comparison_json or config.get("outputs", {}).get("comparison_json")
    extensions_folder = parsed.extensions_folder or config.get("paths", {}).get("v3_dir")
    output_csv = parsed.output_csv or config.get("outputs", {}).get("score_output_csv")

    # Final validation
    if not comparison_json or not extensions_folder or not output_csv:
        parser.error("You must provide --comparison_json, --extensions_folder, and --output_csv (or use --config with those set)")

    # Run pipeline logic
    pattern_weights = load_pattern_scores(comparison_json)
    if not pattern_weights:
        print("❌ No pattern weights loaded. Check the comparison JSON file.")
        return

    process_extensions_folder(extensions_folder, pattern_weights, output_csv)


if __name__ == "__main__":
    main()
