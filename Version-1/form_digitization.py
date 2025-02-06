import cv2
# import matplotlib.pyplot as plt
import numpy as np
import csv
import easyocr
from nltk.translate.bleu_score import sentence_bleu
import os
import subprocess
import json
import torch


class FormDigitization:

    def __init__(self):
        self.saved_masked_image_dir = "masked_output"
        self.dir_align_image = "aligned_images"
        self.dir_template_image_info = "form_template_info"
        self.final_result_directory = "result"

#function for remove the background
    def backgroundRemoval(self, input_image_path,saved_masked_image_dir):
        input_image = cv2.imread(input_image_path)
        if input_image.shape[1] >= 2000 or input_image.shape[0]>= 2000:
            print(f"The width and height of the image is :{input_image.shape[1]},{input_image.shape[0]}")
            print("We need to resize")
            input_image = cv2.resize(input_image, (input_image.shape[1]//2, input_image.shape[0]//2))
            cv2.imwrite(input_image_path, input_image)
        # dir_masked_image = "masked_output"
        #remove the background
        self.backgroundRemoval(input_image_path, self.saved_masked_image_dir)
        python_command_backremoval = f"python U-2-Net/u2net_test.py --input_image {input_image_path} --saved_output {saved_masked_image_dir}"

        subprocess.call(python_command_backremoval, shell = True)

    

# backgroundRemoval("uploads/school_form.jpg", "masked_output")

#function for detect the contour
    def detectMaxContour(self, input_image_path,saved_masked_image_dir):
        largest_contour = None
        max_area = 0
        input_image_name = os.path.basename(input_image_path).split(".")[0]
        masked_image_name = input_image_name + "_masked"+ ".png"
        masked_image_directory = os.path.join(self.saved_masked_image_dir, masked_image_name)
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

    

#function for getting four points from the contour
    def getCornerPoints(self, largest_contour):
        epsilon = 0.04 * cv2.arcLength(largest_contour, True)
        approx_polygon = cv2.approxPolyDP(largest_contour, epsilon, True)

        corner_points = approx_polygon.reshape(-1,2)

        return corner_points

#function for make four combination of corner points
    def createCombination(self, listPoints):
        combinations = []
        for i in range(len(listPoints)):
            combination = np.concatenate((listPoints[i:], listPoints[:i]), axis = 0)
            combinations.append(combination)

        return combinations

#function for first stage alignment
    def getFirstAlign(self, template_image_path, input_image_path, corner_point):
        template_image = cv2.imread(template_image_path)
        captured_image = cv2.imread(input_image_path)
        captured_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)

        template_image_top_left = (0,0)
        template_image_bottom_left = (0, template_image.shape[0])
        template_image_bottom_right = (template_image.shape[1], template_image.shape[0])
        template_image_top_right = (template_image.shape[1], 0)

        pts1 = np.array([template_image_top_left, template_image_bottom_left, template_image_bottom_right, template_image_top_right])

        pts2 = corner_point

        print(pts2)
        h, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC)

        captured_image_warped = cv2.warpPerspective(captured_image, h, (template_image.shape[1], template_image.shape[0]))

        return captured_image_warped

#function for reading the file of the crafted output
    def readfile(self, textfile):
        with open(textfile, "r")as file:
            lines = file.readlines()
            return lines
    
#function for check distances between two bounding boxes
    def checkDistance(self,pt1, pt2, mode):
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
    
#function for check distance between two bounding boxes for hw region
    def checkDistanceHw(self,y1, y2, thresh):
        if y2- y1 <=thresh:
            return 1
        else:
            return 0

#function for merging the bounding boxes    

    def mergeBoundingBoxHw(self,list_bounding_box):
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


            if self.checkDistanceHw(points1_y, points2_y, 20) == 1:
                y_coordinates_pt.append(points2_y)
                mergeBox.append(four_points2)
                # print(mergeBox)

            elif self.checkDistanceHw(points1_y, points2_y, 20) == 0:
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

#function for make a list of boxes which are on the same axis
    def getListBox(self, dict_boxes):
        boxes_coord = []
        for key , value in dict_boxes.items():
            single_line_boxes = dict_boxes[key]
            # print(single_line_boxes)
            

            for i in single_line_boxes:
                boxes_coord.append(i)
        


        # boxes_coord.append([for j in len(dict_boxes[key])])
        return boxes_coord

#function for getting the digitized list
    def getDigitizedList(self, img,bbox_list, ocr_reader):
        digitized_word_list = []

        for i in bbox_list:
            cropped_image = img[i[1]: i[5], i[0]: i[4]]
            result = ocr_reader.readtext(cropped_image)
            if len(result)!= 0:
                digitized_text = result[0][1]
                # print(digitized_text)
                digitized_word_list.append((digitized_text, i))

        return digitized_word_list  

#function for get the boxes from the csv file
    def getBox(self, csv_file_path):
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

#function for modify the line
    def modifyLine(self, bbox_text_file):
        with open (bbox_text_file,"r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            new_lines = [item for item in lines if item]

        #write the modified lines to a new file
        with open(bbox_text_file, "w") as file:
            file.write("\n".join(new_lines))

#function for calculating the blue score
    def Bleu4(self, gt, pred):
        bleu4_score = sentence_bleu([gt], pred, weights=(0.25,0.25,0.25,0.25))
        return bleu4_score

    def calBleu4(self,list_fields, single_word, score_hyperParam = 0.50):
        score = []
        count = 0

        for word in list_fields:
            bleu4_val = self.Bleu4(single_word, word)
            score.append(bleu4_val)
        
        if max(score) >= score_hyperParam:
            ind = score.index(max(score))
            count = 1

        else:
            ind = -1
            count = 0

        return ind, count

#function for filtering the unique character from the character list
    def getUniqueCharacter(self,character_list):
        character_list = [(term.lower(), values) for term , values in character_list]
        term_count = {}

        for term, _ in character_list:
            if term in term_count:
                term_count[term] += 1
            else:
                term_count[term] = 1

        character_list_unique = [(term, values) for term, values in character_list if term_count[term] ==1]

        return character_list_unique 

#function for getting content matching point
    def getMatchedPoints(self,ocred_output_template, ocred_output_form):
        digitized_form_output = [j[0].lower() for j in ocred_output_form]

        pt_aligned_form = []
        pt_template = []

        main_count = 0

        for i in ocred_output_template:
            min_ind, count = self.calBleu4(digitized_form_output, i[0])
            main_count += count

            if min_ind != -1:
                pt_template.append(i[1])
                pt_aligned_form.append(ocred_output_form[min_ind][1])

        print(f"Total Number of correct match:{main_count}")
        return pt_template,pt_aligned_form, main_count

#function for read the template json
    def jsonTolist(self,json_file):

        with open(json_file, "r") as f:
            json_data = json.load(f)

        #convert the json data back to the desired list
        converted_list = [(key, value) for key, value in json_data.items()]

        return converted_list


#function for convert the list of points in (x,y) format
    def convertPointFormat(self, listPoints):
        point_format = []
        for i in listPoints:
            for j in range(0, len(i),2):
                point_format.append((i[j], i[j+1]))

        return point_format


#function for final stage of alignment
    def finalAlign(self,points_template, points_form, dir_align_image, input_image_path, template_image_path):
        
        template_image = cv2.imread(template_image_path)
        pt_four_point_format_template = self.convertPointFormat(points_template)
        pt_four_point_format_aligned_form = self.convertPointFormat(points_form)

        first_stage_aligned_image_path = dir_align_image +"/"+ os.path.basename(input_image_path).split(".")[0]+ "_aligned.png"

        first_stage_aligned_image = cv2.imread(first_stage_aligned_image_path)
        first_stage_aligned_image = cv2.cvtColor(first_stage_aligned_image, cv2.COLOR_BGR2RGB)

        pts1_new = np.array(pt_four_point_format_template)
        pts2_new = np.array(pt_four_point_format_aligned_form)

        new_h, mask = cv2.findHomography(pts2_new, pts1_new, cv2.RANSAC)

        final_aligned_image = cv2.warpPerspective(first_stage_aligned_image, new_h, (template_image.shape[1], template_image.shape[0]))

        cv2.imwrite(first_stage_aligned_image_path, final_aligned_image)


#function for choose the correct aligned version
    def getCheckAlign(self, template_image_path, input_image_path, list_corner_points, saved_aligned_image_dir):
        
        flag = 0
        for i in range(len(list_corner_points)):
            aligned_image = self.getFirstAlign(template_image_path, input_image_path, list_corner_points[i])
            
            os.makedirs(saved_aligned_image_dir, exist_ok = True)
            image_name = os.path.basename(input_image_path).split(".")[0] + "_aligned" + ".png"
            saved_folder_path = os.path.join(saved_aligned_image_dir, image_name)

            # print(saved_folder_path)

            cv2.imwrite(saved_folder_path, aligned_image)

            #To run the craft model for detecting the contents of the form
            #CRAFT model path for inference
            # crafted_output = 
            craft_model_path = "CRAFT-pytorch/text_detection_model/craft_mlt_25k.pth"
            python_command_CRAFT = f"python CRAFT-pytorch/test.py --trained_model {craft_model_path} --test_folder {saved_aligned_image_dir} --saved_result {saved_aligned_image_dir}"
            subprocess.call(python_command_CRAFT, shell = True)

            detected_box_path = "res_"+os.path.basename(saved_folder_path).split(".")[0] + ".txt"

            aligned_image_crafted_boxes_path = os.path.join(saved_aligned_image_dir,detected_box_path)

            self.modifyLine(aligned_image_crafted_boxes_path)

            lines_bbox_aligned_image =self.readfile(aligned_image_crafted_boxes_path)
            dict_roi_bbox_aligned_image = self.mergeBoundingBoxHw(lines_bbox_aligned_image)
            list_aligned_image_boxes = self.getListBox(dict_roi_bbox_aligned_image)

            #initialize the easy ocr reader object
            reader = easyocr.Reader(["en"], gpu = True)

            Ocred_output_form = self.getDigitizedList(aligned_image, list_aligned_image_boxes, reader)

            #get the template image name
            template_image_name = os.path.basename(template_image_path).split(".")[0]
            template_info_dir = os.path.join("form_template_info",template_image_name)

            #get the ocred output 

            template_json_file_path = os.path.join(template_info_dir,"ocred.json")
            template_ocred_list = self.jsonTolist(template_json_file_path)

            #Delete the duplicate characters from the template ocred output
            template_unique_ocred_list = self.getUniqueCharacter(template_ocred_list)

            #calling the content matching function for getting the matched points
            pt_template, pt_form, number_of_matches = self.getMatchedPoints(template_unique_ocred_list, Ocred_output_form)

            if number_of_matches >= 20:
                self.finalAlign(pt_template, pt_form, saved_aligned_image_dir,input_image_path, template_image_path )
                flag = 1
                print("Sufficient matches are founded")
                return

        # if flag ==1:
        #     print("Sufficient matches are founded")
        if flag == 0:
            print("Sufficient matches not found")
            print("Please take the clear picture and upload again")
    

#function for OCR
    def ocr(self, img_path, ocr_type = "easy_ocr", lang = "en", text_type = "key"):
        if ocr_type == "easy_ocr" and text_type == "key":
            reader = easyocr.Reader(["en"], gpu =True)
            ocr_result = reader.readtext(img_path)

        elif ocr_type == "easy_ocr" and text_type == "val":
            reader = easyocr.Reader([lang], gpu = True)
            ocr_result = reader.readtext(img_path)

        return ocr_result

#function for detect and digitizing the detected text 
    def detectAndDigitize(self,image_path,box_path,text_type = "key", ocr_lang = "en"):

        ocr_text = []
        count = 0

        # first_stage_aligned_image_path = dir_align_image +"/"+ os.path.basename(input_image_path).split(".")[0]+ "_aligned.png"

        aligned_image = cv2.imread(image_path)
        aligned_image = cv2.cvtColor(aligned_image, cv2.COLOR_BGR2RGB)


        os.makedirs(os.path.join("temp", os.path.basename(image_path).split(".")[0]), exist_ok=True)

        
        
        with open(box_path, mode = "r") as file:
            next(file)

            csvfile = csv.reader(file)

            for lines in csvfile:
                x = int(lines[1])
                y = int(lines[2])
                w = int(lines[3])
                h = int(lines[4])

                if w and h != 0:
                    


                    single_image = aligned_image[y: y+h, x: x+w]

                    extract_image_name = str(count)+ ".png"

                    extracted_image_directory = os.path.join("temp", os.path.basename(image_path).split(".")[0])
                    extracted_image_path = os.path.join(extracted_image_directory, extract_image_name)

                    cv2.imwrite(extracted_image_path, single_image)

                    result_ocred = self.ocr(extracted_image_path,lang = ocr_lang,text_type=text_type)

                    merge_text = ""

                    for i in range (len(result_ocred)):
                        info_ocr = result_ocred[i]
                        text  = info_ocr[1]
                        merge_text += text +" "

                    ocr_text.append(merge_text)

                count +=1

        # print(ocr_text)
            # print(count)
        return ocr_text


#function for creating a output textfile
    def createTextFile(self, template_output, form_output, filename):
        with open(filename, "w")as f:
            for key , value in zip(template_output, form_output):
                f.write(f"{key} => {value}\n")

        print(f"key value pair have been written to {filename}.")

#final function for form digitization
    def run(self,template_image_path, input_image_path, ocr_lang):
        # dir_masked_image = "masked_output"
        #remove the background
        self.backgroundRemoval(input_image_path, self.saved_masked_image_dir)

        #detect the largest contour
        biggest_contour = self.detectMaxContour(input_image_path, self.saved_masked_image_dir)
        #get the four corner points from the largest contour
        corner_points = self.getCornerPoints(biggest_contour)
        #get the four combinations of the corner points
        list_corner_point = self.createCombination(corner_points)

        # #directory for the align image
        # dir_align_image = "aligned_images"

        # #directory for the template image information
        # dir_template_image_info = "form_template_info"

        #check the corrected aligned image
        self.getCheckAlign(template_image_path, input_image_path,list_corner_point,self.dir_align_image)

        final_aligned_image_path = os.path.join(self.dir_align_image, os.path.basename(input_image_path).split(".")[0] + "_aligned.png")
        key_annotation_basnemae = os.path.join(os.path.basename(template_image_path).split(".")[0], "key_annotation.csv")
        key_annotation_path = os.path.join(self.dir_template_image_info, key_annotation_basnemae)
        template_ocred_text = self.detectAndDigitize(template_image_path, key_annotation_path, text_type="key")
        value_annotation_basname = os.path.join(os.path.basename(template_image_path).split(".")[0], "annotation.csv")
        value_annotation_path = os.path.join(self.dir_template_image_info, value_annotation_basname)
        alignedForm_image_ocred_text = self.detectAndDigitize(final_aligned_image_path, value_annotation_path, text_type="val")
        final_result_basename = os.path.basename(input_image_path).split(".")[0] + ".txt"
        final_result_path = os.path.join(self.final_result_directory, final_result_basename)
        self.createTextFile(template_ocred_text, alignedForm_image_ocred_text, final_result_path)
        
        return template_ocred_text, alignedForm_image_ocred_text
        

# if __name__ == '__main__':
#     formDigitization = FormDigitization()
#     template_image_path = "form_templates/Form27.png"
#     input_image_path = "uploads/school_form.jpg"
#     formDigitization.run(template_image_path, input_image_path)