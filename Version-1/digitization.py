import cv2
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
import getocr



def digitize(image_path, ocr_type = "easyocr", ocr_lang = "en", mode= "template"):

    if mode == "template":
        count = 1
        digitized_temp_key = {}
        image_name = os.path.basename(image_path).split(".")[0]
        extracted_images_sub_folder = os.path.join("form_template_info", image_name)

        #reading the extracted images
        extracted_images_folder = os.path.join(extracted_images_sub_folder, "extracted_key_images") 
        print(extracted_images_folder)
        images = glob.glob(os.path.join(extracted_images_folder, "*.png"))
        images = natsorted(images)
        print(len(images))

        for single_img in images:

            result_ocr = getocr.ocr(single_img)

            # single_img_name = os.path.basename(single_img).split(".")[0]

            merge_text = ""

            for i in range(len(result_ocr)):

                info_ocr = result_ocr[i]

                text = info_ocr[1]
                merge_text+= text + " "

            digitized_temp_key[str(count)] = merge_text
            print(merge_text)
            count += 1

        ocred_key_json_path = os.path.join(extracted_images_sub_folder, "ocred_key.json")


        with open (ocred_key_json_path, "w") as f:

            json.dump(digitized_temp_key, f, indent = 4)

        
        

        
    if mode == "form":
        count = 1

        digitized_form_val = {}

        image_name = os.path.basename(image_path).split(".")[0]
        # image_name_split = image_name.split("_")
        extracted_image_sub_sub_folder = image_name

        extracted_image_sub_folder = os.path.join("temp",extracted_image_sub_sub_folder)

        extracted_image_folder = glob.glob(os.path.join(extracted_image_sub_folder, "val_*"))
        print(extracted_image_folder)
        extracted_image_folder = natsorted(extracted_image_folder)

        for single_image_folder in extracted_image_folder:
            folder_name = os.path.basename(single_image_folder)

            cropped_images_single_folder = glob.glob(os.path.join(single_image_folder, "*"))
            
            print(cropped_images_single_folder)
            list_ocred_image = []

            for cropped_single_image in cropped_images_single_folder:

                
                
                if ocr_type == "easyocr":
                    result_ocr = getocr.ocr(cropped_single_image, lang = ocr_lang, text_type = "val")

                    merge_text = ""

                    for i in range(len(result_ocr)):

                        info_ocr = result_ocr[i]

                        text = info_ocr[1]
                        merge_text+= text + " "

                    list_ocred_image.append(merge_text)

            # digitized_form_val[str(count)] = merge_text
            # count += 1

                elif ocr_type == "IIIT-H-OCR":
                    result_ocr = getocr.bhashini_ocr(cropped_single_image, ocr_lang)
                    list_ocred_image.append(result_ocr)
                
            digitized_form_val[str(count)] = list_ocred_image

            count += 1
                    

        return digitized_form_val



