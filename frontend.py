import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import shutil
from omr_core.pipeline import run_full_pipeline  # assumes it takes (omr_dir, key_file)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB


UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

ALLOWED_SHEET_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
ALLOWED_KEY_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Check if files part exists
        if 'answer_sheets' not in request.files or 'answer_key' not in request.files:
            return render_template('upload.html', error="Please upload both answer sheets and answer key.")

        # Get list of uploaded OMR sheets
        answer_files = request.files.getlist('answer_sheets')
        key_file = request.files['answer_key']

        # Debug print to confirm received files
        print("Received OMR sheets:", [f.filename for f in answer_files if f.filename])
        print("Received answer key:", key_file.filename)

        if not answer_files or all(f.filename == '' for f in answer_files):
            return render_template('upload.html', error="No OMR sheets selected.")
        if not key_file or key_file.filename == '':
            return render_template('upload.html', error="No answer key uploaded.")

        # Clear uploads folder and recreate structure
        shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        omr_dir = os.path.join(UPLOAD_FOLDER, "omr_sheets")
        os.makedirs(omr_dir, exist_ok=True)

        # Save all OMR sheets
        for file in answer_files:
            if file and allowed_file(file.filename, ALLOWED_SHEET_EXTENSIONS):
                filename = secure_filename(file.filename)
                save_path = os.path.join(omr_dir, filename)
                file.save(save_path)
                print(f"Saved OMR sheet: {filename}")
            else:
                return render_template('upload.html', error=f"Invalid OMR file: {file.filename}")

        # Save Answer Key
        if allowed_file(key_file.filename, ALLOWED_KEY_EXTENSIONS):
            key_filename = secure_filename(key_file.filename)
            key_path = os.path.join(UPLOAD_FOLDER, key_filename)
            key_file.save(key_path)
            print(f"Saved answer key: {key_filename}")
        else:
            return render_template('upload.html', error="Invalid answer key format. Allowed formats: .xls, .xlsx, .csv")

        # Run the pipeline
        try:
            summary_text, plot_files = run_full_pipeline(omr_dir, key_path)
        except Exception as e:
            print("[ERROR]", e)  # Log the error server side
            return render_template('results.html', summary="❌ Failed to process files. Check format and content.", plots=[])

        return render_template('results.html', summary=summary_text, plots=plot_files)

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
