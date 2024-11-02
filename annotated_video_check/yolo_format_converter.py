import json
import os
from PIL import Image, ImageDraw
from tqdm import tqdm
import subprocess

map_label = {
    'truck': 0.0,
    'car': 1.0
}

def convert_frames(video_filename):
    video_prefix = video_filename.split('.')[0]
    input_path = f'/home/kabin/ls_test/mydata/nas_data/cctv_footage/all_footage/{video_filename}'
    output_path = f'/home/kabin/drafts/DRAFTS/annotated_video_check/all_images/{video_prefix}_%d.jpg'
    try:
        subprocess.run(['ffmpeg', '-i', input_path, '-vf', "fps=25", output_path])
    except:
        return
    return

def normalize_bbox(x, y, width, height, original_width, original_height):
    x_center = x / 100.0 * original_width
    y_center = y / 100.0 * original_height
    width = width / 100.0 * original_width
    height = height / 100.0 * original_height
    return x_center, y_center, width, height

with open('project-1-at-2024-11-02-12-42-facb572e.json', 'r') as f:
    annotations = json.load(f)

data = []

for idx, ann in enumerate(annotations): 
    file = ann['data']['video'].split('/')[-1]
    print(file)
    convert_frames(file)
    for result in ann['annotations'][0]['result']:
        values = result['value']['sequence']
        label = str(result['value']['labels'][0])
        for frame in tqdm(values, total = len(values)):
            row = {}
            row['frame_name'] = f"{file.split('.')[0]}_{frame['frame']}.jpg"
            row['x'] = frame['x']
            row['y'] = frame['y']
            row['width'] = frame['width']
            row['height'] = frame['height']
            row['label'] = label
            data.append(row)

with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

# img = Image.open(f"all_images/{images[0]}")
# org_w, org_h = img.size

# for item in tqdm(data, total = len(data)):
#     print(f'images/{item['frame_no']}.png')
#     img = Image.open(f'images/{item['frame_no']}.png')
#     print(img.size)
#     x, y, width, height = normalize_bbox(item['x'], item['y'], item['width'], item['height'], org_w, org_h)
#     draw = ImageDraw.Draw(img)
#     draw.rectangle([x, y, width+x, height+y], outline = 'red', width = 2)
#     img.save('lol.png')
#     break

