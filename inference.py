import argparse
import json
import math
import os
import time

from tqdm import tqdm

from load_data import get_data_loader
from model_engines import get_model_engine


ALL_TASKS = (
    'Global_Structure_Understanding_Topdown_Selection_Easy',
    'Global_Structure_Understanding_Topdown_Selection_Hard',
    'Global_Structure_Understanding_Topdown_Selection_Medium',
    'Global_Structure_Understanding_Trajectory_Selection',
    'Object_Localization_Egocentric_Direction_semantic',
    'Object_Localization_Egocentric_Direction_visual',
    'Object_Localization_Egocentric_Distance_semantic',
    'Object_Localization_Egocentric_Distance_visual',
    'Object_Localization_Global_Position_semantic',
    'Object_Localization_Global_Position_visual',
    'Self_Localization_Global_Orientation',
    'Self_Localization_Global_Position'
)

SUPPORTED_MODEL_NAMES = (
    'Qwen/Qwen3-VL-2B-Instruct',
    'Qwen/Qwen3-VL-4B-Instruct',
    'Qwen/Qwen3-VL-8B-Instruct',
    'Qwen/Qwen3-VL-32B-Instruct',
    'OpenGVLab/InternVL3_5-2B',
    'OpenGVLab/InternVL3_5-4B',
    'OpenGVLab/InternVL3_5-8B',
    'OpenGVLab/InternVL3_5-38B',
    'lmms-lab/LLaVA-OneVision-1.5-4B-Instruct',
    'lmms-lab/LLaVA-OneVision-1.5-8B-Instruct',
    'gpt4o',
    'gpt5',
    'gemini_2_5_pro',
    'gemini3',
    'Efficient-Large-Model/NVILA-8B',
    'Efficient-Large-Model/NVILA-15B',
    'Efficient-Large-Model/NVILA-8B-Video',
    'Efficient-Large-Model/NVILA-15B-Video',
    'Efficient-Large-Model/qwen2-1.5b-longvila-256f',
    'nvidia/Cosmos-Reason2-8B',
    'nvidia/Cosmos-Reason2-2B',
    'seed1_8',
    'robobrain2.5',
    'Robix_7B',
    'Robix_32B',
)

SUPPORTED_MODEL_SERIES = (
    'Cosmos',
    'Internvl',
    'LLaVA-OneVision',
    'NVILA',
    'Qwen3vl',
    'Robix',
    'gemini_2_5_pro',
    'gpt4o',
    'gpt5',
    'seed1_8',
)

ROBIX_MODEL_NAMES = ('Robix_7B', 'Robix_32B')
ROBIX_MODEL_SERIES = 'Robix'
ROBIX_HELP_NOTE = 'Please contact the authors for the inference code.'


def format_model_choices(choices, restricted_choices):
    return "\n  ".join(
        f"{choice} ({ROBIX_HELP_NOTE})" if choice in restricted_choices else choice
        for choice in choices
    )


def existing_directory(value):
    if not os.path.isdir(value):
        raise argparse.ArgumentTypeError(f"directory does not exist: {value}")
    return value


def non_negative_float(value):
    try:
        parsed_value = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"expected a number, got: {value}") from exc

    if not math.isfinite(parsed_value) or parsed_value < 0:
        raise argparse.ArgumentTypeError("value must be a finite number greater than or equal to 0")
    return parsed_value


def get_args():
    parser = argparse.ArgumentParser(
        description="Run GST-Bench inference for one or more evaluation tasks.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--model_name",
        choices=SUPPORTED_MODEL_NAMES,
        default="Qwen/Qwen3-VL-8B-Instruct",
        metavar="MODEL_NAME",
        help=(
            "Model engine to use.\n"
            "Choices:\n  "
            + format_model_choices(SUPPORTED_MODEL_NAMES, ROBIX_MODEL_NAMES)
            + "\n"
            "Default: Qwen/Qwen3-VL-8B-Instruct"
        ),
    )
    parser.add_argument(
        "--model_series",
        choices=SUPPORTED_MODEL_SERIES,
        default="Qwen3vl",
        metavar="MODEL_SERIES",
        help=(
            "Input formatting implementation matching the selected model.\n"
            "Choices:\n  "
            + format_model_choices(SUPPORTED_MODEL_SERIES, (ROBIX_MODEL_SERIES,))
            + "\n"
            "Default: Qwen3vl"
        ),
    )
    parser.add_argument(
        "--model_path",
        default=None,
        help="Optional local model or checkpoint path; otherwise model_name is used.",
    )
    parser.add_argument(
        "--tasks",
        nargs='+',
        choices=ALL_TASKS,
        default=ALL_TASKS,
        metavar="TASK",
        help=(
            "Evaluation task names. Multiple values may be provided.\n"
            "Choices:\n  " + "\n  ".join(ALL_TASKS) + "\n"
            "Default: all tasks"
        ),
    )
    parser.add_argument(
        "--eval_dir",
        type=existing_directory,
        required=True,
        help="Existing directory containing one JSON file per evaluation task.",
    )
    parser.add_argument(
        "--save_dir",
        required=True,
        help="Directory in which result files will be created.",
    )
    parser.add_argument(
        "--save_name",
        default=None,
        help="Optional output folder name; defaults to the model basename.",
    )
    parser.add_argument(
        "--sleep",
        type=non_negative_float,
        default=0.0,
        metavar="SECONDS",
        help="Delay before each request, useful for rate-limited remote APIs. Default: 0.0",
    )
    args = parser.parse_args()

    if args.model_name in ROBIX_MODEL_NAMES or args.model_series == ROBIX_MODEL_SERIES:
        parser.error(
            "Robix inference code is not included in this repository. "
            + ROBIX_HELP_NOTE
        )

    missing_task_files = [
        os.path.join(args.eval_dir, f"{task_name}.json")
        for task_name in args.tasks
        if not os.path.isfile(os.path.join(args.eval_dir, f"{task_name}.json"))
    ]
    if missing_task_files:
        parser.error(
            "eval_dir is missing the following task files:\n  "
            + "\n  ".join(missing_task_files)
        )

    return args


def main():
    args = get_args()

    print(f"Loading Model Engine: {args.model_name}...")
    engine = get_model_engine(args.model_name, args.model_path)

    for task_name in args.tasks:
        print(f"\n--- Current Task: {task_name} ---")

        model_basename = args.model_name.split("/")[-1]
        save_folder = args.save_name if args.save_name else model_basename
        output_file = os.path.join(args.save_dir, save_folder, "results", f"{task_name}.jsonl")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Resume by skipping sample indices already present in the output file.
        existing_ids = set()
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        existing_ids.add(data["i_th"])
                    except json.JSONDecodeError:
                        # Ignore malformed JSONL records.
                        continue
            print(f"Existing records found: {len(existing_ids)}. Resuming...")
        else:
            print("No existing records. Starting from scratch.")

        data_iter = get_data_loader(args.model_series, task_name, args.eval_dir)

        for i, formatted_input, gt in tqdm(data_iter, desc=f"Eval {task_name}"):
            if i in existing_ids:
                continue
            try:
                if args.sleep > 0:
                    time.sleep(args.sleep)
                pred = engine.predict(formatted_input)

                # Append immediately so interrupted runs can resume.
                result_item = {
                    "i_th": i,
                    "gt": gt,
                    "pred": pred,
                    "video_path": formatted_input.get('video_path', ''),
                    "image_path": formatted_input.get('image_path', ''),
                    "uid": formatted_input.get('uid', ''),
                }
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(result_item, ensure_ascii=False) + '\n')

            except Exception as e:
                print(f"Error at index {i} in task {task_name}: {e}")
                continue

    print(f"\nEvaluation finished. Results saved at: {os.path.join(args.save_dir, save_folder)}")

if __name__ == "__main__":
    main()
