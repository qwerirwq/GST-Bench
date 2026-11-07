import os
import cv2
import base64
import numpy as np
import requests
def encode_file_to_base64(file_path):
    """Encode a local file as a base64 string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')
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
            "type": "image_url",
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

    video_b64 = encode_file_to_base64(video_path)
    image_b64 = encode_file_to_base64(image_path)
    video_data_url = f"data:video/mp4;base64,{video_b64}"
    image_data_url = f"data:image/jpeg;base64,{image_b64}"

    messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": video_prompt},
                    {"type": "image_url", "image_url": {"url": video_data_url}},
                    {"type": "text", "text": img_prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                    {"type": "text", "text": question_prompt},
                ]
            }
        ]
    answer = record['answer']
    return {"input": messages, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer
def Object_Localization_Egocentric_Direction_visual_test(record):

    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]

    image_b64 = encode_file_to_base64(image_path)
    image_data_url = f"data:image/jpeg;base64,{image_b64}"

    messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": img_prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                    {"type": "text", "text": question_prompt.replace(' in the video','')},
                ]
            }
        ]
    answer = record['answer']
    return {"input": messages, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer



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


    video_b64 = encode_file_to_base64(video_path)
    image_b64_1 = encode_file_to_base64(image_path_1)
    image_b64_2 = encode_file_to_base64(image_path_2)
    image_b64_3 = encode_file_to_base64(image_path_3)
    image_b64_4 = encode_file_to_base64(image_path_4)
    video_data_url = f"data:video/mp4;base64,{video_b64}"
    image_data_url_1 = f"data:image/jpeg;base64,{image_b64_1}"
    image_data_url_2 = f"data:image/jpeg;base64,{image_b64_2}"
    image_data_url_3 = f"data:image/jpeg;base64,{image_b64_3}"
    image_data_url_4 = f"data:image/jpeg;base64,{image_b64_4}"

    messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": video_prompt},
                    {"type": "image_url", "image_url": {"url": video_data_url}},
                    {"type": "text", "text": img_prompt_1},
                    {"type": "image_url", "image_url": {"url": image_data_url_1}},
                    {"type": "text", "text": img_prompt_2},
                    {"type": "image_url", "image_url": {"url": image_data_url_2}},
                    {"type": "text", "text": img_prompt_3},
                    {"type": "image_url", "image_url": {"url": image_data_url_3}},
                    {"type": "text", "text": img_prompt_4},
                    {"type": "image_url", "image_url": {"url": image_data_url_4}},
                ]
            }
        ]
    answer = record['answer']
    return {"input": messages, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer
def Self_Localization_Global_Orientation(record):

    video_prompt = record['texts'][0]
    img_prompt_1 = record['texts'][1]
    img_prompt_2 = record['texts'][2]
    question_prompt = record['texts'][3]

    video_path = record['video_path']
    image_path_1 = record['image_path'][0]
    image_path_2 = record['image_path'][1]

    video_b64 = encode_file_to_base64(video_path)
    image_b64_1 = encode_file_to_base64(image_path_1)
    image_b64_2 = encode_file_to_base64(image_path_2)
    video_data_url = f"data:video/mp4;base64,{video_b64}"
    image_data_url_1 = f"data:image/jpeg;base64,{image_b64_1}"
    image_data_url_2 = f"data:image/jpeg;base64,{image_b64_2}"
    messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": video_prompt},
                    {"type": "image_url", "image_url": {"url": video_data_url}},
                    {"type": "text", "text": img_prompt_1},
                    {"type": "image_url", "image_url": {"url": image_data_url_1}},
                    {"type": "text", "text": img_prompt_2},
                    {"type": "image_url", "image_url": {"url": image_data_url_2}},
                    {"type": "text", "text": question_prompt},
                ]
            }
        ]
    answer = record['answer']
    return {"input": messages, "video_path": record['video_path'], "image_path": record['image_path'],'uid':record['uid']},answer


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
