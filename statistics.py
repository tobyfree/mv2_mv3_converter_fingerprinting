import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("extensions_data.csv")

df["manifest_version"] = pd.to_numeric(df["Manifest_Version"], errors="coerce").fillna(-1).astype(int)

version_counts = df[df["manifest_version"] > 0]["manifest_version"].value_counts().sort_index()
total_extensions = version_counts.sum()
version_percentages = (version_counts / total_extensions) * 100

distribution = pd.DataFrame({
    "Count": version_counts,
    "Percentage": version_percentages
})

print(distribution)

plt.figure(figsize=(6,4))
ax = version_counts.plot(kind="bar", color=["blue", "orange"])
for i, count in enumerate(version_counts):
    percentage = version_percentages[version_counts.index[i]]
    ax.text(i, count + 10, f"{percentage:.2f}%", ha="center", va="bottom")

plt.xlabel("Manifest Version")
plt.ylabel("Number of Extensions")
plt.title("Distribution of Manifest Versions (with Percentage")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()