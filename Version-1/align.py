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
import utils


#get the version-1 alignment image of the form
def getAlignVerOne(template_image_path, input_image_path, corner_points, saved_alignedv1_image_dir):

    template_image = cv2.imread(template_image_path)
    captured_image = cv2.imread(input_image_path)
    captured_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)


    template_image_top_left = (0,0)
    template_image_bottom_left = (0, template_image.shape[0])
    template_image_bottom_right = (template_image.shape[1], template_image.shape[0])

 
    template_image_top_right = (template_image.shape[1], 0)




    pts1_new = np.array([template_image_top_left,template_image_bottom_left, template_image_bottom_right, template_image_top_right])
    pts2_new = corner_points

    h, mask = cv2.findHomography(pts2_new, pts1_new, cv2.RANSAC)

    captured_image_warped = cv2.warpPerspective(captured_image, h, (template_image.shape[1], template_image.shape[0]))


    # plt.figure(figsize= [20,10])
    # plt.imshow(captured_image_warped)

    # plt.axis("off")

    os.makedirs(saved_alignedv1_image_dir, exist_ok = True)

    image_name = os.path.basename(input_image_path).split(".")[0]

    aligned_image_name = image_name + "_alignedV1" + ".png"

    cv2.imwrite(os.path.join(saved_alignedv1_image_dir, aligned_image_name),captured_image_warped)

    return os.path.join(saved_alignedv1_image_dir,aligned_image_name)
    

#get the final aligned image
def finalAlign(aligned_imageStage1_path, template_path,pt_template, pt_form,saved_final_aligned_image_path = "aligned_images",craft_model_path =  "CRAFT-pytorch/text_detection_model/craft_mlt_25k.pth"):
    aligned_imageStage1 = cv2.imread(aligned_imageStage1_path)
    aligned_imageStage1 = cv2.cvtColor(aligned_imageStage1, cv2.COLOR_BGR2RGB)

    version_1_dirname = "aligned_version1"
    
    version_1_imageBasename = os.path.basename(aligned_imageStage1_path).split(".")[0]


    pt_four_point_format_template = utils.convertPointFormat(pt_template)
    pt_four_point_format_alignedV1 = utils.convertPointFormat(pt_form)


    #converting point to np.array format

    pts1_new = np.array(pt_four_point_format_template)
    pts2_new = np.array(pt_four_point_format_alignedV1)

    new_h, mask = cv2.findHomography(pts2_new, pts1_new, cv2.RANSAC)

    #reading the template image
    template_image = cv2.imread(template_path)
    template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2RGB)

    final_aligned_image = cv2.warpPerspective(aligned_imageStage1, new_h, (template_image.shape[1], template_image.shape[0]))

    final_aligned_image_name = version_1_imageBasename + "_final.png"
    cv2.imwrite(os.path.join(saved_final_aligned_image_path, final_aligned_image_name), final_aligned_image)

    return os.path.join(saved_final_aligned_image_path, final_aligned_image_name)



#function for checing the right aligned image with respect to the template

def getCheckAlign(template_image_path, input_image_path, list_corner_points, saved_aligned_imagev1_dir, saved_aligned_image_dir):
    
    flag = 0
    for i in range(len(list_corner_points)):
        aligned_imagev1_path = getAlignVerOne(template_image_path, input_image_path, list_corner_points[i], saved_aligned_imagev1_dir)
        
        aligned_imageStage1 = cv2.imread(aligned_imagev1_path)
        aligned_imageStage1 = cv2.cvtColor(aligned_imageStage1, cv2.COLOR_BGR2RGB)        


        version_1_dirname = saved_aligned_imagev1_dir
    
        version_1_imageBasename = os.path.basename(aligned_imagev1_path).split(".")[0]

        craft_saved_result_dir = os.path.join(version_1_dirname, version_1_imageBasename)
        print(craft_saved_result_dir)
        
        os.makedirs(craft_saved_result_dir, exist_ok= True)
    

        #To run the craft model for detecting the contents of the form
        #CRAFT model path for inference
        # crafted_output = 
        craft_model_path = "CRAFT-pytorch/text_detection_model/craft_mlt_25k.pth"
        python_command_CRAFT = f"python CRAFT-pytorch/test.py --trained_model {craft_model_path} --test_folder {version_1_dirname} --saved_result {craft_saved_result_dir}"
        subprocess.call(python_command_CRAFT, shell = True)

        detected_bounding_box_subpath = "res"+ "_" + version_1_imageBasename + ".txt"

        detected_bounding_box_fullpath = os.path.join(craft_saved_result_dir, detected_bounding_box_subpath)

        utils.modifyLine(detected_bounding_box_fullpath)

        lines_bbox_aligned_image =utils.readfile(detected_bounding_box_fullpath)
        dict_roi_bbox_aligned_image = utils.mergeBoundingBoxHw(lines_bbox_aligned_image)
        list_aligned_image_boxes = utils.getListBox(dict_roi_bbox_aligned_image)

        #initialize the easy ocr reader object
        reader = easyocr.Reader(["en"], gpu = True)

        Ocred_output_form = utils.getDigitizedList(aligned_imageStage1, list_aligned_image_boxes, reader)

        #get the template image name
        template_image_name = os.path.basename(template_image_path).split(".")[0]
        template_info_dir = os.path.join("form_template_info",template_image_name)

        #get the ocred output 

        template_json_file_path = os.path.join(template_info_dir,"ocred.json")
        template_ocred_list = utils.jsonTolist(template_json_file_path)

        #Delete the duplicate characters from the template ocred output
        template_unique_ocred_list = utils.getUniqueCharacter(template_ocred_list)

        #calling the content matching function for getting the matched points
        pt_template, pt_form, number_of_matches = utils.getMatchedPoints(template_unique_ocred_list, Ocred_output_form)
        print(number_of_matches)

        if number_of_matches >= 20:
            aligned_image_path = finalAlign(aligned_imagev1_path,template_image_path ,pt_template, pt_form, saved_aligned_image_dir)
            flag = 1
            print("Sufficient matches are founded")
            return aligned_image_path

    # if flag ==1:
    #     print("Sufficient matches are founded")
    if flag == 0:
        print("Sufficient matches not found")
        print("Please take the clear picture and upload again")







    







