import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import re

import sys

SPECIFIC_DIR = 'final_data'
DICTIONARY_PATH = 'Company_names.csv'
if len(sys.argv) > 1:
    DICTIONARY_PATH = sys.argv[1]
else:
    print('please, insert dictionary path !')
    exit()

if os.path.exists(DICTIONARY_PATH):
    df = pd.read_csv(DICTIONARY_PATH)

latinRe = re.compile('[\da-zA-z-]{2,}')
labels = []

def getRomaji(japan_company_name):
    # print(df)
    try:
        return df.loc[df['Company'] == japan_company_name].Romaji.tolist()[0]
    except IndexError:
        return None

# print(Romaji("asdasdasdsa"))



def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            # if member[0].text.startswith('_'):
            #     member[0].text = member[0].text[1:]
            member[0].text = member[0].text.strip().replace(' ','_')
            if latinRe.search(member[0].text) and len(latinRe.search(member[0].text).group()) == len(member[0].text):
                if not member[0].text in labels:
                    labels.append(member[0].text)
                continue
            elif '_logo' in member[0].text:
               member[0].text = getRomaji(member[0].text.replace('_logo','')) + '_logo'
            elif getRomaji(member[0].text):
               member[0].text = getRomaji(member[0].text)
            else:
                print('Not found:',member[0].text)
            if not member[0].text in labels:
                labels.append(member[0].text)
        tree.write(xml_file)
    return True


def main():
    for directory in ['train','test']:
        images_path = os.path.join(SPECIFIC_DIR, directory)
        xml_df = xml_to_csv(images_path)
        
    print('####### LABELS ####### ')
    for label in labels:
        print(label)
    pbtxt_template = """item {
    id:%s
    name:'%s'
}"""
    pbtxt = ""
    for index, label in enumerate(labels):
         pbtxt += pbtxt_template % (str(index+1), str(label))
         if not index == len(labels) - 1:
            pbtxt += '\n\n'
    json_template = """
    {
        "id": %s,
        "label": "%s" 
    }"""
    json = """{
    "objects": [%s
    ]
}
    """
    json_body = ""
    for index, label in enumerate(labels):
        json_body += json_template % (str(index+1), label)
        if not index == len(labels) - 1:
            json_body += ','
    json = json % (json_body)

    if not os.path.exists('data'):
        os.makedirs('data')
    pbtxt_file = open('data/object-detection.pbtxt', 'w')
    pbtxt_file.write(pbtxt)
    pbtxt_file.close()

    json_file = open('data/objects.json', 'w')
    json_file.write(json)
    json_file.close()

        
    print('######################')
    print('Successfully converted xml to csv.')


if __name__ == '__main__':
    main()


