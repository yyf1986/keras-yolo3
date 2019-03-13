#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
'''
Created on 2019年2月14日

@author: yaoyf
'''

import os
import xml.etree.ElementTree as ET

classes = ["chin"]


def convert_annotation(xmlfile):
    in_file = open(xmlfile)
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    imagepath = root.find("path").text

    classes_ret = []
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        classes_ret.append(",".join([str(a) for a in b]) + ',' + str(cls_id))
    
    in_file.close()
    return (imagepath + " " + " ".join(classes_ret))


if __name__ == '__main__':
    train_txt = open("train_chin.txt", "w")
    xml_path = "./images"
    for xmlfile in os.listdir(xml_path):
        if not xmlfile.endswith(".xml"):
            continue
        print(xmlfile)
        train_txt.write(convert_annotation(xml_path + os.sep + xmlfile)+"\n")
    train_txt.close()
