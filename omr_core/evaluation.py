import os
import cv2
import numpy as np
import pandas as pd
from .preprocessing import preprocess_image  # your preprocessing function


def detect_bubbles(thresh_img, num_questions, options_per_question=4, debug=False):
    """
    Detect marked bubbles in a thresholded image and return the selected answers.

    Args:
        thresh_img (numpy array): Thresholded OMR image (binary).
        num_questions (int): Number of questions expected.
        options_per_question (int): Number of options per question, default 4 (A-D).
        debug (bool): Print debug info if True.

    Returns:
        dict: question_number -> selected_option_letter (e.g. {1: 'A', 2: 'C', ...})
    """
    # Find contours in the thresholded image
    cnts, _ = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    question_contours = []

    # Filter contours likely to be bubbles based on size and shape
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = w / float(h)
        if w >= 20 and h >= 20 and 0.8 <= aspect_ratio <= 1.2:
            question_contours.append(c)

    # Sort bubbles top-to-bottom (by y-coordinate)
    question_contours = sorted(question_contours, key=lambda c: cv2.boundingRect(c)[1])

    answers = {}

    # Group bubbles by question and determine filled bubble per question
    for q_idx, i in enumerate(range(0, len(question_contours), options_per_question)):
        if q_idx + 1 > num_questions:
            break
        row_cnts = question_contours[i : i + options_per_question]
        # Sort left to right within the question options
        row_cnts = sorted(row_cnts, key=lambda c: cv2.boundingRect(c)[0])

        max_nonzero = 0
        selected_option = None

        for opt_idx, c in enumerate(row_cnts):
            mask = np.zeros(thresh_img.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            masked_region = cv2.bitwise_and(thresh_img, thresh_img, mask=mask)
            non_zero = cv2.countNonZero(masked_region)

            if debug:
                print(f"Question {q_idx+1}, option {opt_idx} (letter {chr(ord('A') + opt_idx)}), non-zero pixels: {non_zero}")

            if non_zero > max_nonzero:
                max_nonzero = non_zero
                selected_option = opt_idx

        option_letter = chr(ord('A') + selected_option) if selected_option is not None else None
        answers[q_idx + 1] = option_letter

    return answers


def evaluate_answers(images_folder, num_questions, answer_key, options_per_question=4, debug=False):
    """
    Evaluate all OMR sheets in a folder against the answer key.

    Args:
        images_folder (str): Path to folder containing OMR images.
        num_questions (int): Number of questions on the sheet.
        answer_key (dict): Correct answers, e.g. {1:'A', 2:'B', ...}
        options_per_question (int): Number of options per question.
        debug (bool): Print debug info.

    Returns:
        pandas.DataFrame: Results containing student IDs, their answers, and total scores.
    """
    results = []

    for filename in os.listdir(images_folder):
        if filename.lower().endswith((".jpg", ".png")):
            img_path = os.path.join(images_folder, filename)
            preprocessed_img = preprocess_image(img_path)
            if preprocessed_img is None:
                if debug:
                    print(f"Skipping {filename}: could not preprocess image.")
                continue

            student_answers = detect_bubbles(preprocessed_img, num_questions, options_per_question, debug)

            total_score = score_omr(student_answers, answer_key)

            entry = {'Student_ID': filename, **student_answers, 'Total_Score': total_score}
            results.append(entry)

    if not results:
        print("⚠️ No valid OMR images found in:", images_folder)

    return pd.DataFrame(results)


def score_omr(student_answers, answer_key):
    """
    Score student answers against the answer key.

    Args:
        student_answers (dict): student answers, e.g. {1:'A', 2:'C', ...}
        answer_key (dict): correct answers.

    Returns:
        int: total score.
    """
    score = 0
    for q, ans in student_answers.items():
        if answer_key.get(q) and ans == answer_key[q]:
            score += 1
    return score
