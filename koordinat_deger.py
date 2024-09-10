# xml dosyalarında bulunan x ve y değerlerinin durumuna bakıyor

import os
import xml.etree.ElementTree as ET


def check_xml_values(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    x_value = None
    y_value = None

    bndbox_element = root.find(".//object/bndbox")

    if bndbox_element is not None:
        x_value = float(bndbox_element.find('xmin').text)
        y_value = float(bndbox_element.find('ymin').text)

    if x_value is not None and y_value is not None:
        if x_value < 0 or y_value < 0:
            print(f"XML dosyası: {xml_file}, x veya y değeri 0'ın altında.")
        else:
            print(f"XML dosyası: {xml_file}, Pozitif değerler.")
    else:
        print(f"XML dosyası: {xml_file}, x veya y değerleri bulunamadı.")


def check_folder_for_xml(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(folder_path, filename)
            check_xml_values(xml_file_path)


klasor_yolu = "C:\\Users\\bekta\\PycharmProjects\\dataAugmentation\\horizontal"
check_folder_for_xml(klasor_yolu)
