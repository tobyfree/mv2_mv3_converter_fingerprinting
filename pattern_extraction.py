#!/usr/bin/env python3
import pandas as pd
import ast
import json
import re
import argparse
from tqdm import tqdm
from collections import defaultdict, Counter

# ========================
# Helper Functions
# ========================
def parse_cell(cell):
    if not isinstance(cell, str) or not cell.strip():
        return {}
    try:
        normalized = cell.replace('""', '"')
        return ast.literal_eval(normalized)
    except Exception:
        return {}

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    return " ".join(text.split())

def tokenize(text):
    return re.findall(r"\b[\w-]+\b", text)

# ========================
# Core Functionality
# ========================
def extract_text_patterns(
    csv_file,
    columns_to_parse,
    output_json="summary.json",
    ratio_threshold=0.01
):
    df = pd.read_csv(csv_file, header=0, sep=",", dtype=str).fillna("")
    total_extensions = len(df)

    patterns = defaultdict(lambda: {
        "token_counts": Counter(),
        "raw_values": Counter()
    })

    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Parsing {csv_file}", unit="ext"):
        for col in columns_to_parse:
            cell_value = row.get(col, "")
            parsed_dict = parse_cell(cell_value)
            if not isinstance(parsed_dict, dict):
                continue

            tokens_set = set()
            raw_set = set()

            for key, value in parsed_dict.items():
                pattern = f"{key}: {value}"
                pattern = normalize_text(pattern)
                if pattern:
                    raw_set.add(pattern)
                    tokens_set.update(tokenize(pattern))

            patterns[col]["token_counts"].update(tokens_set)
            patterns[col]["raw_values"].update(raw_set)

    summary = {}
    for col, data in patterns.items():
        token_counts = data["token_counts"]
        raw_counts = data["raw_values"]

        token_details = {
            token: {
                "count": count,
                "ratio": count / total_extensions
            }
            for token, count in token_counts.items()
            if count >= total_extensions * ratio_threshold
        }

        raw_details = {
            raw: {
                "count": count,
                "ratio": count / total_extensions
            }
            for raw, count in raw_counts.items()
            if count >= total_extensions * ratio_threshold
        }

        summary[col] = {
            "total_extensions": total_extensions,
            "token_counts": token_details,
            "raw_values": raw_details
        }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"✅ Done. Wrote summary to {output_json}")

# ========================
# Main (argparse enabled)
# ========================
def main(args=None):
    parser = argparse.ArgumentParser(description="Extract text patterns from manifest diff CSV.")
    parser.add_argument("--csv_file", help="Path to the input CSV file", default=None)
    parser.add_argument("--output_json", help="Path to the output JSON file", default=None)
    parser.add_argument("--ratio_threshold", type=float, help="Minimum pattern frequency ratio", default=0.02)
    parser.add_argument("--columns", nargs='+', help="List of columns to analyze",
                        default=["added_details", "removed_details", "modified_details_v2", "modified_details_v3"])

    parsed = parser.parse_args(args)

    if parsed.csv_file and parsed.output_json:
        extract_text_patterns(
            csv_file=parsed.csv_file,
            columns_to_parse=parsed.columns,
            output_json=parsed.output_json,
            ratio_threshold=parsed.ratio_threshold
        )
    else:
        # Default hardcoded calls if no args are provided
        extract_text_patterns(
            csv_file="manifest_differences_malicious.csv",
            columns_to_parse=parsed.columns,
            output_json="malicious_summary.json",
            ratio_threshold=parsed.ratio_threshold
        )
        extract_text_patterns(
            csv_file="manifest_differences_general.csv",
            columns_to_parse=parsed.columns,
            output_json="general_summary.json",
            ratio_threshold=parsed.ratio_threshold
        )

if __name__ == "__main__":
    main()
