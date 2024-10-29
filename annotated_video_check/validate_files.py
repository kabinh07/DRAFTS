import os
import subprocess

labels = os.listdir('labels')
files = [l.split('.')[0] for l in labels]

images = os.listdir('all_images')

for image in images:
    if image.split('.')[0] in files:
        if not os.path.exists(f'images/{image}'):
            subprocess.run(['cp', f'all_images/{image}', 'images/'])