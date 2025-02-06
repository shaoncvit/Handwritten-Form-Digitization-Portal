import utils 
import cv2


final_alinged_image_path = "aligned_images/16_alignedV1_final.png"

# alinged_image = cv2.imread(final_alinged_image_path)


bbox_json_path = "form_template_info/template_1/key_val_pair.json"

utils.extractBoundingBox(bbox_json_path, final_alinged_image_path, mode = "val", isPlot = "Yes")








