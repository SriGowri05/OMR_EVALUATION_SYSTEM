import os
import shutil
import traceback
import pandas as pd

from omr_core import preprocessing, scoring, evaluation, summary, report
import pdfplumber


def load_answer_key_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]  # Get first page
        table = page.extract_table()

    if not table:
        raise ValueError("No table found in PDF answer key")

    # Convert table to DataFrame for easier processing
    df = pd.DataFrame(table[1:], columns=table[0])
    df.columns = df.columns.str.strip()

    answer_key = {}
    question_num = 1

    # Loop through all columns and their values to build answer key dict
    for col in df.columns:
        for val in df[col].dropna():
            val = str(val).strip()
            if '-' in val:
                ans = val.split('-')[1].strip()
            elif '.' in val:
                ans = val.split('.')[1].strip()
            else:
                ans = val
            answer_key[question_num] = ans
            question_num += 1

    return answer_key


STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
def load_answer_key(file_path, sheet_name=None):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.xlsx', '.xls']:
        # Use existing Excel loader in scoring.py
        return scoring.load_answer_key(file_path, sheet_name)
    elif ext == '.pdf':
        # Load from PDF using pdfplumber
        return load_answer_key_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported answer key format: {ext}")
def run_full_pipeline(omr_sheets_folder, answer_key_path):
    logs = []
    plot_filenames = []

    # Clear static folder
    if os.path.exists(STATIC_DIR):
        for f in os.listdir(STATIC_DIR):
            file_path = os.path.join(STATIC_DIR, f)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"❌ Failed to delete {file_path}: {e}")

    os.makedirs(STATIC_DIR, exist_ok=True)

    try:
        logs.append("▶️ Loading answer key...")
        answer_key = load_answer_key(answer_key_path)

        # Convert DataFrame answer_key to dict if needed
        if isinstance(answer_key, pd.DataFrame):
            answer_key_dict = {}
            for idx, row in answer_key.iterrows():
                q = row['Question'] if 'Question' in row else idx + 1
                a = row['Answer'] if 'Answer' in row else row[1]
                answer_key_dict[q] = a
            answer_key = answer_key_dict

        logs.append("✅ Answer key loaded.")
    except Exception as e:
        logs.append(f"❌ Failed to load answer key: {e}")
        logs.append(traceback.format_exc())
        return ("\n".join(logs), [])

    try:
        logs.append("▶️ Running evaluation on OMR sheets...")

        # <-- Place here -->
        num_questions = len(answer_key)  # get number of questions
        df_results = evaluation.evaluate_answers(omr_sheets_folder, num_questions, answer_key)
        if df_results.empty:
            logs.append("❌ No valid OMR sheets processed.")
            return ("\n".join(logs), [])

        logs.append(f"✅ Evaluation processed {len(df_results)} OMR sheets.")

        # Save results CSV
        output_csv = os.path.join(omr_sheets_folder, "OMR_Scores.csv")
        df_results.to_csv(output_csv, index=False)
        logs.append(f"✅ Evaluation complete. Scores saved to {output_csv}")
    except Exception as e:
        logs.append(f"❌ Evaluation failed: {e}")
        logs.append(traceback.format_exc())
        return ("\n".join(logs), [])

    try:
        logs.append("▶️ Creating summary...")
        summary_data = summary.create_summary(output_csv)
        print("DEBUG summary_data:", summary_data)  # Debug print

        if summary_data:
            logs.append(f"✅ Summary: Avg Score {summary_data['average_score']:.2f}, "
                        f"Max Score {summary_data['max_score']}, "
                        f"Top Students {summary_data['top_students']}")
        else:
            logs.append("❌ Summary creation skipped.")
    except Exception as e:
        logs.append(f"❌ Summary creation failed: {e}")
        logs.append(traceback.format_exc())
        return ("\n".join(logs), [])

    try:
        logs.append("▶️ Generating report plots...")
        csv_df = pd.read_csv(output_csv)
        report_dir = STATIC_DIR
        csv_report_path, plot_path = report.generate_report(csv_df, summary_data, report_dir, set_name="OMR Results")
        if plot_path:
            plot_filenames.append(os.path.basename(plot_path))
            logs.append(f"✅ Report generated: {plot_path}")
        else:
            logs.append("❌ Report generation skipped.")
    except Exception as e:
        logs.append(f"❌ Report generation failed: {e}")
        logs.append(traceback.format_exc())
        return ("\n".join(logs), [])

    return "\n".join(logs), plot_filenames


    


if __name__ == "__main__":
    # For quick local testing
    omr_folder = r"C:\Users\enugu sarika reddy\OneDrive\Desktop\omr_system\uploads\omr_sheets"
    answer_key_file = r"C:\Users\enugu sarika reddy\OneDrive\Desktop\omr_system\uploads\answer_key.pdf"  # or .xlsx
    summary_log, plots = run_full_pipeline(omr_folder, answer_key_file)
    print(summary_log)
