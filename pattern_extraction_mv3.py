#!/usr/bin/env python3
import os
import json
import argparse
import yaml
import re
from collections import defaultdict, Counter
from tqdm import tqdm

def flatten_manifest(d, parent_key="", sep="."):
    items = {}
    key_mapping = {
        "browser_action": "action",
        "page_action": "action",
        "background.scripts": "background.service_worker"
    }
    for k, v in d.items():
        k = key_mapping.get(k, k)
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_manifest(v, new_key, sep=sep))
        elif isinstance(v, list):
            new_list = []
            for elem in v:
                if isinstance(elem, dict):
                    flat_elem = flatten_manifest(elem)
                    sorted_items = sorted(flat_elem.items())
                    joined = ", ".join([f"{key}: {value}" for key, value in sorted_items])
                    new_list.append(joined)
                else:
                    new_list.append(str(elem).lower().strip())
            items[new_key] = new_list
        else:
            items[new_key] = str(v).lower().strip()
    return items

def tokenize(text):
    return re.findall(r"\b[\w-]+\b", text)

def extract_patterns_from_folder(folder, ratio_threshold=0.02):
    extensions = [ext for ext in os.listdir(folder) if os.path.isdir(os.path.join(folder, ext))]
    total = len(extensions)

    patterns = defaultdict(lambda: {
        "token_counts": Counter(),
        "raw_values": Counter()
    })

    for ext_id in tqdm(extensions, desc="Processing extensions"):
        manifest_path = os.path.join(folder, ext_id, "manifest.json")
        if not os.path.exists(manifest_path):
            continue
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading {manifest_path}: {e}")
            continue

        flat = flatten_manifest(manifest)
        token_set = set()
        raw_set = set()

        for key, value in flat.items():
            if isinstance(value, list):
                for v in value:
                    pattern = f"{key}: {v}".lower().strip()
                    raw_set.add(pattern)
                    token_set.update(tokenize(pattern))
            else:
                pattern = value.lower().strip()
                raw_set.add(pattern)
                token_set.update(tokenize(pattern))

        patterns["manifest"]["token_counts"].update(token_set)
        patterns["manifest"]["raw_values"].update(raw_set)

    result = {}
    for section, counts in patterns.items():
        result[section] = {
            "total_extensions": total,
            "token_counts": {},
            "raw_values": {}
        }

        for token, count in counts["token_counts"].items():
            if count / total >= ratio_threshold:
                result[section]["token_counts"][token] = {
                    "count": count,
                    "ratio": count / total
                }

        for raw, count in counts["raw_values"].items():
            if count / total >= ratio_threshold:
                result[section]["raw_values"][raw] = {
                    "count": count,
                    "ratio": count / total
                }

    return result

def main(args=None):
    parser = argparse.ArgumentParser(description="Extract patterns directly from MV3 manifests.")
    parser.add_argument("--extensions_folder", help="Path to extension folders")
    parser.add_argument("--output_json", help="Output file for pattern summary")
    parser.add_argument("--ratio_threshold", type=float)
    parser.add_argument("--config", help="Optional config file")
    parsed = parser.parse_args(args)

    config = {}
    if parsed.config:
        with open(parsed.config, "r") as f:
            config = yaml.safe_load(f)

    folder = parsed.extensions_folder or config.get("paths", {}).get("v3_dir")
    output = parsed.output_json or "summary_mv3.json"
    ratio = parsed.ratio_threshold or config.get("parameters", {}).get("ratio_threshold", 0.02)

    if not folder or not output:
        parser.error("Missing --extensions_folder or --output_json. Or set them in config.")

    result = extract_patterns_from_folder(folder, ratio_threshold=ratio)

    if not result["manifest"]["token_counts"]:
        print("⚠️ No valid patterns found — check if manifests are present and parsable.")

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    print(f"✅ Pattern summary written to {output}")

if __name__ == "__main__":
    main()