import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import numpy as np

# Function to get the data from XML Annotation
def extract_info_from_xml(xml_file):
    root = ET.parse(xml_file).getroot()
    
    # Initialise the info dict 
    info_dict = {}
    info_dict['bboxes'] = []

    # Parse the XML Tree
    for elem in root:
              
        # Get details of the bounding box 
        if elem.tag == "object":
          bbox = {}
          for subelem in elem:
              if subelem.tag == "name":
                  bbox["class"] = subelem.text
                    
              elif subelem.tag == "bndbox":
                  for subsubelem in subelem:
                       bbox[subsubelem.tag] = int(subsubelem.text)            
          info_dict['bboxes'].append(bbox)
    
    return info_dict


# Dictionary that maps class names to IDs
class_name_to_id_mapping = {"کل ناحیه پلاک": 0}


# Convert the info dict to the required yolo format and write it to disk
def convert_to_yolov7(info_dict):

  print_buffer = []
    
    # For each bounding box
  for b in info["bboxes"]:
    if b['class'] == 'کل ناحیه پلاک':
      try:
          class_id = class_name_to_id_mapping[b["class"]]
      except KeyError:
          print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
          
          # Transform the bbox co-ordinates as per the format required by YOLO v7
      b_center_x = (b["xmin"] + b["xmax"]) / 2 
      b_center_y = (b["ymin"] + b["ymax"]) / 2
      b_width    = (b["xmax"] - b["xmin"])
      b_height   = (b["ymax"] - b["ymin"])
        
        # Normalise the co-ordinates by the dimensions of the image
      im=plt.imread(img)
      image_h, image_w, image_c = im.shape
      b_center_x /= image_w 
      b_center_y /= image_h 
      b_width    /= image_w 
      b_height   /= image_h 
        
        #Write the bbox details to the file 
      print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
  save_file_name = ann[:-3] + 'txt'
  print("\n".join(print_buffer), file= open(save_file_name, "w"))        
