# organize_stats: Stats about syntactic constructions in different corpora
import pandas as pd
from pathlib import Path

base_dir = Path("/Users/argy/workspace/extractor/data/stats")
rows = []

for folder in base_dir.iterdir():
    if not folder.is_dir():
        continue

    for file in folder.glob("*.txt"):
        corpus = file.stem.replace(f"{folder.name}.parsed", "")
        folder_name = folder.name

        # Initialize sum
        construction_sum = 0

        # Skip empty files
        if file.stat().st_size == 0:
            print(f"Skipping empty file: {file}")
        else:
            try:
                df = pd.read_csv(file)
                # Drop columns we don't need
                df_counts = df.drop(columns=["Filename"], errors="ignore")
                if not df_counts.empty:
                    first_col = df_counts.columns[0]
                    total = df_counts[first_col].iloc[0]
                    construction_sum = (df_counts.drop(columns=first_col).select_dtypes(include='number').sum(axis=1).iloc[0])

            except pd.errors.EmptyDataError:
                print(f"Empty data in file, skipping: {file}")
            except Exception as e:
                print(f"Error processing {file}: {e}")

        rows.append({
            "corpus": corpus,
            "category_name": folder_name,
            "category_count": construction_sum,
            "total": total
        })

# Create final summary table
summary_df = pd.DataFrame(rows)

# Save to CSV
summary_df.to_csv("stats_by_category.csv", index=False)

print("Saved: stats_by_category.csv")
