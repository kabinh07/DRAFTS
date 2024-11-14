import json
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
        subprocess.run(['ffmpeg', '-i', input_path, '-vf', "fps=25.0", output_path])
    except:
        return
    return

def normalize_bbox(x, y, width, height, original_width, original_height):
    x_center = x / 100.0 * original_width
    y_center = y / 100.0 * original_height
    width = width / 100.0 * original_width
    height = height / 100.0 * original_height
    return x_center, y_center, width, height

with open('raw_data/new_dataset.json', 'r') as f:
    annotations = json.load(f)

data = []
count = 0

for idx, ann in enumerate(annotations): 
    file = ann['data']['video'].split('/')[-1]
    if file == 'outfile_11.webm':
        continue
    convert_frames(file)
    for result in ann['annotations'][0]['result']:
        values = result['value']['sequence']
        label = str(result['value']['labels'][0])
        for frame in values:
            frame['frame'] = f"{file.split('.')[0]}_{frame['frame']}.jpg"
            frame['label'] = label
            data.append(frame)

with open('raw_data/dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

