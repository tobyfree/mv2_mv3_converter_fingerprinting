import os
import json
import re

import pandas as pd

data_folder = "/home/tobias/extension-data"

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
        break

    if not os.path.isfile(manifest_path):
        print(f"Manifestpath not found: {manifest_path}")
        break

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
                "Background Scripts": "empty",
                "Comments": "empty"
            })

        elif isinstance(manifest, dict):

            name = manifest.get("name", "Unknown")
            manifest_version = manifest.get("manifest_version", "Unknown")
            version = manifest.get("version", "Unknown")
            description = manifest.get("description", "No description")
            background_script = manifest.get("background", "No background")
            permissions = manifest.get("permissions", "No Permissions")

            extensions_data.append({
                "Extension ID": extensions_id,
                "Name": name,
                "Description": description,
                "Manifest_Version": manifest_version,
                "Version": version,
                "Permissions": permissions,
                "Background Scripts": background_script,
                "Comments": comments
            })
        else:
            print(f"Skipping {extensions_id} - Invalid manifest.json")

    except Exception as e:
        print(f"Error reading {manifest_path}: {e}")

df = pd.DataFrame(extensions_data)

df.to_csv("extensions_data.csv", index=False)
