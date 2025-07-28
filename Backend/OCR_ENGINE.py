from PIL import Image
import pytesseract
import cv2
import numpy as np

def pre_process_img(img_path: str) -> np.ndarray:
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Binarize the image


    #resize
    scale_percent = 150 
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    resized = cv2.resize(thresh, (width, height), interpolation = cv2.INTER_AREA)
    


    return resized

def perform_ocr(image_path: str, lang: str = "hin") -> str:
    preprocessed_image = pre_process_img(image_path)
    pil_image = Image.fromarray(preprocessed_image)

    custom_config = "--oem 1 --psm 6"

    return pytesseract.image_to_string(pil_image, lang=lang, config=custom_config).strip()