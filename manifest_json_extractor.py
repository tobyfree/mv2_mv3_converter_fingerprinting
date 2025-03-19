import ast
import os
import json
import re
import openpyxl

import pandas as pd

#change directory depending on own structure
data_folder = "D:\\extensions\\large-dataset\\V2"

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
            print(f"Reading {extensions_id}")
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
                "Externally Connectable": "empty",
                "Declarative Net Requests": "empty",
                "Side Panel": "empty",
                "Content Security Policy": "empty",
                "WARs": "empty",
                "Comments": "empty",
                "Browser Actions": "empty",
                "Actions": "empty"
            })

        elif isinstance(manifest, dict):
            name = manifest.get("name", "Unknown")
            manifest_version = manifest.get("manifest_version", "Unknown")
            version = manifest.get("version", "Unknown")
            description = manifest.get("description", "No description")
            background_script = manifest.get("background", "No background")
            content_scripts = manifest.get("content_scripts", "No content scripts")
            externally_connectable = manifest.get("externally_connectable", "No external connection")
            declarative_net_request = manifest.get("declarative_net_request", "No declarative net request")
            side_panel = manifest.get("side_panel", "No side panel")
            wars = manifest.get("web_accessible_resources", "No WARs")
            permissions = manifest.get("permissions", "No Permissions")
            host_permissions = manifest.get("host_permissions", "No Host Permissions")
            browser_actions = manifest.get("browser_action", "No browser actions")
            actions = manifest.get("action", "No actions")
            content_security_policy = manifest.get("content_security_policy", "No content security policy")


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
                "Externally Connectable": externally_connectable,
                "Declarative Net Requests": declarative_net_request,
                "Side Panel": side_panel,
                "WARs": wars,
                "Content Security Policy": content_security_policy,
                "Browser Actions": browser_actions,
                "Actions": actions,
                "Comments": comments
            })
        else:
            print(f"Skipping {extensions_id} - Invalid manifest.json")

    except Exception as e:
        print(f"Error reading {manifest_path}: {e}")

columns = ["Extension ID",
                "Name",
                "Description",
                "Manifest_Version",
                "Version",
                "Permissions",
                "Host Permissions",
                "Background Scripts",
                "Content Scripts",
                "Externally Connectable",
                "Declarative Net Requests",
                "Side Panel",
                "WARs",
                "Content Security Policy",
                "Browser Actions",
                "Actions",
                "Comments"]

df = pd.DataFrame(extensions_data)


def convert_lists(value):
    """Ensure lists and nested structures are stored properly in Excel"""
    if isinstance(value, list):
        # Convert each item to a string, handling dictionaries inside lists
        return ", ".join(str(item) if isinstance(item, str) else json.dumps(item) for item in value)

    elif isinstance(value, str):
        try:
            parsed_value = ast.literal_eval(value)  # Convert back if stored as a string
            if isinstance(parsed_value, list):
                return ", ".join(str(item) if isinstance(item, str) else json.dumps(item) for item in parsed_value)
        except:
            return value  # Return as-is if conversion fails

    return value

def clean_text(value):
    """ Remove any illegal characters from the text """
    if isinstance(value, str):
        return "".join(c for c in value if c.isprintable())
    return value  # Return original value if not a string

# Apply cleaning function to all columns
df = df.map(convert_lists)
df = df.map(clean_text)

df.to_excel("D:\\extensions\\large-dataset\\V2\\data-description.xlsx", columns=columns, index=False)
