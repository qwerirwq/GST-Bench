import os
import math
import numpy as np
import torch
import torchvision.transforms as T
from decord import VideoReader, cpu
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)
def get_index(bound, fps, max_frame, first_idx=0, num_segments=32):
    if bound:
        start, end = bound[0], bound[1]
    else:
        start, end = -100000, 100000
    start_idx = max(first_idx, round(start * fps))
    end_idx = min(round(end * fps), max_frame)
    seg_size = float(end_idx - start_idx) / num_segments
    frame_indices = np.array([
        int(start_idx + (seg_size / 2) + np.round(seg_size * idx))
        for idx in range(num_segments)
    ])
    return frame_indices

def load_video(video_path, bound=None, input_size=448, max_num=1, num_segments=32):
    vr = VideoReader(video_path, ctx=cpu(0), num_threads=1)
    max_frame = len(vr) - 1
    fps = float(vr.get_avg_fps())

    pixel_values_list, num_patches_list = [], []
    transform = build_transform(input_size=input_size)
    frame_indices = get_index(bound, fps, max_frame, first_idx=0, num_segments=num_segments)
    for frame_index in frame_indices:
        img = Image.fromarray(vr[frame_index].asnumpy()).convert('RGB')
        img = dynamic_preprocess(img, image_size=input_size, use_thumbnail=True, max_num=max_num)
        pixel_values = [transform(tile) for tile in img]
        pixel_values = torch.stack(pixel_values)
        num_patches_list.append(pixel_values.shape[0])
        pixel_values_list.append(pixel_values)
    pixel_values = torch.cat(pixel_values_list)
    return pixel_values, num_patches_list

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # Enumerate valid tile grids up to ``max_num`` blocks.
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # Select the grid whose aspect ratio best matches the source image.
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def load_image(image_file, input_size=448, max_num=12):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values




def Object_Localization_Egocentric_Direction_visual(record):

    video_prompt = record['texts'][0]
    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    video_path = record['video_path']
    image_path = record['image_path'][0]




    # Load one image tile and 64 uniformly distributed video frames.
    pixel_values_img = load_image(image_path, max_num=1).to(torch.bfloat16).cuda()


    pixel_values_video, num_patches_list = load_video(video_path, num_segments=64, max_num=1)
    pixel_values_video = pixel_values_video.to(torch.bfloat16).cuda()
    pixel_values = torch.cat((pixel_values_video,pixel_values_img,), dim=0)
    # Prefix each sampled frame with its position in the video.
    video_prefix = ''.join([f'Frame{i+1}: <image>\n' for i in range(len(num_patches_list))])
    # Track the patch count for every visual input.
    num_patches_list.append(pixel_values_img.size(0))


    question = video_prompt+video_prefix + img_prompt+'Image-1: <image>\n'+question_prompt

    answer = record['answer']
    return {"pixel_values": pixel_values,"question": question,"num_patches_list":num_patches_list, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer

def Object_Localization_Egocentric_Direction_visual_test(record):

    img_prompt = record['texts'][1]
    question_prompt = record['texts'][2]
    image_path = record['image_path'][0]

    pixel_values_img = load_image(image_path, max_num=1).to(torch.bfloat16).cuda()
    pixel_values = pixel_values_img

    num_patches_list = [pixel_values_img.size(0)]

    question = img_prompt + 'Image-1: <image>\n' + question_prompt.replace(' in the video', '')
    answer = record['answer']

    return {
        "pixel_values": pixel_values,
        "question": question,
        "num_patches_list": num_patches_list,
        "image_path": record['image_path'],
        "uid": record['uid']
    }, answer

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

    answer = record['answer']


    # Load one tile per reference image and 64 uniformly distributed video frames.
    pixel_values_img_1 = load_image(image_path_1, max_num=1).to(torch.bfloat16).cuda()
    pixel_values_img_2 = load_image(image_path_2, max_num=1).to(torch.bfloat16).cuda()
    pixel_values_img_3 = load_image(image_path_3, max_num=1).to(torch.bfloat16).cuda()
    pixel_values_img_4 = load_image(image_path_4, max_num=1).to(torch.bfloat16).cuda()


    pixel_values_video, num_patches_list = load_video(video_path, num_segments=64, max_num=1)
    pixel_values_video = pixel_values_video.to(torch.bfloat16).cuda()
    pixel_values = torch.cat((pixel_values_video,pixel_values_img_1,pixel_values_img_2,pixel_values_img_3,pixel_values_img_4), dim=0)
    # Prefix each sampled frame with its position in the video.
    video_prefix = ''.join([f'Frame{i+1}: <image>\n' for i in range(len(num_patches_list))])
    # Track the patch count for every visual input.
    num_patches_list.append(pixel_values_img_1.size(0))
    num_patches_list.append(pixel_values_img_2.size(0))
    num_patches_list.append(pixel_values_img_3.size(0))
    num_patches_list.append(pixel_values_img_4.size(0))

    question = video_prompt+video_prefix + img_prompt_1+'Image-1: <image>\n' + img_prompt_2+'Image-2: <image>\n' + img_prompt_3+'Image-3: <image>\n' + img_prompt_4+'Image-4: <image>\n'

    return {"pixel_values": pixel_values,"question": question,"num_patches_list":num_patches_list, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer



def Self_Localization_Global_Orientation(record):

    video_prompt = record['texts'][0]
    img_prompt_1 = record['texts'][1]
    img_prompt_2 = record['texts'][2]
    question_prompt = record['texts'][3]

    video_path = record['video_path']
    image_path_1 = record['image_path'][0]
    image_path_2 = record['image_path'][1]

    answer = record['answer']

    # Load one tile per reference image and 64 uniformly distributed video frames.
    pixel_values_img_1 = load_image(image_path_1, max_num=1).to(torch.bfloat16).cuda()
    pixel_values_img_2 = load_image(image_path_2, max_num=1).to(torch.bfloat16).cuda()

    pixel_values_video, num_patches_list = load_video(video_path, num_segments=64, max_num=1)
    pixel_values_video = pixel_values_video.to(torch.bfloat16).cuda()
    pixel_values = torch.cat((pixel_values_video,pixel_values_img_1,pixel_values_img_2), dim=0)
    # Prefix each sampled frame with its position in the video.
    video_prefix = ''.join([f'Frame{i+1}: <image>\n' for i in range(len(num_patches_list))])
    # Track the patch count for every visual input.
    num_patches_list.append(pixel_values_img_1.size(0))
    num_patches_list.append(pixel_values_img_2.size(0))

    question = video_prompt+video_prefix + img_prompt_1+'Image-1: <image>\n' + img_prompt_2+'Image-2: <image>\n' + question_prompt

    return {"pixel_values": pixel_values,"question": question,"num_patches_list":num_patches_list, "video_path": video_path, "image_path": record['image_path'],'uid':record['uid']},answer



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
    "semantic_target_distance_seen": Object_Localization_Egocentric_Direction_visual,
    "Another_Task_Name": process_another_task,
}
