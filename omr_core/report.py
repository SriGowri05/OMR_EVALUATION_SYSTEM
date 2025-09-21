import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

def generate_report(df, summary_data, output_dir, set_name="Set"):
    if df.empty:
        print("Report skipped: empty data")
        return

    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, f"{set_name}_OMR_Scores.csv")
    df.to_csv(csv_path, index=False)
    print(f"Report CSV saved to: {csv_path}")

    # Plot Total_Score
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Student_ID', y='Total_Score', data=df, palette="viridis")
    plt.title(f"Total Scores - {set_name}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plot_path = os.path.join(output_dir, f"{set_name}_score_plot.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Score plot saved to: {plot_path}")

    return csv_path, plot_path
