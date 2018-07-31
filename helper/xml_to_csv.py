import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import sys

SPECIFIC_DIR = None
if len(sys.argv) > 1:
    SPECIFIC_DIR = sys.argv[1]

labels = []
def xml_to_csv(path, directory):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (os.path.join(directory, root.find('filename').text),
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
            if not member[0].text in labels:
                labels.append(member[0].text)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    if SPECIFIC_DIR:
        for directory in ['train','test']:
            image_path = os.path.join(SPECIFIC_DIR, directory)
            subdir = os.path.join(SPECIFIC_DIR, directory)
            xml_df = xml_to_csv(image_path, subdir)
            xml_df.to_csv('data/{}_labels.csv'.format(directory), index=None)
    print(labels)
    print('Successfully converted xml to csv.')


main()
