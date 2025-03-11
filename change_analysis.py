#!/usr/bin/env python3
import pandas as pd
import ast
import json
import re
from collections import defaultdict, Counter


def parse_cell(cell):
    """
    Safely parse a CSV cell that contains JSON- or Python-like dict strings.
    Returns an empty dictionary if parsing fails.
    """
    if not isinstance(cell, str) or not cell.strip():
        return {}
    try:
        # Replace double double-quotes with single quotes (in case of CSV escape issues)
        normalized = cell.replace('""', '"')
        return ast.literal_eval(normalized)
    except Exception:
        return {}


def normalize_text(text):
    """
    Lowercase and collapse extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = " ".join(text.split())
    return text


def tokenize(text):
    """
    Simple word-level tokenization by word characters plus hyphens.
    """
    return re.findall(r"\b[\w-]+\b", text)


def extract_text_patterns(
        csv_file,
        columns_to_parse,
        output_json="summary.json",
        ratio_threshold=0.01
):
    """
    1) For each row in the CSV, parse the specified columns (which contain dict-like strings)
       and for each cell, compute the set of unique tokens and raw values.
    2) Count (per column) in how many extensions (rows) a given token/raw value appears.
    3) Compute ratio = (number of extensions containing the token) / (total extensions).
    4) Only include tokens/raw values that appear in at least 'ratio_threshold' of extensions.
    5) Save the result as JSON.

    :param csv_file: Path to the CSV file.
    :param columns_to_parse: List of columns to parse.
    :param output_json: Path for the JSON output.
    :param ratio_threshold: Minimum ratio (as fraction of total extensions) a pattern must have.
    """
    df = pd.read_csv(csv_file, header=0, sep=",", dtype=str).fillna("")
    total_extensions = len(df)

    # Store extension-level presence for tokens and raw values for each column.
    patterns = defaultdict(lambda: {
        "token_counts": Counter(),
        "raw_values": Counter()
    })

    # Process each row (each extension)
    for _, row in df.iterrows():
        for col in columns_to_parse:
            cell_value = row.get(col, "")
            parsed_dict = parse_cell(cell_value)
            if not isinstance(parsed_dict, dict):
                continue

            # Build sets to count each token and raw value only once per extension.
            tokens_set = set()
            raw_set = set()

            for _, value in parsed_dict.items():
                val_str = normalize_text(str(value))
                if val_str:
                    raw_set.add(val_str)
                    tokens_set.update(tokenize(val_str))

            # Update counters for this column with the set of tokens/raw values for this extension.
            patterns[col]["token_counts"].update(tokens_set)
            patterns[col]["raw_values"].update(raw_set)

    # Build the summary with ratios relative to the total number of extensions.
    summary = {}
    for col, data in patterns.items():
        token_counts = data["token_counts"]
        raw_counts = data["raw_values"]

        token_details = {}
        for token, count in token_counts.items():
            if count < total_extensions * ratio_threshold:
                continue
            ratio = count / total_extensions
            token_details[token] = {
                "count": count,
                "ratio": ratio
            }

        raw_details = {}
        for raw, count in raw_counts.items():
            if count < total_extensions * ratio_threshold:
                continue
            ratio = count / total_extensions
            raw_details[raw] = {
                "count": count,
                "ratio": ratio
            }

        summary[col] = {
            "total_extensions": total_extensions,
            "token_counts": token_details,
            "raw_values": raw_details
        }

    # Write the summary to JSON.
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"Done. Wrote summary to {output_json}")


def main():
    # Example usage: process two CSV files (malicious and general)
    columns_to_parse = ["added_details", "removed_details", "modified_details_v2", "modified_details_v3"]

    # 1) Malicious dataset
    extract_text_patterns(
        csv_file="manifest_differences_malicious.csv",
        columns_to_parse=columns_to_parse,
        output_json="malicious_summary.json",
        ratio_threshold=0.01
    )

    # 2) General dataset
    extract_text_patterns(
        csv_file="manifest_differences_general.csv",
        columns_to_parse=columns_to_parse,
        output_json="general_summary.json",
        ratio_threshold=0.01
    )


if __name__ == "__main__":
    main()
