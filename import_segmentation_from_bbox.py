import json


json_opendir = "/home/user/Downloads/Construct.AI.v2.BB.v1i.coco/valid/_annotations.coco.json"
json_savedir = '/home/user/Downloads/Construct.AI.v2.BB.v1i.coco/modify_val.json'


with open(json_opendir, 'r') as file_handle:
    lines = json.load(file_handle)
# make annotations
    for l in lines["annotations"]:
        xmin, ymin, width, height = l["bbox"]
        # bbox x1,y1 is top left, x2,y3 is down right
        # segmetation dict : 8 points to fill, x1,y1,x2,y2,x3,y3,x4,y4
        segmentation_list_list = []
        segmentation_list = []
        segmentation_list.append(xmin)
        segmentation_list.append(ymin)
        segmentation_list.append(xmin + width)
        segmentation_list.append(ymin)
        segmentation_list.append(xmin + width)
        segmentation_list.append(ymin + height)
        segmentation_list.append(xmin)
        segmentation_list.append(ymin + height)
        l["segmentation"] = [segmentation_list]
        
    json.dumps(lines)

with open(json_savedir, 'w') as f:
    json.dump(lines,f)