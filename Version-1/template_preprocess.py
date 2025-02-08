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
import shutil
import time
import argparse


#modification of line

def modifyLine(bbox_text_file):
    with open(bbox_text_file, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

        new_lines = [item for item in lines if item]

    #write the modify lines to a new file
    with open(bbox_text_file, "w") as file:
        file.write("\n".join(new_lines))

# reading the file
def readfile(textfile):
    with open (textfile,"r") as file:
        lines = file.readlines()
        return lines
    


def checkDistanceHw(y1, y2, thresh):
    if y2- y1 <=thresh:
        return 1
    else:
        return 0
    

#merging the bounding boxes 

def mergeBoundingBoxHw(list_bounding_box):
    dictMergeBox = {}
    y_coordinates_pt = []
    mergeBox = []
    count = 0
    for i in range(len(list_bounding_box)-1):
        # print(i)
        if len(y_coordinates_pt) == 0:

            four_points1 = list_bounding_box[i].split(",")
            four_points2 = list_bounding_box[i+1].split(",")

            four_points1 = [eval(k) for k in four_points1]
            four_points2 = [eval(j) for j in four_points2]

            points1_y = four_points1[1]
            points2_y = four_points2[1]
            y_coordinates_pt.append(points1_y)
            mergeBox.append(four_points1)
        else:
            points1_y = y_coordinates_pt[-1]
            four_points2 = list_bounding_box[i+1].split(",")
            four_points2 = [eval(j) for j in four_points2]

            points2_y = four_points2[1]
            # print(i)


        if checkDistanceHw(points1_y, points2_y, 20) == 1:
            y_coordinates_pt.append(points2_y)
            mergeBox.append(four_points2)
            # print(mergeBox)

        elif checkDistanceHw(points1_y, points2_y, 20) == 0:
            if len(mergeBox) >1:
                mergeBox.sort()
            # print(mergeBox)
            dictMergeBox[count+1] = mergeBox
            y_coordinates_pt = []
            mergeBox = []
            y_coordinates_pt.append(points2_y)
            mergeBox.append(four_points2)
            count += 1
    if len(mergeBox)>1:
        mergeBox.sort()
    dictMergeBox[count+1] = mergeBox

    # print(i)
    return dictMergeBox




def getListBox(dict_boxes):
    boxes_coord = []
    for key , value in dict_boxes.items():
        single_line_boxes = dict_boxes[key]
        # print(single_line_boxes)
        

        for i in single_line_boxes:
            boxes_coord.append(i)
        


        # boxes_coord.append([for j in len(dict_boxes[key])])
    return boxes_coord

#function for clear the folder

def clear_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate over all files in the folder and delete them
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"Folder not found: {folder_path}")


#defining the bhashini ocr module

def bhashini_ocr(image_paths, ocr_lang, modality = "handwritten", version = "v3"):
    url = "https://ilocr.iiit.ac.in/ocr/infer"
    base64_image = []

    for sample_image in image_paths:

        

        word_image1 = base64.b64encode(open(sample_image, 'rb').read()).decode()

        base64_image.append(word_image1)

    payload = json.dumps({ "modality": modality, 
                          "language": ocr_lang, 
                          "version": version, 
                          "imageContent": base64_image})
    headers = { 'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload) 
    ocr_output = response.json()
    print(ocr_output)
    # print(ocr_output[0]["text"])

    return ocr_output

#function for getting the digitized list

def getDigitizedList(img,bbox_list, lang = "en", save_folder_destination = "Version-1/temp"):
    
    clear_folder(save_folder_destination)
    
    print("For digitization ", lang)
    
    digitized_word_list = []
    count = 0
    # length_box = len(bbox_list)
    boundingBox = []
    # start_time = time.time()
    for i in bbox_list:
        cropped_image = img[i[1]: i[5], i[0]: i[4]]

        #if the form's language is English
        if lang == "en":
            ocr_reader = easyocr.Reader(["en"], gpu = True)
            result = ocr_reader.readtext(cropped_image)
            print(result)
            if len(result)!= 0:
                digitized_text = result[0][1]
                digitized_word_list.append((digitized_text, i))
            else:
                digitized_text = ""
        #if the form's language is not English
        else:
            try:
                if cropped_image.size == 0:
                    raise ValueError("Image Can not be saved, Empty Image")
                # print("Entering for Bhashini Ocr model")
                # print("lang is :", lang)
                image_path = str(count) + ".png"
                image_full_path = os.path.join(save_folder_destination, image_path)

                #saving all the cropped images to the temp foldar
                cv2.imwrite(image_full_path, cropped_image)
                boundingBox.append(i)
                count += 1 

            
            except Exception as e:
                print(f"Error processing Bhashini OCR for image {image_path}: {e}")


    # #Now all the cropped images are saved in to the temp foldar
    
    # #Reading all the images and will pass it to the ocr

    # cropped_images = glob.glob(save_folder_destination +"/*.png")

    # #Ordering ascedincally based on the image names

    # cropped_images = natsorted(cropped_images)

    # #results from bhashini ocr module

    # ocr_output = bhashini_ocr(cropped_images, lang, "printed", "v4_robustbilingual")

    # end_time = time.time()
    # duration = end_time - start_time

    # print(f"To finish digitization of all the cropped images from one form time taken: {duration:.2f} seconds", flush = True)

    # #storing digitized output and it's corresponding bounding boxes 

    # for i, out in enumerate(ocr_output):

    #     if len(out["text"]) == 0:
    #         digitized_word_list.append(("", boundingBox[i]))

    #     digitized_word_list.append((out["text"], boundingBox[i]))
        # print(out["text"])

    return digitized_word_list



def modifyAnnotationFile(annotation_file_path):
    data_list = []

    with open(annotation_file_path, "r")as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")

        #Extract and process the header now

        header_row = next(csv_reader, None)

        if header_row:
            column_names = header_row[0].split(",")


            for row in csv_reader:
                #Split the label name column to get the seperate values
                label_name_values = row[0].split(",")

                #create a dictionary for each row using column names and row
                row_dict = {column_names[i]:label_name_values[i] for i in range (min(len(column_names), len(label_name_values))) }

                data_list.append(row_dict)


    return data_list



def makeKeyValPair(annotation_file_path):


    data_list_annotation_file = modifyAnnotationFile(annotation_file_path)
    key_val_dict = {}
    count = 1
    check = 0
    
    for row in data_list_annotation_file:
        # print(row)
        check +=1



        key_val_pair = []

        key_rows =[]
        label_name_key = row['label_name']
        key_val = label_name_key.split("_")[0] # Extract the key or val
        # print(f"key_name : {key_val}")

        if key_val == "key":
            tag = label_name_key.split("_")[1] #Extract the tag from the key
            # print(f"key tag : {tag}")
            bbox_info_key = []
            if label_name_key not in key_rows:
                key_rows.append(label_name_key)

                

            bbox_x = int(row["bbox_x"])
            bbox_y = int(row["bbox_y"])
            bbox_width = int(row["bbox_width"])
            bbox_height = int(row["bbox_height"])

            bbox_info_key.append(bbox_x)
            bbox_info_key.append(bbox_y)
            bbox_info_key.append(bbox_width)
            bbox_info_key.append(bbox_height)

            key_rows.append(bbox_info_key)
            # print(f"key bbox info {key_rows}")

            #find all cooresponding "val" rows with the same tag
            val_rows = []

            for val_row in data_list_annotation_file:
                val_label_name = val_row["label_name"]
                

                # print(val_label_name)

                val_name = val_label_name.split("_")[0]

                # print(f"val name: {val_name}")

                val_tag = val_label_name.split("_")[1] #Extract the tag from the value
                # print(f"value tag: {val_tag}")
                bbox_info_val = []

                if val_name == "val":
                
                    if val_tag == tag:
                        bbox_info_val = []
                        if val_label_name not in val_rows:
                            val_rows.append(val_label_name)


                        

                        bbox_x = int(val_row["bbox_x"])
                        bbox_y = int(val_row["bbox_y"])
                        bbox_width = int(val_row["bbox_width"])
                        bbox_height = int(val_row["bbox_height"])




                        bbox_info_val.append(bbox_x)
                        bbox_info_val.append(bbox_y)
                        bbox_info_val.append(bbox_width)
                        bbox_info_val.append(bbox_height)

                        val_rows.append(bbox_info_val)

                        # print(f" val bbox info: {val_rows}")

            key_val_pair.append(key_rows)
            key_val_pair.append(val_rows)
            # print(key_val_pair)

            key_val_dict[count] = key_val_pair

            count += 1

        # print(check)

    return key_val_dict



def extractBoundingBox(bbox_json_path,image_path, mode = "key", isPlot = "No", isExtract = "Yes"):

    img = cv2.imread(image_path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()

    print(img.shape)

    

    with open(bbox_json_path, "r", encoding  = "utf-8" )as f:
        data = json.load(f)

    
    
    count_key = 1

    for i, bbox_data in data.items():
        # print(i)

        if mode == "key":
            
            info_bbox = bbox_data[0]


            if isExtract == "Yes":
        

                for j in range(1,len(info_bbox)):
                    x,y,w,h = info_bbox[j][0], info_bbox[j][1], info_bbox[j][2], info_bbox[j][3]
                    
                    if w and h !=0:
                        single_image = img[y:y+h, x:x+w]
                        image_name = str(count_key) + ".png"

                        processed_image_folder = os.path.basename(image_path).split(".")[0]

                        key_image_saved_subfolder = os.path.join(processed_image_folder, "extracted_key_images")
                        
                        key_image_saved_folder = os.path.join("form_template_info", key_image_saved_subfolder)
                        os.makedirs(key_image_saved_folder, exist_ok=True)

                        single_image_saved_path = os.path.join(key_image_saved_folder, image_name)

                        cv2.imwrite(single_image_saved_path, single_image)

                count_key+=1



            if isPlot == "Yes":

                for j in range (1, len(info_bbox)):
                    x, y, w, h = info_bbox[j][0], info_bbox[j][1], info_bbox[j][2], info_bbox[j][3]

                    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),5)

            reader = easyocr.Reader(["en"], gpu = False)
        elif mode == "val":
            info_bbox = bbox_data[1]
            temporary_folder = "E:/OCR-PORTAL/Version-1/temp"


            if isExtract == "Yes":

                name_val = info_bbox[0]
                # print(name_val)
               
                
                image_name = os.path.basename(image_path).split(".")[0]
                # processed_image_folder = image_folder_split[0] + "_" + image_folder_split[1]
                saved_val_images_subfolder = os.path.join(temporary_folder,image_name)
                saved_val_imagesfolder = os.path.join(saved_val_images_subfolder, name_val)

                

                os.makedirs(saved_val_imagesfolder, exist_ok= True)
                for j in range (1, len(info_bbox)):

                    x,y,w,h = info_bbox[j][0], info_bbox[j][1], info_bbox[j][2], info_bbox[j][3]

                    # print(x, y, w, h)

                    if w and h !=0:
                        single_image = img[y:y+h, x:x+w]
                        # print(single_image.shape)
                        image_name = str(j) + ".png"
                        single_image_saved_path = os.path.join(saved_val_imagesfolder, image_name)

                        cv2.imwrite(single_image_saved_path, single_image)
            
            if isPlot == "Yes":
                for j in range (1, len(info_bbox)):
                    x, y, w, h = info_bbox[j][0], info_bbox[j][1], info_bbox[j][2], info_bbox[j][3]

                    cv2.rectangle(img_copy, (x,y), (x+w, y+h), (0,255,0),5)
            
            image_name = os.path.basename(image_path).split(".")[0]+"_form_with_plotted_bounding_box" + ".png"
            form_bbox_path = os.path.join(temporary_folder, image_name)
            cv2.imwrite(form_bbox_path, img_copy)



def ocr(image_path,ocr_type = "easy_ocr", lang = "en", text_type = "key"):
    if ocr_type == "easy_ocr" and text_type == "key":
        reader = easyocr.Reader(["en"], gpu = False)

        ocr_result = reader.readtext(image_path)

    elif ocr_type == "easy_ocr" and text_type == "val":
        reader = easyocr.Reader([lang], gpu = False)

        ocr_result = reader.readtext(image_path)

    elif ocr_type == "bhashini" and text_type == "key":
        ocr_result = bhashini_ocr(image_path, lang, "printed", "v4_robust")
        

    return ocr_result





def digitize(image_path,lang ="en", mode= "template"):

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
        print("language for key digitization:", lang)

        for single_img in images:

            if lang == "en":

                result_ocr = ocr(single_img, "easy_ocr", lang, "key" )

                # single_img_name = os.path.basename(single_img).split(".")[0]

                merge_text = ""

                for i in range(len(result_ocr)):

                    info_ocr = result_ocr[i]

                    text = info_ocr[1]
                    merge_text+= text + " "
            else:
                result_ocr = ocr(single_img, "bhashini", lang, "key")
                merge_text = result_ocr

            digitized_temp_key[str(count)] = merge_text
            print(merge_text)
            count += 1

        ocred_key_json_path = os.path.join(extracted_images_sub_folder, "ocred_key.json")


        with open (ocred_key_json_path, "w", encoding = "utf-8") as f:

            json.dump(digitized_temp_key, f,ensure_ascii=False, indent = 4)

        
        

        
    if mode == "form":
        count = 1

        digitized_form_val = {}

        image_name = os.path.basename(image_path).split("_")[0]
        image_name_split = image_name.split("_")
        extracted_image_sub_sub_folder = image_name_split[0] + "_" + image_name_split[1]

        extracted_image_sub_folder = os.path.join("aligned_verion1",extracted_image_sub_sub_folder)

        extracted_image_folder = glob.glob(os.path.join(extracted_image_sub_folder, "val_*"))
        extracted_image_folder = natsorted(extracted_image_folder)

        for single_image_folder in extracted_image_folder:
            folder_name = os.path.basename(single_image_folder)

            cropped_images_single_folder = glob.glob(os.path.join(single_image_folder, "*"))
            for cropped_single_image in cropped_images_single_folder:
                result_ocr = ocr(cropped_single_image, lang = "hi", text_type = "val")

                merge_text = ""

                for i in range(len(result_ocr)):

                    info_ocr = result_ocr[i]

                    text = info_ocr[1]
                    merge_text+= text + " "

                digitized_form_val[str(count)] = merge_text
                count += 1

        return digitized_form_val


#main function for template preprocess

def temPreprocess(template_path,template_annotation_path, lang = "en",craft_model_path = "CRAFT-pytorch/text_detection_model/craft_mlt_25k.pth"):
    

    print("Selected template language is:", lang)
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
    modifyLine(crafted_template_boxes_path)
    lines_bbox_template = readfile(crafted_template_boxes_path)
    

    dict_roi_bbox_template = mergeBoundingBoxHw(lines_bbox_template)
    list_template_boxes = getListBox(dict_roi_bbox_template)

    OcredOutputTemplate = getDigitizedList(template_image, list_template_boxes, lang)
    print(OcredOutputTemplate)

    #convert the data into a dictionary
    json_data = {key:value for key , value in OcredOutputTemplate}

    saved_json_file_path = os.path.join(final_template_dir, "ocred.json")

    #save the data to a json file
    with open(saved_json_file_path, "w", encoding = "utf-8")as f:
        json.dump(json_data, f,ensure_ascii=False, indent = 4)


    print("Json file successfully created")


    #for saving the key value pair from the annotation of the template

    key_val_pair_json = makeKeyValPair(template_annotation_path)

    saved_annotation_file_path = os.path.join(final_template_dir, "key_val_pair.json")

    with open(saved_annotation_file_path, "w") as f:
        json.dump(key_val_pair_json, f, indent = 4)

    print("Key value pair json file created successfully")

    #cropping the images from the template with the help of bounding boxes 

    key_val_pair_json_path =saved_annotation_file_path
    template_image_path = template_path


    extractBoundingBox(key_val_pair_json_path, template_image_path)

    #storing the digitized key for future references
    print(lang)
    digitize(template_path,lang)
    print("Keys are digitized successfully and stored in a json file")


def main():
    parser = argparse.ArgumentParser(description="Preprocessing the templates")
    parser.add_argument("--template_path", required=True, help="Enter the template path")
    parser.add_argument("--template_annotation_path", required=True, help="Provide template annotation csv file path")

    args = parser.parse_args()

    temPreprocess(args.template_path, args.template_annotation_path)

if __name__ == "__main__":
    
    main()


