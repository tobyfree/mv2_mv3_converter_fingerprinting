import os
import json
import re

import pandas as pd

#change directory depending on own structure
data_folder = "D:\\extensions\\combined"

extensions_data = []
listdir = os.listdir(data_folder)

def read_json_file(filepath):
    encodings= ["utf-8", "utf-8-sig", "latin-1"]
    for encoding in encodings:
        try:
            with open(filepath, "r", encoding=encoding) as file:
                json_content = file.read().strip()

            if not json_content:
                return "empty", "empty"

            comments = re.findall(r"^\s*//.$", json_content, flags=re.MULTILINE)
            cleaned_json_str = re.sub(r"^\s*//.$", "", json_content, flags=re.MULTILINE)
            cleaned_json = json.loads(cleaned_json_str), "; ".join(comments)
            return cleaned_json

        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            continue
    print(f"Failed to read {filepath} with available encodings")
    return None

for extensions_id in listdir:
    extension_path = os.path.join(data_folder, extensions_id)
    manifest_path = os.path.join(extension_path, "manifest.json")

    if not os.path.isdir(extension_path):
        print(f"Extensionpath not found: {extension_path}")
        continue

    if not os.path.isfile(manifest_path):
        print(f"Manifestpath not found: {manifest_path}")
        continue

    try:
        manifest, comments = read_json_file(manifest_path)
        if manifest == "empty":
            extensions_data.append({
                "Extension ID": extensions_id,
                "Name": "empty",
                "Description": "empty",
                "Manifest_Version": "empty",
                "Version": "empty",
                "Permissions": "empty",
                "Host Permissions": "empty",
                "Background Scripts": "empty",
                "Content Scripts": "empty",
                "WARs": "empty",
                "Comments": "empty",
                "Browser Actions": "empty"
            })

        elif isinstance(manifest, dict):
            print(f"Reading {extensions_id}")
            name = manifest.get("name", "Unknown")
            manifest_version = manifest.get("manifest_version", "Unknown")
            version = manifest.get("version", "Unknown")
            description = manifest.get("description", "No description")
            background_script = manifest.get("background", "No background")
            content_scripts = manifest.get("content_scripts", "No content scripts")
            wars = manifest.get("web_accessible_resources", "No WARs")
            permissions = manifest.get("permissions", "No Permissions")
            host_permissions = manifest.get("permissions", "No Host Permissions")
            browser_actions = manifest.get("browser_action", "No browser actions")

            extensions_data.append({
                "Extension ID": extensions_id,
                "Name": name,
                "Description": description,
                "Manifest_Version": manifest_version,
                "Version": version,
                "Permissions": permissions,
                "Host Permissions": host_permissions,
                "Background Scripts": background_script,
                "Content Scripts": content_scripts,
                "WARs": wars,
                "Browser Actions": browser_actions,
                "Comments": comments
            })
        else:
            print(f"Skipping {extensions_id} - Invalid manifest.json")

    except Exception as e:
        print(f"Error reading {manifest_path}: {e}")

df = pd.DataFrame(extensions_data)

df.to_csv("D:\\extensions\\combined\\extensions_data.csv", index=False)
