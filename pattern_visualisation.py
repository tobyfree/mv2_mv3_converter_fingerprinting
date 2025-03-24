#!/usr/bin/env python3
import json
import argparse
from pathlib import Path

import yaml
from tqdm import tqdm

# ========================
# Helper Functions
# ========================
def load_comparison(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_html_table(section_data, section_name):
    html_content = f"<h2>{section_name.replace('_', ' ').title()}</h2>\n"
    for col in tqdm(sorted(section_data.keys()), desc=f"Generating {section_name}", unit="col"):
        html_content += f"<h3>Column: {col}</h3>\n"
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>Pattern</th>
                    <th>General Ratio</th>
                    <th>Malicious Ratio</th>
                    <th>Absolute Diff</th>
                    <th>Relative Diff</th>
                </tr>
            </thead>
            <tbody>
        """
        sorted_items = sorted(
            section_data[col].items(),
            key=lambda kv: (-kv[1].get("relative_diff", 0), -kv[1].get("absolute_diff", 0))
        )
        for token, stats in sorted_items:
            html_content += "<tr>"
            html_content += f"<td>{token}</td>"
            html_content += f"<td>{stats.get('general_ratio', 0):.4f}</td>"
            html_content += f"<td>{stats.get('malicious_ratio', 0):.4f}</td>"
            html_content += f"<td>{stats.get('absolute_diff', 0):.4f}</td>"
            html_content += f"<td>{stats.get('relative_diff', 0):.4f}</td>"
            html_content += "</tr>\n"
        html_content += """
            </tbody>
        </table>
        <br/>
        """
    return html_content

def generate_report(json_file, output_html="report.html"):
    data = load_comparison(json_file)
    token_section = data.get("token_comparison", {})
    raw_section = data.get("raw_value_comparison", {})

    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Comparison Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2, h3 { color: #333; }
        table { border-collapse: collapse; margin-bottom: 20px; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #eee; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Comparison Report</h1>
    <p>This report compares the patterns found in the general dataset with those in the malicious dataset. The tables show, per column, the ratio in the general dataset, the ratio in the malicious dataset, their absolute difference, and their relative difference (i.e. the difference as a proportion of the larger ratio).</p>
    """

    html += generate_html_table(token_section, "token_comparison")
    html += generate_html_table(raw_section, "raw_value_comparison")
    html += "\n</body>\n</html>"

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Report generated: {output_html}")

# ========================
# Main Function (argparse)
# ========================
def main(args=None):
    parser = argparse.ArgumentParser(description="Generate an HTML report from comparison summary JSON.")
    parser.add_argument("--input_json", help="Input comparison JSON file")
    parser.add_argument("--output_html", help="Output HTML report path")
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

    # Resolve inputs: CLI args > config values
    input_json = parsed.input_json or config.get("outputs", {}).get("comparison_json")
    output_html = parsed.output_html or config.get("outputs", {}).get("html_report")

    # Final check
    if not input_json or not output_html:
        parser.error("You must provide --input_json and --output_html, or use --config with those set.")

    # Run report generation
    generate_report(input_json, output_html)

if __name__ == "__main__":
    main()
