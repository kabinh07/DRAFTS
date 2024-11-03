from PIL import Image, ImageDraw
import json

with open('dataset.json', 'r') as f:
    dataset = json.load(f)

def normalize_bbox(x, y, width, height, original_width, original_height):
    x_center = x / 100.0 * original_width
    y_center = y / 100.0 * original_height
    width = width / 100.0 * original_width
    height = height / 100.0 * original_height
    return x_center, y_center, width, height

def denormalize_bbox(x_center_norm, y_center_norm, width_norm, height_norm, image_width, image_height):
    x_center = x_center_norm * image_width
    y_center = y_center_norm * image_height
    width = width_norm * image_width
    height = height_norm * image_height

    return x_center, y_center, width, height

for idx, data in enumerate(dataset): 
    img = Image.open(f"images/{data['frame_name']}")
    x = data['x']
    y = data['y']
    width = data['width']
    height = data['height']
    img_width, img_height = img.size
    x, y, w, h = normalize_bbox(x, y, width, height, img_width, img_height)
    x, y, w, h = (x + w / 2) / img_width, (y + h / 2) / img_height, w / img_width, h / img_height
    x, y, w, h = denormalize_bbox(x, y, w, h, img_width, img_height)
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, w+x, h+y], outline = 'red', width = 2)
    img.save(f'lol_{idx}.png')
    if idx == 5:
        break