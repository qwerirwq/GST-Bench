
import json
import argparse
from pathlib import Path

if __package__:
    from .common import add_eval_dir_argument, read_task_results
else:
    from common import add_eval_dir_argument, read_task_results

parser = argparse.ArgumentParser(description="Evaluate trajectory selection.")
parser.add_argument('--model_name', '--model-name', dest='model', required=True, help='Model name used to normalize predictions.')
parser.add_argument('--output_dir', '--output-dir', type=Path, required=True, help='Directory containing task JSONL result files.')
add_eval_dir_argument(parser)
args = parser.parse_args()

jsonl_path = args.output_dir / 'Global_Structure_Understanding_Trajectory_Selection.jsonl'
def read_jsonl(file_path, eval_dir):
    return read_task_results(file_path, eval_dir)




def process_pred(pred,model_name):
    if "A"==pred:
        return "A"
    elif "B"==pred:
        return "B"
    elif "C"==pred:
        return "C"
    elif "D"==pred:
        return "D"

    elif "A." == pred:
        return "A"
    elif "B." == pred:
        return "B"
    elif "C." == pred:
        return "C"
    elif "D." == pred:
        return "D"

    if "InternVL" in model_name:
        if "A. Image-" in pred:
            return "A"
        elif "B. Image-" in pred:
            return "B"
        elif "C. Image-" in pred:
            return "C"
        elif "D. Image-" in pred:
            return "D"

        elif "A is the" in pred:
            return "A"
        elif "B is the" in pred:
            return "B"
        elif "C is the" in pred:
            return "C"
        elif "D is the" in pred:
            return "D"
        else:
            return pred
    if "gpt4o" in model_name:
        if "correct option is A" in pred:
            return "A"
        elif "correct option is B" in pred:
            return "B"
        elif "correct option is C" in pred:
            return "C"
        elif "correct option is D" in pred:
            return "D"

        elif "is option A" in pred:
            return "A"
        elif "is option B" in pred:
            return "B"
        elif "is option C" in pred:
            return "C"
        elif "is option D" in pred:
            return "D"

        elif "is A." in pred:
            return "A"
        elif "is B." in pred:
            return "B"
        elif "is C." in pred:
            return "C"
        elif "is D." in pred:
            return "D"

        elif "A." in pred[-2:]:
            return "A"
        elif "B." in pred[-2:]:
            return "B"
        elif "C." in pred[-2:]:
            return "C"
        elif "D." in pred[-2:]:
            return "D"



    else:
        return pred



pred_info = read_jsonl(jsonl_path, args.eval_dir)

correct = 0
total = 0

for record in pred_info:
    # 跳过没有 ground truth 的样本
    if not record.get('gt'):
        continue

    gt_list = record['gt']
    if type(record.get('pred', '')) == list:
        pred_str = record.get('pred', '')[0].strip()
    else:
        pred_str = record.get('pred', '').strip()

    # 只处理单选情况（题目只对应一个正确选项）
    if isinstance(gt_list, list):
        if len(gt_list) != 1:
            continue  # 跳过多选或空的情况（根据你的需求调整）
        gt = gt_list[0].strip().upper()
    else:
        gt = str(gt_list).strip().upper()


    pred = process_pred(pred_str,args.model)
    # 仅当预测为单个字母（A-Z）时才参与评估（可选过滤）
    if len(pred) != 1 or not pred.isalpha():
        total += 1
        continue

    total += 1
    if gt == pred:
        correct += 1

if total == 0:
    print("没有有效的样本用于评估。")
else:
    accuracy = correct / total
    # print(f"Total samples: {total}")
    # print(f"Correct predictions: {correct}")
    print(f"{accuracy*100:.2f} ")
