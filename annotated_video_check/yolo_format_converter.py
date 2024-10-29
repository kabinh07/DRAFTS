import json
import os
from PIL import Image, ImageDraw
from tqdm import tqdm

map_label = {
    'truck': 0.0,
    'car': 1.0
}

def normalize_bbox(x, y, width, height, original_width, original_height):
    x_center = x / 100.0 * original_width
    y_center = y / 100.0 * original_height
    width = width / 100.0 * original_width
    height = height / 100.0 * original_height
    return x_center, y_center, width, height

with open('project-1-at-2024-10-16-05-54-b3e1f710.json', 'r') as f:
    annotations = json.load(f)

images = os.listdir('all_images')
data = []
for ann in annotations[0]['annotations'][0]['result']:
    values = ann['value']['sequence']
    label = str(ann['value']['labels'])
    for value in values:
        row = {}
        row['frame_no'] = value['frame']
        row['x'] = value['x']
        row['y'] = value['y']
        row['width'] = value['width']
        row['height'] = value['height']
        row['label'] = label.replace("['", '').replace("']", '')
        data.append(row)

img = Image.open(f"all_images/{images[0]}")
org_w, org_h = img.size

for item in tqdm(data, total = len(data)):
    print(f'images/{item['frame_no']}.png')
    img = Image.open(f'images/{item['frame_no']}.png')
    print(img.size)
    x, y, width, height = normalize_bbox(item['x'], item['y'], item['width'], item['height'], org_w, org_h)
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, width+x, height+y], outline = 'red', width = 2)
    img.save('lol.png')
    break

