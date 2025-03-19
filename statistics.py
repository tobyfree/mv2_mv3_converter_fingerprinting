import pandas as pd

# Load the Excel file (update the path)
df = pd.read_excel("D:\\extensions\\large-dataset\\data-description-all.xlsx")

manifest_version = 3
number_of_extensions = df[(df["Manifest_Version"] == manifest_version)].shape[0]
print(number_of_extensions)
count_permissions = df[(df["Manifest_Version"] == manifest_version) & (df["Permissions"] == "No Permissions")].shape[0]
percentage_permissions = (count_permissions / number_of_extensions) * 100
using_permissions = 100 - percentage_permissions
print(f"Number of 'No Permissions' entries where 'Manifest Version' is {manifest_version}: {count_permissions}. Percentage: {percentage_permissions}. Using Percentage: {using_permissions}")

count_host_permissions = df[(df["Manifest_Version"] == manifest_version) & (df["Host Permissions"] == "No Host Permissions")].shape[0]
percentage_host_permissions = (count_host_permissions / number_of_extensions) * 100
using_host_permissions = 100 - percentage_host_permissions
print(f"Number of 'No Host Permissions' entries where 'Manifest Version' is {manifest_version}: {count_host_permissions}. Percentage: {percentage_host_permissions}. Using Percentage: {using_host_permissions}")

count_background = df[(df["Manifest_Version"] == manifest_version) & (df["Background Scripts"] == "No background")].shape[0]
percentage_background = (count_background / number_of_extensions) * 100
using_background = 100 - percentage_background
print(f"Number of 'No background' entries where 'Manifest Version' is {manifest_version}: {count_background}. Percentage: {percentage_background}. Using Percentage: {using_background}")


count_content_scripts = df[(df["Manifest_Version"] == manifest_version) & (df["Content Scripts"] == "No content scripts")].shape[0]
percentage_content_scripts = (count_content_scripts / number_of_extensions) * 100
using_content_scripts = 100 - percentage_content_scripts
print(f"Number of 'No content_scripts' entries where 'Manifest Version' is {manifest_version}: {count_content_scripts}. Percentage: {percentage_content_scripts}. Using Percentage: {using_content_scripts}")

count_wars = df[(df["Manifest_Version"] == manifest_version) & (df["WARs"] == "No WARs")].shape[0]
percentage_wars = (count_wars / number_of_extensions) * 100
using_wars = 100 - percentage_wars
print(f"Number of 'No WARs' entries where 'Manifest Version' is {manifest_version}: {count_wars}. Percentage: {percentage_wars}. Using Percentage: {using_wars}")

count_content_security_policy = df[(df["Manifest_Version"] == manifest_version) & (df["Content Security Policy"] == "No content security policy")].shape[0]
percentage_content_security_policy = (count_content_security_policy / number_of_extensions) * 100
using_content_security_policy = 100 - percentage_content_security_policy
print(f"Number of 'No content security policy' entries where 'Manifest Version' is {manifest_version}: {count_content_security_policy}. Percentage: {percentage_content_security_policy}. Using Percentage: {using_content_security_policy}")

count_browser_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Browser Actions"] == "No browser actions")].shape[0]
percentage_browser_actions = (count_browser_actions / number_of_extensions) * 100
using_browser_actions = 100 - percentage_browser_actions
print(f"Number of 'No browser actions' entries where 'Manifest Version' is {manifest_version}: {count_browser_actions}. Percentage: {percentage_browser_actions}. Using Percentage: {using_browser_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Actions"] == "No actions")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No actions' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Externally Connectable"] == "No external connection")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No externally connection' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Declarative Net Requests"] == "No declarative net request")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No declarative net request' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Side Panel"] == "No side panel")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No side panel' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")


manifest_version = 2
number_of_extensions = df[(df["Manifest_Version"] == manifest_version)].shape[0]
print(number_of_extensions)
count_permissions = df[(df["Manifest_Version"] == manifest_version) & (df["Permissions"] == "No Permissions")].shape[0]
percentage_permissions = (count_permissions / number_of_extensions) * 100
using_permissions = 100 - percentage_permissions
print(f"Number of 'No Permissions' entries where 'Manifest Version' is {manifest_version}: {count_permissions}. Percentage: {percentage_permissions}. Using Percentage: {using_permissions}")

count_host_permissions = df[(df["Manifest_Version"] == manifest_version) & (df["Host Permissions"] == "No Host Permissions")].shape[0]
percentage_host_permissions = (count_host_permissions / number_of_extensions) * 100
using_host_permissions = 100 - percentage_host_permissions
print(f"Number of 'No Host Permissions' entries where 'Manifest Version' is {manifest_version}: {count_host_permissions}. Percentage: {percentage_host_permissions}. Using Percentage: {using_host_permissions}")

count_background = df[(df["Manifest_Version"] == manifest_version) & (df["Background Scripts"] == "No background")].shape[0]
percentage_background = (count_background / number_of_extensions) * 100
using_background = 100 - percentage_background
print(f"Number of 'No background' entries where 'Manifest Version' is {manifest_version}: {count_background}. Percentage: {percentage_background}. Using Percentage: {using_background}")


count_content_scripts = df[(df["Manifest_Version"] == manifest_version) & (df["Content Scripts"] == "No content scripts")].shape[0]
percentage_content_scripts = (count_content_scripts / number_of_extensions) * 100
using_content_scripts = 100 - percentage_content_scripts
print(f"Number of 'No content_scripts' entries where 'Manifest Version' is {manifest_version}: {count_content_scripts}. Percentage: {percentage_content_scripts}. Using Percentage: {using_content_scripts}")

count_wars = df[(df["Manifest_Version"] == manifest_version) & (df["WARs"] == "No WARs")].shape[0]
percentage_wars = (count_wars / number_of_extensions) * 100
using_wars = 100 - percentage_wars
print(f"Number of 'No WARs' entries where 'Manifest Version' is {manifest_version}: {count_wars}. Percentage: {percentage_wars}. Using Percentage: {using_wars}")

count_content_security_policy = df[(df["Manifest_Version"] == manifest_version) & (df["Content Security Policy"] == "No content security policy")].shape[0]
percentage_content_security_policy = (count_content_security_policy / number_of_extensions) * 100
using_content_security_policy = 100 - percentage_content_security_policy
print(f"Number of 'No content security policy' entries where 'Manifest Version' is {manifest_version}: {count_content_security_policy}. Percentage: {percentage_content_security_policy}. Using Percentage: {using_content_security_policy}")

count_browser_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Browser Actions"] == "No browser actions")].shape[0]
percentage_browser_actions = (count_browser_actions / number_of_extensions) * 100
using_browser_actions = 100 - percentage_browser_actions
print(f"Number of 'No browser actions' entries where 'Manifest Version' is {manifest_version}: {count_browser_actions}. Percentage: {percentage_browser_actions}. Using Percentage: {using_browser_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Actions"] == "No actions")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No actions' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Externally Connectable"] == "No external connection")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No externally connection' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Declarative Net Requests"] == "No declarative net request")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No declarative net request' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] == manifest_version) & (df["Side Panel"] == "No side panel")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No side panel' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

manifest_version = 1
number_of_extensions = df[(df["Manifest_Version"] != manifest_version)].shape[0]
print(number_of_extensions)
count_permissions = df[(df["Manifest_Version"] != manifest_version) & (df["Permissions"] == "No Permissions")].shape[0]
percentage_permissions = (count_permissions / number_of_extensions) * 100
using_permissions = 100 - percentage_permissions
print(f"Number of 'No Permissions' entries where 'Manifest Version' is {manifest_version}: {count_permissions}. Percentage: {percentage_permissions}. Using Percentage: {using_permissions}")

count_host_permissions = df[(df["Manifest_Version"] != manifest_version) & (df["Host Permissions"] == "No Host Permissions")].shape[0]
percentage_host_permissions = (count_host_permissions / number_of_extensions) * 100
using_host_permissions = 100 - percentage_host_permissions
print(f"Number of 'No Host Permissions' entries where 'Manifest Version' is {manifest_version}: {count_host_permissions}. Percentage: {percentage_host_permissions}. Using Percentage: {using_host_permissions}")

count_background = df[(df["Manifest_Version"] != manifest_version) & (df["Background Scripts"] == "No background")].shape[0]
percentage_background = (count_background / number_of_extensions) * 100
using_background = 100 - percentage_background
print(f"Number of 'No background' entries where 'Manifest Version' is {manifest_version}: {count_background}. Percentage: {percentage_background}. Using Percentage: {using_background}")


count_content_scripts = df[(df["Manifest_Version"] != manifest_version) & (df["Content Scripts"] == "No content scripts")].shape[0]
percentage_content_scripts = (count_content_scripts / number_of_extensions) * 100
using_content_scripts = 100 - percentage_content_scripts
print(f"Number of 'No content_scripts' entries where 'Manifest Version' is {manifest_version}: {count_content_scripts}. Percentage: {percentage_content_scripts}. Using Percentage: {using_content_scripts}")

count_wars = df[(df["Manifest_Version"] != manifest_version) & (df["WARs"] == "No WARs")].shape[0]
percentage_wars = (count_wars / number_of_extensions) * 100
using_wars = 100 - percentage_wars
print(f"Number of 'No WARs' entries where 'Manifest Version' is {manifest_version}: {count_wars}. Percentage: {percentage_wars}. Using Percentage: {using_wars}")

count_content_security_policy = df[(df["Manifest_Version"] != manifest_version) & (df["Content Security Policy"] == "No content security policy")].shape[0]
percentage_content_security_policy = (count_content_security_policy / number_of_extensions) * 100
using_content_security_policy = 100 - percentage_content_security_policy
print(f"Number of 'No content security policy' entries where 'Manifest Version' is {manifest_version}: {count_content_security_policy}. Percentage: {percentage_content_security_policy}. Using Percentage: {using_content_security_policy}")

count_browser_actions = df[(df["Manifest_Version"] != manifest_version) & (df["Browser Actions"] == "No browser actions")].shape[0]
percentage_browser_actions = (count_browser_actions / number_of_extensions) * 100
using_browser_actions = 100 - percentage_browser_actions
print(f"Number of 'No browser actions' entries where 'Manifest Version' is {manifest_version}: {count_browser_actions}. Percentage: {percentage_browser_actions}. Using Percentage: {using_browser_actions}")

count_actions = df[(df["Manifest_Version"] != manifest_version) & (df["Actions"] == "No actions")].shape[0]
percentage_actions = ((count_actions + count_browser_actions) / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No actions' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] != manifest_version) & (df["Externally Connectable"] == "No external connection")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No externally connection' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] != manifest_version) & (df["Declarative Net Requests"] == "No declarative net request")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No declarative net request' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")

count_actions = df[(df["Manifest_Version"] != manifest_version) & (df["Side Panel"] == "No side panel")].shape[0]
percentage_actions = (count_actions / number_of_extensions) * 100
using_actions = 100 - percentage_actions
print(f"Number of 'No side panel' entries where 'Manifest Version' is {manifest_version}: {count_actions}. Percentage: {percentage_actions}. Using Percentage: {using_actions}")
