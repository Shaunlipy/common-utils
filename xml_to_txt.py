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
    print('Len img: {}, len xmls: {}'.format(len(imgs), len(xmls)))
    print('In xml not in imgs: ', _file_1)
    _file_2 = set(imgs) - set(_xmls)
    print('In imgs not in xmls: ', _file_2)

def visualize(xml):
    anno = ET.parse(xml)
    objs = anno.findall('object')
    img = cv2.imread(xml.replace('.xml', '.jpg'))
    for obj in objs:
        cat_name = obj.find('name').text.strip()
        bndbox_anno = obj.find('bndbox')
        xmin = int(bndbox_anno.find('xmin').text)
        ymin = int(bndbox_anno.find('ymin').text)
        xmax = int(bndbox_anno.find('xmax').text)
        ymax = int(bndbox_anno.find('ymax').text)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 6)
        cv2.putText(img, cat_name, (xmin, ymin), color=(255, 255, 255), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1)
    cv2.imshow(xml, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    save_dir = '/Volumes/CT500/Researches/Tooth_xray/yolov3'
    cur_dir = '/Volumes/CT500/Researches/Tooth_xray/yolov3/9-5-2020(Correct)'
    imgs = glob.glob(os.path.join(cur_dir, '*.jpg'))
    xmls = glob.glob(os.path.join(cur_dir, '*.xml'))

    # Check if each has corresponding file
    check_same_file(imgs, xmls)

    # Visualize
    visualize(xmls[10])
    # for i, xml in enumerate(xmls):
    #     process((xml, i))
    # for xml in xmls:
    #     process_old(xml)
