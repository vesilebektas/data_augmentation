import os
import cv2
from albumentations import VerticalFlip
import xml.etree.ElementTree as ET
from lxml import etree

data_folder = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\data"
save_folder = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\vertical"

# p = 1 her görüntünün dikey olarak çevrilmesi
vertical_flip_transform = VerticalFlip(p=1)
for filename in os.listdir(data_folder):
    if filename.lower().endswith((".jpg", ".png")):

    #if filename.endswith(".jpg"):
        image_path = os.path.join(data_folder, filename)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        augmented_image = vertical_flip_transform(image=image)['image']

        save_path = os.path.join(save_folder, filename)

        label_filename = os.path.splitext(filename)[0] + ".xml"
        label_path = os.path.join(data_folder, label_filename)

        tree = ET.parse(label_path)
        root = tree.getroot()

        # koordinat değiştirme işlemi
        for obj in root.findall(".//object"):
            for box in obj.findall("bndbox"):
                ymin = int(box.find("ymin").text)
                ymax = int(box.find("ymax").text)

            new_ymin = image.shape[0] - ymax
            new_ymax = image.shape[0] - ymin

            box.find("ymin").text = str(new_ymin)
            box.find("ymax").text = str(new_ymax)

        new_label_path = os.path.join(save_folder, label_filename)
        tree.write(new_label_path)

        cv2.imwrite(save_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
