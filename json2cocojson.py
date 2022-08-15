import json
import os
import cv2
from cv2 import sort
from tqdm import tqdm
from PIL import Image


def yolo2coco(image_dir_path, label_dir_path, save_file_name, is_normalized):

    total = {}

    # make info
    info = {
        "description": "",
        "url": "",
        "version": "",
        "year": 2020,
        "contributor": "",
        "data_created": "2020-04-14 01:45:18.567988"
    }
    total["info"] = info

    # make licenses
    licenses_list = []
    licenses_0 = {
        "id": 1,
        "name": "your_name",
        "url": "your_name"
    }
    licenses_list.append(licenses_0)

    """ if you want to add licenses, copy this code
    licenses_1 = {
        "id": "2",
        "name": "your_name",
        "url": "your_name"
    }
    licenses_list.append(licenses_1)
    """

    total["licenses"] = licenses_list

    # make categories
    category_list = []
    class_0 = {
        "id":  1,
        "name": "ConcreteCrack",
        "supercategory": "category"
    }
    category_list.append(class_0)
    class_1 = {
        "id":  2,
        "name": "Spalling",
        "supercategory": "category"
    }
    category_list.append(class_1)
    class_2 = {
        "id":  3,
        "name": "Efflorescene",
        "supercategory": "category"
    }
    category_list.append(class_2)
    class_3 = {
        "id":  4,
        "name": "Exposure",
        "supercategory": "category"
    }
    category_list.append(class_3)
    class_4 = {
        "id":  5,
        "name": "SteelDefect",
        "supercategory": "category"
    }
    category_list.append(class_4)
    class_5 = {
        "id":  6,
        "name": "PaintDamage",
        "supercategory": "category"
    }
    category_list.append(class_5)

    """
    # if you want to add class
    class_1 = {
            "id":  2,
            "name" : "defect",
            "supercategory" : "None"
            }
    category_list.append(class_1)
    """

    total["categories"] = category_list

    # make yolo to coco format

    # get images
    image_list = os.listdir(image_dir_path)
    print("image length : ", len(image_list))
    label_list = os.listdir(label_dir_path)
    print("label length : ", len(label_list))

    image_dict_list = []
    count = 0
    for image_name in image_list:
        try:
            img = Image.open(image_dir_path+image_name)
            # img = cv2.imread(image_dir_path+image_name)
            image_dict = {
                "id": count,
                "file_name": image_name,
                "width": img.size[0],
                "height": img.size[1],
                "date_captured": "2020-04-14 -1:45:18.567975",
                "license": 1,  # put correct license
            }
            image_dict_list.append(image_dict)
            count += 1
        except:
            print(image_name)
    total["images"] = image_dict_list

    # make yolo annotation to coco format

    image_count = 0
    label_count = 0
    label_dict_list = []

    # for image_name in tqdm(image_list):
    for image_name in tqdm(total["images"]):
        image_id = image_name['id']
        image_name = image_name['file_name']
        img = Image.open(image_dir_path + image_name)
        with open(label_dir_path + image_name.split(".")[0] + ".json", "r") as file_handle:
            try:
                line = json.load(file_handle)
                bbox_dict_list = []
                segmentation_list_list = []

                # for l in line["annotations"]:
                for l in range(len(line["annotations"])):
                    box = [x for x in line["annotations"][l]["bbox"]]

                    top_left_x = box[0]
                    top_left_y = box[1]
                    box_width = box[2]
                    box_height = box[3]

                    bbox_dict = []
                    bbox_dict.append(top_left_x)
                    bbox_dict.append(top_left_y)
                    bbox_dict.append(box_width)
                    bbox_dict.append(box_height)
                    bbox_dict_list.append(bbox_dict)
                    # segmetation dict : 8 points to fill, x1,y1,x2,y2,x3,y3,x4,y4

                    segmentation_list = []
                    segmentation_list.append(bbox_dict[0])
                    segmentation_list.append(bbox_dict[1])
                    segmentation_list.append(bbox_dict[0] + bbox_dict[2])
                    segmentation_list.append(bbox_dict[1])
                    segmentation_list.append(bbox_dict[0]+bbox_dict[2])
                    segmentation_list.append(bbox_dict[1]+bbox_dict[3])
                    segmentation_list.append(bbox_dict[0])
                    segmentation_list.append(bbox_dict[1] + bbox_dict[3])
                    segmentation_list_list.append(segmentation_list)

                    if line["annotations"][l]["attributes"]['class'] == 'ConcreteCrack':
                        line["annotations"][l]['category_id'] = 1

                    elif line["annotations"][l]["attributes"]['class'] == 'Spalling':
                        line["annotations"][l]['category_id'] = 2

                    elif line["annotations"][l]["attributes"]['class'] == 'Efflorescene':
                        line["annotations"][l]['category_id'] = 3

                    elif line["annotations"][l]["attributes"]['class'] == 'Exposure':
                        line["annotations"][l]['category_id'] = 4

                    elif line["annotations"][l]["attributes"]['class'] == 'SteelDefect':
                        line["annotations"][l]['category_id'] = 5

                    elif line["annotations"][l]["attributes"]['class'] == 'PaintDamage':
                        line["annotations"][l]['category_id'] = 6

                    label_dict = {
                        "id": label_count,
                        "image_id": image_id,
                        "category_id": line["annotations"][l]['category_id'],
                        "iscrowd": 0,
                        "area": int(bbox_dict[2] * bbox_dict[3]),
                        "bbox": bbox_dict_list[l],
                        "segmentation": segmentation_list_list[l]
                    }
                    label_dict_list.append(label_dict)
                    label_count += 1
                image_count += 1
            except:
                pass
        total["annotations"] = label_dict_list
    # json.dumps(lines)

    with open(save_file_name, "w", encoding="utf-8") as make_file:
        json.dump(total, make_file, ensure_ascii=False, indent="\t")


if __name__ == "__main__":
    image_dir_path = "/mmdetection/data/train/image/"
    label_dir_path = "/mmdetection/data/train/json/"
    save_file_name = "/mmdetection/data/train/cocojson/train_new.json" 
    is_normalized = False
    # if you want to add more licenses or classes
    # add in code
    yolo2coco(image_dir_path, label_dir_path, save_file_name, is_normalized)