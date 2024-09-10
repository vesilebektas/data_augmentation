import os
import cv2
from albumentations import Rotate
import xml.etree.ElementTree as ET
import albumentations
import numpy as np

data_folder = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\data"
save_folder = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\rotate"

transform = albumentations.Rotate(limit=90,
                                  interpolation=cv2.INTER_LINEAR,
                                  border_mode=cv2.BORDER_CONSTANT,  #döndürme sonrasında oluşan boşlukları doldurmak için kullanılır
                                  value=0,  #border_mode, BORDER_CONSTANT seçilmişse kullanılır value=0 demek siyah arkaplan oluşturur
                                  p=1)

for filename in os.listdir(data_folder):
    if filename.endswith(".jpg"):
        image_path = os.path.join(data_folder, filename)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        transformed_image = transform(image=np.array(image))['image']

        save_path = os.path.join(save_folder, filename)

        label_filename = os.path.splitext(filename)[0] + ".xml"
        label_path = os.path.join(data_folder, label_filename)

        tree = ET.parse(label_path)
        root = tree.getroot()

        for obj in root.iter("object"):
            for box in obj.findall("bndbox"):
                xmin = int(box.find("xmin").text)
                ymin = int(box.find("ymin").text)
                xmax = int(box.find("xmax").text)
                ymax = int(box.find("ymax").text)

                old_width = xmax - xmin
                old_height = ymax - ymin

                new_xmin = image.shape[1] - ymax
                new_ymin = xmin
                new_xmax = new_xmin + old_height
                new_ymax = new_ymin + old_width

                box.find("xmin").text = str(new_xmin)
                box.find("ymin").text = str(new_ymin)
                box.find("xmax").text = str(new_xmax)
                box.find("ymax").text = str(new_ymax)

        new_label_path = os.path.join(save_folder, label_filename)
        tree.write(new_label_path)

        cv2.imwrite(save_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
