import os
import glob
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def xml_to_yolo(path):

    
    os.makedirs('XML_label', exist_ok=True)
    os.makedirs('YOLO_label', exist_ok=True)

    #Find every xml file
    for xml_file in glob.glob(path + '\*.xml'):

        tree = ET.parse(xml_file)
        root = tree.getroot()
           
        #get size from img file
        img_path = xml_file[:-4] + '.jpg'
        img = mpimg.imread(img_path)
        w, h = img.shape[:-1] 

        pedals = []
        for children in root.findall('object'):
            name = children[0].text
            bndbox = children[1]
            for child in children:
                if child.tag == 'bndbox': #bounding box tag
                    bndbox = child
            if name == 'کل ناحیه پلاک':
                xmin = float(bndbox[0].text)
                ymin = float(bndbox[1].text)
                xmax = float(bndbox[2].text)
                ymax = float(bndbox[3].text)

                x_center, y_center, width, height = convert(xmin, ymin, xmax, ymax, w, h)
                pedals.append(f'0 {x_center} {y_center} {width} {height}\n')
        
        xml_path = xml_file.replace(path, '')
        yolo_file_path = f'YOLO_label\{xml_path[:-4]}.txt'
        os.rename(xml_file, f'XML_label\{xml_path}')

        with open(yolo_file_path, 'w') as f:
            for p in pedals:
                f.write(p)


#Convert min/max data to yolo format
def convert(xmin, ymin, xmax, ymax, w, h):
    x_center = ((xmin + xmax) / 2) / w
    y_center = ((ymin + ymax) / 2) / w
    width = (xmax - xmin) / w
    height =(ymax - ymin) / h
    return [x_center, y_center, width, height]


#train test validation
images_path = "test"
xml_to_yolo(images_path)