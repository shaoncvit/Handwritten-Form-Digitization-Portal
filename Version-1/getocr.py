import cv2
# import matplotlib.pyplot as plt
import numpy as np
import csv
import easyocr
from nltk.translate.bleu_score import sentence_bleu
import random
import os
import subprocess
import glob
import json
from natsort import natsorted
import requests
import base64


def ocr(image_path,ocr_type = "easy_ocr", lang = "en", text_type = "key"):
    if ocr_type == "easy_ocr" and text_type == "key":
        reader = easyocr.Reader(["en"], gpu = True)

        ocr_result = reader.readtext(image_path)

    elif ocr_type == "easy_ocr" and text_type == "val":
        reader = easyocr.Reader([lang], gpu = True)

        ocr_result = reader.readtext(image_path)

    elif ocr_type == "tesseract" and text_type == "val":
        pass

    return ocr_result


def bhashini_ocr(image_path, ocr_lang):
    sample_image = image_path

    url = "https://ilocr.iiit.ac.in/ocr/infer"

    base64_image = []

    word_image1 = base64.b64encode(open(sample_image, 'rb').read()).decode()

    base64_image.append(word_image1)

    payload = json.dumps({ "modality": "handwritten", 
                          "language": ocr_lang, 
                          "version": "v3", 
                          "imageContent": base64_image})
    headers = { 'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload) 
    ocr_output = response.json()
    print(ocr_output[0]["text"])

    return ocr_output[0]["text"]
    


