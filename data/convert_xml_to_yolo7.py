import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import numpy as np

# Function to combile train and validation files and remove validation folder
def combine_train_valid(path):

  source = path + 'validation'
  destination = path + 'train'

  # gather all files
  allfiles = os.listdir(source)

  # iterate on all files to move them to destination folder
  for f in allfiles:
    src_path = os.path.join(source, f)
    dst_path = os.path.join(destination, f)
    os.rename(src_path, dst_path)

  # delete empty validation folder
  os.rmdir(source)

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
def convert_to_yolov7(info_dict, ann, img):

  print_buffer = []
    
    # For each bounding box
  for b in info_dict["bboxes"]:
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
      #img = ann[:-3] + 'jpg'
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

#function to make desireable folders for image and labels
def makefolder(path):
  Paths=['train/images', 'train/labels', 'test/images', 'test/labels']
  for p in Paths:
    os.mkdir(path+p)

#function to move .jpg and .txt files to folders and remove .xml files
def movtofoldertrain(path):
  src = path + 'train'
  dest1 = path + 'train/images'
  dest2 = path + 'train/labels'
  allfiles = os.listdir(src)
  for f in allfiles:
    print(f)
    if f.endswith(".jpg"):
      src_path = os.path.join(src, f)
      dst_path = os.path.join(dest1, f)
      os.rename(src_path, dst_path)
    elif f.endswith(".txt"):
      src_path = os.path.join(src, f)
      dst_path = os.path.join(dest2, f)
      os.rename(src_path, dst_path)
    elif f.endswith(".xml"):
      src_path = os.path.join(src, f)
      os.remove(src_path)
    else:
      pass

#function to move .jpg and .txt files to folders and remove .xml files
def movtofoldertest(path):
  src = path + 'test'
  dest1 = path + 'test/images'
  dest2 = path + 'test/labels'
  allfiles = os.listdir(src)
  for f in allfiles:
    if f.endswith(".jpg"):
      src_path = os.path.join(src, f)
      dst_path = os.path.join(dest1, f)
      os.rename(src_path, dst_path)
    elif f.endswith(".txt"):
      src_path = os.path.join(src, f)
      dst_path = os.path.join(dest2, f)
      os.rename(src_path, dst_path)
    elif f.endswith(".xml"):
      src_path = os.path.join(src, f)
      os.remove(src_path)
    else:
      pass

#final function
#just insert car_plate folder path like this: path='/content/drive/MyDrive/car_plate/' 
def XMLtoYOLO(path):  
  combine_train_valid(path)
  makefolder(path)
  searchxml   = os.path.join( path , "*" , "*.xml" )
  xmlfiles = sorted(glob.glob( searchxml ))
  for xml in xmlfiles:
    ann = xml
    img = ann[:-3] + 'jpg'
    info_dict = extract_info_from_xml(ann)
    convert_to_yolov7(info_dict, ann, img)
  movtofoldertrain(path)
  movtofoldertest(path)
