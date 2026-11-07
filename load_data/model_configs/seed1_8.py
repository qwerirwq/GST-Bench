import os
import cv2
import base64
import numpy as np
import requests
def calculate_doubao_fps(video_path, max_frames=64):
    """Compute an API sampling rate that targets ``max_frames`` per video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file: {video_path}")
        return 1.0

    total_raw_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    if original_fps <= 0:
        return 1.0

    duration_seconds = total_raw_frames / original_fps
    cap.release()

    if duration_seconds <= 0:
        return 1.0

    suggested_fps = max_frames / duration_seconds

    # The API accepts sampling rates between 0.2 and 5.0 FPS.
    final_fps = max(0.2, min(5.0, suggested_fps))
    return round(final_fps, 2)
def encode_file_to_base64(file_path):
    """Encode a local file as a base64 string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')
def get_image_data_url(image_path):
    image_b64 = encode_file_to_base64(image_path)
    image_data_url = f"data:image/jpeg;base64,{image_b64}"
    return image_data_url
def get_video_data_url(video_path):
    video_b64 = encode_file_to_base64(video_path)
    video_data_url = f"data:video/mp4;base64,{video_b64}"
    return video_data_url



def Object_Localization_Egocentric_Direction_visual(record):

    video_prompt = record['texts'][0]
    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]

    video_url = get_video_data_url(video_path)
    image_url = get_image_data_url(image_path)

    fps = calculate_doubao_fps(video_path)

    input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": video_prompt},
                    {"type": "input_video", "video_url": video_url,"fps": fps},
                    {"type": "input_text", "text": img_prompt},
                    {"type": "input_image", "image_url":image_url},
                    {"type": "input_text", "text": question_prompt},
                ]
            }
        ]
    answer = record['answer']
    return {"input": input, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer

def Object_Localization_Egocentric_Direction_visual_test(record):

    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]

    image_url = get_image_data_url(image_path)

    input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": img_prompt},
                    {"type": "input_image", "image_url":image_url},
                    {"type": "input_text", "text": question_prompt.replace(' in the video','')},
                ]
            }
        ]
    answer = record['answer']
    return {"input": input, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer


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


    video_url = get_video_data_url(video_path)
    image_url_1 = get_image_data_url(image_path_1)
    image_url_2 = get_image_data_url(image_path_2)
    image_url_3 = get_image_data_url(image_path_3)
    image_url_4 = get_image_data_url(image_path_4)

    fps = calculate_doubao_fps(video_path)

    input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": video_prompt},
                    {"type": "input_video", "video_url": video_url,"fps": fps},
                    {"type": "input_text", "text": img_prompt_1},
                    {"type": "input_image", "image_url": image_url_1},
                    {"type": "input_text", "text": img_prompt_2},
                    {"type": "input_image", "image_url": image_url_2},
                    {"type": "input_text", "text": img_prompt_3},
                    {"type": "input_image", "image_url": image_url_3},
                    {"type": "input_text", "text": img_prompt_4},
                    {"type": "input_image", "image_url": image_url_4},
                ]
            }
        ]
    answer = record['answer']
    return {"input": input, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer
def Self_Localization_Global_Orientation(record):

    video_prompt = record['texts'][0]
    img_prompt_1 = record['texts'][1]
    img_prompt_2 = record['texts'][2]
    question_prompt = record['texts'][3]

    video_path = record['video_path']
    image_path_1 = record['image_path'][0]
    image_path_2 = record['image_path'][1]

    video_url = get_video_data_url(video_path)
    image_url_1 = get_image_data_url(image_path_1)
    image_url_2 = get_image_data_url(image_path_2)

    fps = calculate_doubao_fps(video_path)

    input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": video_prompt},
                    {"type": "input_video", "video_url": video_url,"fps": fps},
                    {"type": "input_text", "text": img_prompt_1},
                    {"type": "input_image", "image_url": image_url_1},
                    {"type": "input_text", "text": img_prompt_2},
                    {"type": "input_image", "image_url": image_url_2},
                    {"type": "input_text", "text": question_prompt},
                ]
            }
        ]
    answer = record['answer']
    return {"input": input, "video_path": record['video_path'], "image_path": record['image_path'],'uid':record['uid']},answer


def process_another_task(record):
    """Return an empty prompt for the placeholder task mapping."""
    return {"messages": []}

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

    "semantic_target_direction_seen": Object_Localization_Egocentric_Direction_visual_test,
    "Another_Task_Name": process_another_task,
}
