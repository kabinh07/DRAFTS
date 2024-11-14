import json
import subprocess
import os
from PIL import Image
# from yolo_format_converter import normalize_bbox

label_map = {
    "heavy_truck": 0,
    "medium_truck": 1,
    "light_truck": 2,
    "large_bus": 3,
    "minibus": 4,
    "microbus": 5,
    "utility": 6,
    "car/taxi": 7,
    "auto_rickshaw": 8,
    "tempo": 9,
    "motorcycle": 10,
    "bicycle": 11,
    "cycle_rickshaw": 12,
    "rickshaw_van": 13,
    "animal/pushcart": 14
}

with open('dataset.json', 'r') as f:
    dataset = json.load(f)

for data in dataset:
    try:
        image_file = data['frame']
        if not os.path.exists(f'images/{image_file}'):
            subprocess.run(['cp', f'all_images/{image_file}', 'images'])
        img = Image.open(f'images/{image_file}')
        width, height = img.size
        x = data['x']
        y = data['y']
        w = data['width']
        h = data['height']
        # x, y, w, z = normalize_bbox(x, y, w, h, width, height)
        x, y, w, h = (x + w / 2) / 100, (y + h / 2) / 100, w / 100, h / 100
        label = float(label_map[data['label']])
        with open(f'labels/{image_file.split('.')[0]}.txt', 'a') as f:
            f.write(f"{label} {x} {y} {w} {h}")
            f.write('\n')
    except Exception as e:
        print(e)
        continue