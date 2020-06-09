import glob
import os
from pathlib import Path
import shutil
import matplotlib.pyplot as plt
import cv2
import xml.etree.ElementTree as ET

def check_same_file(imgs, xmls):
    _xmls = list(map(lambda x: x.replace('.xml', '.jpg'), xmls))
    _file_1 = set(_xmls) - set(imgs)
    print('In xml not in imgs: ', _file_1)
    _file_2 = set(imgs) - set(_xmls)
    print('In imgs not in xmls: ', _file_2)

def visualize(xml, xmin, ymin, xmax, ymax):
    img = cv2.imread(xml.replace('.xml', '.jpg'))
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 6)
    plt.imshow(img)
    plt.show()

def crop(xml, xmin, ymin, xmax, ymax):
    img = cv2.imread(xml.replace('.xml', '.jpg'))
    img = img[ymin:ymax+1, xmin:xmax+1]
    # plt.imshow(img)
    # plt.show()
    cv2.imwrite(xml.replace('.xml', '.jpg').replace(parent_dir, new_parent), img)

def process(xml):
    file_idx = xml[1]
    anno = ET.parse(xml[0])
    width = int(anno.find('size').find('width').text)
    height = int(anno.find('size').find('height').text)
    bbox = ''
    # 28039541-10-09-1979-23-11-2019-f
    obj = anno.findall('object')
    assert len(obj) == 1
    cat_name = obj[0].find('name').text.strip()
    obj_id = cat_name.split('-')[0]
    bndbox_anno = obj[0].find('bndbox')
    xmin = int(bndbox_anno.find('xmin').text)
    ymin = int(bndbox_anno.find('ymin').text)
    xmax = int(bndbox_anno.find('xmax').text)
    ymax = int(bndbox_anno.find('ymax').text)
    # visualize(xml[0], xmin, ymin, xmax, ymax)
    w = (xmax - xmin) * 1.0 / width
    h = (ymax - ymin) * 1.0 / height
    x_cen = (xmax + xmin) * 1.0 / (2 * width)
    y_cen = (ymax + ymin) * 1.0 / (2 * height)
    bbox += '{} {} {} {} {} \n'.format(0, str(x_cen), str(y_cen), str(w), str(h))
    with open(os.path.join(Path(xml[0]).parent.parent, 'txts', '{}_{}.txt'.format(obj_id, file_idx)), 'w') as f:
        f.write(bbox)
    shutil.copy(xml[0].replace('.xml', '.jpg'), os.path.join(Path(xml[0]).parent.parent, 'imgs', '{}_{}.jpg'.format(obj_id, file_idx)))

def process_old(xml):
    anno = ET.parse(xml)
    width = int(anno.find('size').find('width').text)
    height = int(anno.find('size').find('height').text)
    bbox = ''
    obj = anno.findall('object')
    assert len(obj) == 1
    cat_name = obj[0].find('name').text.strip()
    bndbox_anno = obj[0].find('bndbox')
    xmin = int(bndbox_anno.find('xmin').text)
    ymin = int(bndbox_anno.find('ymin').text)
    xmax = int(bndbox_anno.find('xmax').text)
    ymax = int(bndbox_anno.find('ymax').text)
    crop(xml, xmin, ymin, xmax, ymax)

if __name__ == '__main__':
    new_parent = 'test_1_f'
    root = '/Volumes/INTEL/Tooth_xray/wetransfer-orig-F-1'
    parent_dir = Path(root).name
    imgs = glob.glob(os.path.join(root, '*.jpg'))
    xmls = glob.glob(os.path.join(root, '*.xml'))
    print(xmls[0])
    # check_same_file(imgs, xmls)
    # SILVANEIDE DE SOUZA ROMÃO.xml missing
    # for i, xml in enumerate(xmls):
    #     process((xml, i))
    for xml in xmls:
        process_old(xml)
