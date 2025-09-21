import pandas as pd

def load_answer_key(file_path, sheet_name=0):
    """
    Load the answer key from an Excel file and return as a DataFrame.

    Parameters:
        file_path (str): Path to the answer key Excel file.
        sheet_name (str/int, optional): Sheet name or index to read. Defaults to first sheet (0).

    Returns:
        pd.DataFrame: DataFrame with the answer key.

    Raises:
        ValueError: If the answer key does not contain required columns.
        RuntimeError: For file read errors or other exceptions.
    """
    try:
        # Read the specified sheet (use openpyxl engine for .xlsx files)
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

        # If df is a dict (multiple sheets), take the first sheet DataFrame
        if isinstance(df, dict):
            df = next(iter(df.values()))

        # Define the expected columns in your answer key
        expected_columns = {'Question', 'CorrectOption'}

        # Check if expected columns are in the DataFrame
        if not expected_columns.issubset(df.columns):
            raise ValueError(f"Answer key must contain columns: {expected_columns}")

        return df

    except Exception as e:
        # Wrap and raise as RuntimeError with friendly message
        raise RuntimeError(f"Error loading answer key: {e}")


# Example usage or other scoring functions can go below
# For example, a dummy scoring function:
def score_omr_sheets(answer_sheets_dir, answer_key_df):
    """
    Dummy example function that would score OMR sheets against the answer key.

    Parameters:
        answer_sheets_dir (str): Directory where OMR sheets are stored.
        answer_key_df (pd.DataFrame): DataFrame containing the answer key.

    Returns:
        str: Summary text
        list: List of file paths for any plots generated (if any)
    """
    # Your scoring logic goes here
    summary = "Scoring completed successfully."
    plots = []  # Add generated plot file paths if applicable
    return summary, plots
