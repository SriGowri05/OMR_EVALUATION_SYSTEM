from preprocessing import preprocess_image
import cv2

if __name__ == "__main__":
    img_path = r"C:\Users\enugu sarika reddy\OneDrive\Desktop\omr_system\uploads\OMR-CTET-SHEET-Sample.jpg"  # Change this to your actual OMR image file path
    processed_img = preprocess_image(img_path)
    
    if processed_img is not None:
        cv2.imshow("Processed OMR Image", processed_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Failed to process image.")
