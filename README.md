# OMR Evaluation System

📘 **Innomatics Research Labs** - Optical Mark Recognition (OMR) Evaluation System

---

## Overview

This project is a complete pipeline for evaluating OMR sheets. It automates:

- Loading answer keys (from PDF or Excel)
- Preprocessing OMR sheet images
- Detecting marked answers using image processing
- Scoring student responses against the answer key
- Generating evaluation summaries and reports with plots

---

## Features

- Supports answer keys in **PDF** or **Excel** formats
- Processes scanned OMR sheets (images)
- Scores student answers automatically
- Outputs CSV files with individual scores
- Creates summary statistics and visualization reports
- Clean static directory management for output files

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SriGowri05/OMR_EVALUATION_SYSTEM.git
   cd OMR_EVALUATION_SYSTEM
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt

---

## Usage
1. Place your OMR sheet images (JPG or PNG) in the folder:
   ```bash
   uploads/omr_sheets/
2. Place your answer key file (.pdf or .xlsx) in the uploads folder:
   ```bash
   uploads/answer_key.pdf
3. Run the evaluation pipeline script:
   ```bash
   python -m omr_core.pipeline
4. Results will be saved as:
- OMR_Scores.csv in your OMR sheets folder
- Summary logs and generated plots in the static/ directory

---

## File Structure
```
OMR_EVALUATION_SYSTEM/
├── omr_core/
│   ├── preprocessing.py
│   ├── scoring.py
│   ├── evaluation.py
│   ├── summary.py
│   ├── report.py
│   └── pipeline.py
├── uploads/
│   ├── omr_sheets/          # Folder containing OMR answer sheet images
│   └── answer_key.pdf       # PDF or Excel answer key
├── static/                  # Output folder for plots, CSVs, and reports
├── frontend.py              # Main script to run the application
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Troubleshooting

- Make sure the number of questions in the answer key matches the OMR sheets.
- Ensure OMR images are clear and properly scanned.
- If you face errors about missing packages, run:
   ```bash
   pip install -r requirements.txt
- If your answer key is in PDF format, it must contain a table of answers readable by pdfplumber.

---

## 👨‍💻 Authors

This project was developed as part of an **Code4EdTech Hackathon** at **Innomatics Research Labs** by:

- [SriGowri Cheboyina](https://github.com/SriGowri05)
- [Sandhya Nayini](https://github.com/Sandhya120727)
- [Siliveri Vandhitha](https://github.com/vandhitha23)



