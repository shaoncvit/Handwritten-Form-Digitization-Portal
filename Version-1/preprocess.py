import cv2
import matplotlib.pyplot as plt
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

import utils, digitization

def temPreprocess(template_path,template_annotation_path, ocr_reader,craft_model_path = "CRAFT-pytorch/text_detection_model/craft_mlt_25k.pth"):
    
    template_image = cv2.imread(template_path)
    template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2RGB)
    template_folder_name = os.path.basename(template_path).split(".")[0]
    print(template_folder_name)
    template_dir = template_path.split("/")[-2]
    print(f"template dir {template_dir}")
    final_template_dir = os.path.join("form_template_info", template_dir)
    print(f"final_template_dir {final_template_dir}")
    craft_model_path = craft_model_path
    python_command_CRAFT = f"python CRAFT-pytorch/test.py --trained_model {craft_model_path} --test_folder {final_template_dir} --saved_result {final_template_dir}"
    subprocess.call(python_command_CRAFT, shell= True)


    detected_bbox_path = "res_" + template_folder_name + ".txt"
    crafted_template_boxes_path = os.path.join(final_template_dir, detected_bbox_path)
    utils.modifyLine(crafted_template_boxes_path)
    lines_bbox_template = utils.readfile(crafted_template_boxes_path)
    

    dict_roi_bbox_template = utils.mergeBoundingBoxHw(lines_bbox_template)
    list_template_boxes = utils.getListBox(dict_roi_bbox_template)

    OcredOutputTemplate = utils.getDigitizedList(template_image, list_template_boxes, ocr_reader)
    print(OcredOutputTemplate)

    #convert the data into a dictionary
    json_data = {key:value for key , value in OcredOutputTemplate}

    saved_json_file_path = os.path.join(final_template_dir, "ocred.json")

    #save the data to a json file
    with open(saved_json_file_path, "w")as f:
        json.dump(json_data, f, indent = 4)


    print("Json file successfully created")


    #for saving the key value pair from the annotation of the template

    key_val_pair_json = utils.makeKeyValPair(template_annotation_path)

    saved_annotation_file_path = os.path.join(final_template_dir, "key_val_pair.json")

    with open(saved_annotation_file_path, "w") as f:
        json.dump(key_val_pair_json, f, indent = 4)

    print("Key value pair json file created successfully")

    #cropping the images from the template with the help of bounding boxes 

    key_val_pair_json_path =saved_annotation_file_path
    template_image_path = template_path


    utils.extractBoundingBox(key_val_pair_json_path, template_image_path)

    #storing the digitized key for future references
    digitization.digitize(template_path)
    print("Keys are digitized successfully and stored in a json file")


template_path = "form_template_info/template_3/template_3.png"
template_annotation_path = "form_template_info/template_3/annot_key_val.csv"
reader = easyocr.Reader(["en"], gpu = False)

temPreprocess(template_path, template_annotation_path, reader)

