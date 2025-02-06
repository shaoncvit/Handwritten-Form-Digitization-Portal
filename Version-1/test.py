import cv2

import numpy as np
import csv
import easyocr
from nltk.translate.bleu_score import sentence_bleu
import os
import subprocess
import json
import torch
import utils, align, digitization



class FormDigitization:

    def __init__(self):

        self.saved_masked_image_dir = "masked_output"
        self.dir_align_image = "aligned_images"
        self.dir_alignv1_image = "aligned_version1"
        self.dir_template_image_info = "form_template_info"
        self.final_result_directory = "result"
        self.temp_folder = "temp"


    def run(self,template_image_path, input_image_path, ocr_type= "IIIT-H-OCR", ocr_lang = "hi"):
        #segment the image for seperating out the foregorund and background
        print(ocr_type)
        os.makedirs(self.temp_folder, exist_ok = True)
        utils.backgroundRemoval(input_image_path, self.saved_masked_image_dir)

        #get the biggest contour
        biggest_contour = utils.detectMaxContour(input_image_path, self.saved_masked_image_dir)

        #get the corner points from the largest contour

        corner_points = utils.getCornerPoints(biggest_contour)

        #get the four combination of the corner points

        list_corner_points = utils.createCombination(corner_points)

        #check the corrected aligne imag

        final_aligned_image_path = align.getCheckAlign(template_image_path, input_image_path, list_corner_points, self.dir_alignv1_image, self.dir_align_image)


        #extract and digitize

        template_name = os.path.basename(template_image_path).split(".")[0]

        bbox_json_subPath = os.path.join(self.dir_template_image_info, template_name)

        bbox_json_path = os.path.join(bbox_json_subPath, "key_val_pair.json")

        utils.extractBoundingBox(bbox_json_path,final_aligned_image_path, mode = "val")

        #digitizing the values from the form

        if ocr_type == "easyocr":

            digitized_val = digitization.digitize(final_aligned_image_path,ocr_type, ocr_lang,  mode = "form")

        elif ocr_type == "IIIT-H-OCR":

            print("entering....")

            digitized_val = digitization.digitize(final_aligned_image_path, ocr_type, ocr_lang, mode = "form")


        #get the digitized key from the template
        print(digitized_val)

        ocred_key_path = os.path.join(bbox_json_subPath, "ocred_key.json")

        with open(ocred_key_path, 'r') as file:

            digitize_key = json.load(file)

        key_val_pair = utils.mergeKeyValPair(digitize_key, digitized_val)

        utils.clear_folder(self.dir_alignv1_image)
        utils.clear_folder(self.temp_folder)
        utils.clear_folder(self.saved_masked_image_dir)

        return key_val_pair








    







        


