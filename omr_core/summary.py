import pandas as pd
import os

def create_summary(csv_file):
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        print(f"⚠️  Summary skipped: {csv_file} not found or is empty.")
        return None

    df = pd.read_csv(csv_file)
    if 'Student_ID' not in df.columns or 'Total_Score' not in df.columns:
        print(f"⚠️  Summary skipped: required columns missing in {csv_file}")
        return None

    avg_score = df['Total_Score'].mean()
    max_score = df['Total_Score'].max()
    min_score = df['Total_Score'].min()
    top_students = df[df['Total_Score'] == max_score]['Student_ID'].tolist()

    summary_data = {
        'average_score': avg_score,
        'max_score': max_score,
        'min_score': min_score,
        'top_students': top_students,
        'total_students': len(df)
    }

    # Print nicely formatted summary
    print("\n" + "="*40)
    print("           📊 Student Score Summary")
    print("="*40)
    print(f"👥 Total Students : {len(df)}")
    print(f"📈 Average Score  : {avg_score:.2f}")
    print(f"🏆 Maximum Score  : {max_score}")
    print(f"📉 Minimum Score  : {min_score}")
    print(f"🎯 Top Students   : {top_students}")
    print("="*40 + "\n")

    return summary_data
