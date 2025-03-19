#!/usr/bin/env python3
import os
import csv
import json
import re
import sys
from collections import Counter


#########################
# Flattening & Tokenizing
#########################

def flatten_manifest(manifest, parent_key="", sep="."):
    """
    Recursively flatten the manifest dictionary.
    Instead of joining list elements into one string, each element in a list
    is processed separately as its own pattern (i.e. key: value1 and key: value2).
    Returns a dict where keys with list values will map to a list of pattern strings,
    and other keys map to a single pattern string.
    """
    items = {}
    # Optionally, you can add key mappings here, e.g.:
    key_mapping = {
        "browser_action": "action",
        "background.scripts": "background.service_worker"
    }
    for k, v in manifest.items():
        # Apply mapping if defined
        k = key_mapping.get(k, k)
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_manifest(v, new_key, sep=sep))
        elif isinstance(v, list):
            # Instead of joining, keep each element as a separate pattern.
            patterns = []
            for elem in v:
                elem_str = str(elem).lower().strip()
                patterns.append(f"{new_key}: {elem_str}")
            items[new_key] = patterns  # store list of patterns
        else:
            items[new_key] = f"{new_key}: {str(v).lower().strip()}"
    return items


def tokenize(text):
    """
    Tokenize text using word characters and hyphens.
    """
    return re.findall(r"\b[\w-]+\b", text)


#########################
# Load Pattern Weights
#########################

def load_pattern_scores(comparison_json_file):
    """
    Load the comparison summary JSON and compute a weight for each pattern.
    Here we combine information from both token and raw comparisons.
    For each pattern, if malicious_ratio > general_ratio, assign:
         weight = (malicious_ratio - general_ratio) * relative_diff
    Returns a dictionary mapping pattern strings to weights.
    """
    with open(comparison_json_file, "r", encoding="utf-8") as f:
        comp_data = json.load(f)

    pattern_weights = {}

    for section in ["token_comparison", "raw_value_comparison"]:
        section_data = comp_data.get(section, {})
        for col, patterns in section_data.items():
            for pat, stats in patterns.items():
                gen_ratio = stats.get("general_ratio", 0.0)
                mal_ratio = stats.get("malicious_ratio", 0.0)
                rel_diff = stats.get("relative_diff", 0.0)
                if mal_ratio > gen_ratio:
                    weight = (mal_ratio - gen_ratio) * rel_diff
                    # If the same pattern appears from different columns/sections, sum its weight.
                    pattern_weights[pat] = pattern_weights.get(pat, 0) + weight
    return pattern_weights


#########################
# Scoring Function
#########################

def score_manifest(manifest_file, pattern_weights):
    """
    Score a single extension's manifest for maliciousness.
    Loads the manifest, flattens it (creating a set of pattern strings),
    then sums the weights for patterns that occur.
    Returns a confidence score between 0 and 1.
    """
    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"Error loading manifest {manifest_file}: {e}")
        return None

    flat = flatten_manifest(manifest)
    # Build a set of patterns found in the manifest.
    patterns_in_manifest = set()
    for key, value in flat.items():
        if isinstance(value, list):
            for pattern in value:
                patterns_in_manifest.add(pattern)
        else:
            patterns_in_manifest.add(value)

    # Sum up weights of patterns that appear.
    score = 0.0
    for pat, weight in pattern_weights.items():
        if pat in patterns_in_manifest:
            score += weight

    # Normalize by total possible weight (the sum of all pattern weights)
    total_possible = sum(pattern_weights.values())
    confidence = score / total_possible if total_possible > 0 else 0.0
    return confidence


#########################
# Processing Folder of Extensions
#########################

def process_extensions_folder(extensions_folder, pattern_weights, output_csv):
    """
    Iterates through all folders in the given directory.
    For each folder that contains a manifest.json file, computes the maliciousness score.
    The results (extension id and confidence score) are written to a CSV file.
    """
    results = []
    for ext_name in os.listdir(extensions_folder):
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

    # Write results to CSV.
    fieldnames = ["extension_id", "malicious_confidence"]
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print(f"Results written to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")


#########################
# Main Function
#########################

def main():
    # You can modify these paths as needed.
    # Path to your comparison summary JSON (from previous analysis).
    comparison_json_file = "comparison_summary.json"
    # Folder that contains extension folders (each with a manifest.json)
    if len(sys.argv) >= 2:
        extensions_folder = sys.argv[1]
    else:
        extensions_folder = "D:\\extensions\\large-dataset\\V3"  # update default as needed

    # Output CSV file to write results.
    output_csv = "maliciousness_scores_large_v3.csv" if len(sys.argv) < 3 else sys.argv[2]

    # Load the pattern weights.
    pattern_weights = load_pattern_scores(comparison_json_file)
    if not pattern_weights:
        print("No pattern weights loaded; check your comparison JSON file.")
        return

    # Process all extension folders.
    process_extensions_folder(extensions_folder, pattern_weights, output_csv)


if __name__ == "__main__":
    main()
