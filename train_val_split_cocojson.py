# Filemove.py will be followed by this
import os
import shutil
import json, tqdm

Origimg_dir ='original image path'
json_name = 'original cocojson path'
save_root = 'where to save'

Origjson_dir = os.path.join(Origimg_dir, json_name)
img_dir = os.path.join(save_root,"images")
json_dir = os.path.join(save_root,'annotations')

val_percentage = 20
extract_ratio = int(100/val_percentage)


train_img_dict,val_img_dict = [],[]
train_anno_dict,val_anno_dict = [],[]
objectNum_Cat_train, objectNum_Cat_val = [],[]


if not(os.path.isdir(img_dir)):
    os.makedirs(img_dir)

if not(os.path.isdir(json_dir)):
    os.makedirs(json_dir)

if not(os.path.isdir(os.path.join(img_dir,"val"))):
    os.makedirs(os.path.join(img_dir,"val"))

if not(os.path.isdir(os.path.join(img_dir,"train"))):
    os.makedirs(os.path.join(img_dir,"train"))



with open(Origjson_dir, 'r') as file_handle:
    lines = json.load(file_handle)
    lines2 = lines
    objectNum_Cat_train = [0]*len(lines["categories"])
    objectNum_Cat_val = [0]*len(lines["categories"])

    for img in tqdm.tqdm(lines["images"]):
        if img["id"] % extract_ratio == 0:  
            val_img_dict.append(img)
            shutil.copy(os.path.join(Origimg_dir,img["file_name"]),os.path.join(img_dir,"val"))

            for anno in lines["annotations"]:

                if img["id"] == anno["image_id"]:
                    val_anno_dict.append(anno)
                    objectNum_Cat_val[anno["category_id"] - 1] += 1
        else:
            train_img_dict.append(img)
            shutil.copy(os.path.join(Origimg_dir,img["file_name"]),os.path.join(img_dir,"train"))

            for anno in lines["annotations"]:
                if img["id"] == anno["image_id"]:
                    train_anno_dict.append(anno)
                    objectNum_Cat_train[anno["category_id"] - 1] += 1


    lines["images"] = val_img_dict
    lines["annotations"] = val_anno_dict

    json.dumps(lines)
    with open(os.path.join(json_dir,'val.json'), 'w') as f:
        json.dump(lines, f)

    lines2["images"] = train_img_dict
    lines2["annotations"] = train_anno_dict

    json.dumps(lines2)
    with open(os.path.join(json_dir, 'train.json'), 'w') as f:
        json.dump(lines2, f)

class_names = [cls['name'] for cls in lines["categories"]]
print("Train categories :\n",dict(zip(class_names,objectNum_Cat_train)))
print("validation categories : \n",dict(zip(class_names,objectNum_Cat_val)))