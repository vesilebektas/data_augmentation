import os
import cv2
from albumentations import HorizontalFlip
import xml.etree.ElementTree as ET

data_folder = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\data"
save_folder = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\horizontal"

# p = 1 her görüntünün yatay olarak çevrilmesi
horizontal_flip_transform = HorizontalFlip(p=1)

for filename in os.listdir(data_folder):
    #if filename.endswith(".jpg"):
    if filename.lower().endswith((".jpg", ".png")):
        image_path = os.path.join(data_folder, filename)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        augmented_image = horizontal_flip_transform(image=image)['image']

        save_path = os.path.join(save_folder, filename)

        label_filename = os.path.splitext(filename)[0] + ".xml"
        label_path = os.path.join(data_folder, label_filename)

        tree = ET.parse(label_path)
        root = tree.getroot()

        for obj in root.iter("object"):
            for box in obj.findall("bndbox"):
                xmin = int(box.find("xmin").text)
                xmax = int(box.find("xmax").text)

                new_xmin = image.shape[1] - xmax
                new_xmax = image.shape[1] - xmin

                box.find("xmin").text = str(new_xmin)
                box.find("xmax").text = str(new_xmax)

        new_label_path = os.path.join(save_folder, label_filename)
        tree.write(new_label_path)

        cv2.imwrite(save_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
