import os
import cv2
import base64
import numpy as np
import requests

def get_image_data_url(image_path):
    """Encode a local or remote image as a data URL."""
    if image_path.startswith(('http://', 'https://')):
        img_bytes = requests.get(image_path).content
    else:
        with open(image_path, 'rb') as f:
            img_bytes = f.read()

    b64_image = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_image}"

def extract_uniform_frames_from_path(video_path, num_frames=64):
    """Uniformly sample video frames and encode them as JPEG data URLs."""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        raise ValueError(f"Unable to read video frame count: {video_path}")

    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    frame_data_urls = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame_bgr = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        b64_frame = base64.b64encode(buffer).decode('utf-8')

        frame_data_urls.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{b64_frame}"
        })

    cap.release()
    return frame_data_urls

def Object_Localization_Egocentric_Direction_visual(record):

    video_prompt = record['texts'][0]
    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]

    image_data_url = get_image_data_url(image_path)
    frame_data_urls = extract_uniform_frames_from_path(video_path, num_frames=64)
    final_inputs = [
        {
            "type": "input_text",
            "text": video_prompt,
        }
    ]
    final_inputs.extend(frame_data_urls)
    final_inputs.extend([
        {
            "type": "input_text",
            "text": img_prompt,
        },
        {
            "type": "input_image",
            "image_url": image_data_url,
        },
        {
            "type": "input_text",
            "text": question_prompt,
        }
    ])
    answer = record['answer']
    return {"input": final_inputs, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer
def Object_Localization_Egocentric_Direction_visual_test(record):

    video_prompt = record['texts'][0]
    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]

    image_data_url = get_image_data_url(image_path)
    final_inputs = [

    ]

    final_inputs.extend([
        {
            "type": "input_text",
            "text": img_prompt,
        },
        {
            "type": "input_image",
            "image_url": image_data_url,
        },
        {
            "type": "input_text",
            "text": question_prompt.replace(' in the video',''),
        }
    ])
    answer = record['answer']
    return {"input": final_inputs, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer

def Global_Structure_Understanding_Topdown_Selection_Easy(record):

    video_prompt = record['texts'][0]
    img_prompt_1 = record['texts'][1]
    img_prompt_2 = record['texts'][2]
    img_prompt_3 = record['texts'][3]
    img_prompt_4 = record['texts'][4]

    video_path = record['video_path']
    image_path_1 = record['image_path'][0]
    image_path_2 = record['image_path'][1]
    image_path_3 = record['image_path'][2]
    image_path_4 = record['image_path'][3]


    image_data_url_1 = get_image_data_url(image_path_1)
    image_data_url_2 = get_image_data_url(image_path_2)
    image_data_url_3 = get_image_data_url(image_path_3)
    image_data_url_4 = get_image_data_url(image_path_4)
    frame_data_urls = extract_uniform_frames_from_path(video_path, num_frames=64)
    final_inputs = [
        {
            "type": "input_text",
            "text": video_prompt,
        }
    ]
    final_inputs.extend(frame_data_urls)
    final_inputs.extend([
        {
            "type": "input_text",
            "text": img_prompt_1,
        },
        {
            "type": "input_image",
            "image_url": image_data_url_1,
        },
        {
            "type": "input_text",
            "text": img_prompt_2,
        },
        {
            "type": "input_image",
            "image_url": image_data_url_2,
        },
        {
            "type": "input_text",
            "text": img_prompt_3,
        },
        {
            "type": "input_image",
            "image_url": image_data_url_3,
        },
        {
            "type": "input_text",
            "text": img_prompt_4,
        },
        {
            "type": "input_image",
            "image_url": image_data_url_4,
        },
    ])
    answer = record['answer']
    return {"input": final_inputs, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer

def Self_Localization_Global_Orientation(record):

    video_prompt = record['texts'][0]
    img_prompt_1 = record['texts'][1]
    img_prompt_2 = record['texts'][2]
    question_prompt = record['texts'][3]

    video_path = record['video_path']
    image_path_1 = record['image_path'][0]
    image_path_2 = record['image_path'][1]

    image_data_url_1 = get_image_data_url(image_path_1)
    image_data_url_2 = get_image_data_url(image_path_2)
    frame_data_urls = extract_uniform_frames_from_path(video_path, num_frames=64)
    final_inputs = [
        {
            "type": "input_text",
            "text": video_prompt,
        }
    ]
    final_inputs.extend(frame_data_urls)
    final_inputs.extend([
        {
            "type": "input_text",
            "text": img_prompt_1,
        },
        {
            "type": "input_image",
            "image_url": image_data_url_1,
        },
        {
            "type": "input_text",
            "text": img_prompt_2,
        },
        {
            "type": "input_image",
            "image_url": image_data_url_2,
        },
        {
            "type": "input_text",
            "text": question_prompt,
        }
    ])
    answer = record['answer']

    return {"input": final_inputs, "video_path": record['video_path'], "image_path": record['image_path'],'uid':record['uid']},answer


def process_another_task(record):
    """Return an empty prompt for the placeholder task mapping."""
    return {"input": []}

# Map benchmark task names to their input formatters.
TASK_MAP = {
    "Object_Localization_Egocentric_Direction_visual": Object_Localization_Egocentric_Direction_visual,
    "Object_Localization_Egocentric_Direction_semantic": Object_Localization_Egocentric_Direction_visual,
    "Object_Localization_Egocentric_Distance_visual": Object_Localization_Egocentric_Direction_visual,
    "Object_Localization_Egocentric_Distance_semantic": Object_Localization_Egocentric_Direction_visual,
    "Object_Localization_Global_Position_visual": Object_Localization_Egocentric_Direction_visual,
    "Object_Localization_Global_Position_semantic": Object_Localization_Egocentric_Direction_visual,

    "Global_Structure_Understanding_Topdown_Selection_Easy": Global_Structure_Understanding_Topdown_Selection_Easy,
    "Global_Structure_Understanding_Topdown_Selection_Hard": Global_Structure_Understanding_Topdown_Selection_Easy,
    "Global_Structure_Understanding_Topdown_Selection_Medium": Global_Structure_Understanding_Topdown_Selection_Easy,
    "Global_Structure_Understanding_Trajectory_Selection": Global_Structure_Understanding_Topdown_Selection_Easy,


    "Self_Localization_Global_Orientation":Self_Localization_Global_Orientation,
    "Self_Localization_Global_Position":Self_Localization_Global_Orientation,

    "semantic_target_direction_seen": Object_Localization_Egocentric_Direction_visual,
    "semantic_target_distance_seen": Object_Localization_Egocentric_Direction_visual,
    "Another_Task_Name": process_another_task,
}
