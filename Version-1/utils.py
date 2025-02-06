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
import string



#function for bakground removal

def backgroundRemoval(input_image_path, saved_masked_image_dir):
    input_image = cv2.imread(input_image_path)

    # form_name = os.path.dirname(input_image_path).split("/")[-1]
    if input_image.shape[1] >=2000 or input_image.shape[0] >= 2000:
        print(f"The width and height of the image is :{input_image.shape[1]},{input_image.shape[0]}")

        print("we need to resize")

        input_image = cv2.resize(input_image, (input_image.shape[1]//2, input_image.shape[0]//2))
        cv2.imwrite(input_image_path, input_image)

    os.makedirs(saved_masked_image_dir, exist_ok= True)
    # saved_masked_image_dir = os.path.join(saved_masked_image_dir, form_name)

    python_command_backremoval = f"python U-2-Net/u2net_test.py --input_image {input_image_path} --saved_output {saved_masked_image_dir}"

    subprocess.call(python_command_backremoval, shell = True)


#function for find contours
def detectMaxContour(input_image_path,saved_masked_image_dir):
    largest_contour = None
    max_area = 0
    input_image_name = os.path.basename(input_image_path).split(".")[0]
    masked_image_name = input_image_name + "_masked"+ ".png"
    masked_image_directory = os.path.join(saved_masked_image_dir, masked_image_name)
    print(masked_image_directory)


    masked_image = cv2.imread(masked_image_directory)
    masked_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    print(masked_image.shape)

    contours, _ = cv2.findContours(masked_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour

    return largest_contour

#function for getting corner points from the contour
def getCornerPoints(largest_contour):
    
    epsilon = 0.04 * cv2.arcLength(largest_contour, True)
    approx_polygon = cv2.approxPolyDP(largest_contour, epsilon, True)

    corner_points = approx_polygon.reshape(-1, 2)


    return corner_points

def createCombination(listPoints):
    combinations = []
    for i in range(len(listPoints)):
        combination = np.concatenate((listPoints[i:], listPoints[:i]), axis = 0)
        combinations.append(combination)

    return combinations



def modifyLine(bbox_text_file):
    with open(bbox_text_file, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

        new_lines = [item for item in lines if item]

    #write the modify lines to a new file
    with open(bbox_text_file, "w") as file:
        file.write("\n".join(new_lines))



def readfile(textfile):
    with open (textfile,"r") as file:
        lines = file.readlines()
        return lines



def checkDistance(pt1, pt2, mode):
  if mode == "y":
    if abs(pt2-pt1) <=15:
      return 1
    else:
      return 0
  elif mode == "x":
    if abs(pt2-pt1) <=300:
      return 1
    else:
      return 0
    


def checkDistanceHw(y1, y2, thresh):
    if y2- y1 <=thresh:
        return 1
    else:
        return 0
    

def sepMergeBox(bbox_single_line):
  # track_list = []
  final_single_line_boxes = {}
  count = 1
  for j in bbox_single_line:
    track_list = []
    boxes_list = bbox_single_line[j]

    for k in range(len(boxes_list)):
      if len(track_list) == 0:
        track_list.append(boxes_list[k])
      else:
        lst_box = track_list[-1]
        second_box = boxes_list[k]
        x_val1 = lst_box[2]
        x_val2 = second_box[0]

        if checkDistance(x_val1, x_val2, "x") == 1:
          track_list.append(second_box)

        else:
          final_single_line_boxes[count] = track_list
          track_list = []
          print("Seperated the box from a single line",count)
          count+=1
          track_list.append(second_box)
    final_single_line_boxes[count] = track_list
    print("Final Sperated and Merge Box", count)
    count += 1


  return final_single_line_boxes



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



def getBox(csv_file_path):
    with open (csv_file_path,"r")as file:
        reader = csv.reader(file)
        box_info = []
        for i, row in enumerate(reader):
            if i == 0:
                continue
            else:
                bounding_box = (int(row[1]),int(row[2]),int(row[3]),int(row[4]))
                box_info.append(bounding_box)
    return box_info


def getListBox(dict_boxes):
    boxes_coord = []
    for key , value in dict_boxes.items():
        single_line_boxes = dict_boxes[key]
        # print(single_line_boxes)
        

        for i in single_line_boxes:
            boxes_coord.append(i)
        


        # boxes_coord.append([for j in len(dict_boxes[key])])
    return boxes_coord



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

#Extraction of bounding boxes
def extractBoundingBox(bbox_json_path,image_path, mode = "key", isPlot = "No"):


    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()

    print(img.shape)

    

    with open(bbox_json_path, "r")as f:
        data = json.load(f)
    
    count_key = 1

    for i, bbox_data in data.items():
        # print(i)

        if mode == "key":
            
            info_bbox = bbox_data[0]



        

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

                    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)

            reader = easyocr.Reader(["en"], gpu = False)
        elif mode == "val":
            info_bbox = bbox_data[1]



            name_val = info_bbox[0]
            # print(name_val)
            temporary_folder = "temp"
            
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

                    cv2.rectangle(img_copy, (x,y), (x+w, y+h), (0,255,0),2)
            image_name = "form_with_plotted_bounding_box" + ".png"
            form_bbox_path = os.path.join(temporary_folder, image_name)
            cv2.imwrite(form_bbox_path, img_copy)




    # if isPlot  == "Yes":

    #     plt.figure(figsize = [20,10])
    #     plt.imshow(img_copy)
    #     plt.axis("off")


def Bleu4(gt, pred):
    bleu4_score = sentence_bleu([gt], pred, weights = (0.25,0.25, 0.25))

    return bleu4_score


def calBleu4(list_fields, single_word, score_hyperParam = 0.50):
    score = []
    count = 0

    for word in list_fields:
        bleu4_val = Bleu4(single_word, word)

        score.append(bleu4_val)

    if max(score)>= score_hyperParam:
        ind = score.index(max(score))
        count = 1

    else:
        ind = -1
        count = 0

    return ind, count


def jsonTolist(json_file):

    with open(json_file, "r")as f:
        json_data = json.load(f)

    #convert the json data to the desired list
    converted_list  = [(key, value) for key, value in json_data.items()]

    return converted_list



def getUniqueCharacter(character_list):
    character_list = [(term.lower(), values) for term , values in character_list]

    term_count = {}

    for term, _ in character_list:
        if term in term_count:
            term_count[term] += 1
        else:
            term_count[term] = 1

    character_list_unique = [(term, values) for term , values in character_list if term_count[term] == 1]
    return character_list_unique


def getMatchedPoints(ocred_output_template, ocred_output_form):
    digitized_form_output = [j[0].lower() for j in ocred_output_form]

    pt_aligned_form = []

    pt_template = []

    main_count = 0

    for i in ocred_output_template:
        min_ind, count = calBleu4(digitized_form_output, i[0])
        main_count += count
        if min_ind != 1:
            pt_template.append(i[1])
            pt_aligned_form.append(ocred_output_form[min_ind][1])

    return pt_template, pt_aligned_form, main_count



def convertPointFormat(listPoints):
    point_format = []
    for i in listPoints:
        for j in range(0, len(i),2):
            point_format.append((i[j], i[j+1]))

    return point_format



def getDigitizedList(img,bbox_list, ocr_reader):
    digitized_word_list = []

    for i in bbox_list:
        cropped_image = img[i[1]: i[5], i[0]: i[4]]
        result = ocr_reader.readtext(cropped_image)
        if len(result)!= 0:
            digitized_text = result[0][1]
            # print(digitized_text)
            digitized_word_list.append((digitized_text, i))

    return digitized_word_list  


def mergeKeyValPair(key_dict, val_dict):
    merged_dict = {}

    # Iterate through key dict and populate the merge dict
    for key, description in key_dict.items():
        # Check if description already present in the merge dict
        while description in merged_dict:
            # Append a random string to description
            random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
            description += f"_{random_string}"

        if key in val_dict:
            merged_dict[description] = val_dict[key]

    return merged_dict


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





