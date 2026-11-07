
import os
from llava.media import Image, Video
def Object_Localization_Egocentric_Direction_visual(record):

    video_prompt = record['texts'][0]
    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]

    prompt = [
        video_prompt,
        Video(video_path),
        img_prompt,
        Image(image_path),
        question_prompt,
    ]
    answer = record['answer']
    return {"prompt": prompt, "video_path": video_path, "image_path": image_path,'uid':record['uid']},answer

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

    prompt =[
        video_prompt,
        Video(video_path),
        img_prompt_1,
        Image(image_path_1),
        img_prompt_2,
        Image(image_path_2),
        img_prompt_3,
        Image(image_path_3),
        img_prompt_4,
        Image(image_path_4),
    ]
    answer = record['answer']
    return {"prompt": prompt, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer

def Self_Localization_Global_Orientation(record):

    video_prompt = record['texts'][0]
    img_prompt_1 = record['texts'][1]
    img_prompt_2 = record['texts'][2]
    question_prompt = record['texts'][3]

    video_path = record['video_path']
    image_path_1 = record['image_path'][0]
    image_path_2 = record['image_path'][1]

    prompt =[
        video_prompt,
        Video(video_path),
        img_prompt_1,
        Image(image_path_1),
        img_prompt_2,
        Image(image_path_2),
        question_prompt,
    ]
    answer = record['answer']
    return {"prompt": prompt, "video_path": record['video_path'], "image_path": record['image_path'],'uid':record['uid']},answer


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

    "Another_Task_Name": process_another_task,
}
