from PIL import Image, ImageDraw
import os

def draw_boxes(image, bboxes, width = 2): 
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    for box in bboxes:
        # Convert normalized coordinates to absolute pixel values
        x_center_norm, y_center_norm, width_norm, height_norm = box

        x_center = x_center_norm * image_width
        y_center = y_center_norm * image_height
        width = width_norm * image_width
        height = height_norm * image_height
        
        # Calculate top-left and bottom-right coordinates of the bounding box
        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
    return image

def draw_bbox_and_save(image, label):
    img = Image.open(f'images/{image}')
    with open(f'labels/{label}', 'r') as f:
        labels = f.read().split('\n')
    labels = [l for l in labels if l != '']
    data = []
    for label in labels:
        l = label.split(' ')
        l = [i for i in l if i!= '']
        data.append(list(map(float, l)))

    bbox = [d[1:] for d in data]

    drawn_img = draw_boxes(img, bbox)
    drawn_img.save(f'bbox_images/{image}')

images = os.listdir('images/')
labels = os.listdir('labels')
if len(images) == len(labels):
    for image in images:
        label = image.split('.')[0]+'.txt'
        print(image, label)
        draw_bbox_and_save(image, label)