
import json
import numpy as np
import argparse
from pathlib import Path

if __package__:
    from .common import add_eval_dir_argument, read_task_results
else:
    from common import add_eval_dir_argument, read_task_results

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_name",
    "--model-name",
    dest="model",
    required=True,
    help="Model name used to normalize predictions.",
)
parser.add_argument(
    "--output_dir",
    "--output-dir",
    type=Path,
    required=True,
    help="Directory containing task JSONL result files.",
)
add_eval_dir_argument(parser)
args = parser.parse_args()

jsonl_path = args.output_dir / 'Object_Localization_Egocentric_Distance_semantic.jsonl'
def process_pred(pred,model_name):
    pred = float(pred)
    return pred

def read_jsonl(file_path, eval_dir):
    return read_task_results(file_path, eval_dir)
def distance_abs_error(gt: float, pred: float) -> float:
    """计算两个距离之间的绝对误差，结果 >= 0"""
    return abs(gt - pred)


pred_info = read_jsonl(jsonl_path, args.eval_dir)
errors = []
rel_errors = []
for record in pred_info:
    if not record.get('gt'):
        continue
    try:
        gt = float(record['gt'])
        if type(record.get('pred', '')) == list:
            pred_str = record.get('pred', '')[0].strip()
        else:
            pred_str = record.get('pred', '').strip()
        pred = process_pred(pred_str,args.model)

        if gt <= 0 or pred < 0:
            err = gt
        else:
            err = distance_abs_error(gt, pred)
        errors.append(err)
        rel_errors.append(err / gt)
    except (ValueError, TypeError):
        err = gt
        errors.append(err)
        rel_errors.append(err / gt)
        continue



errors = np.array(errors, dtype=float)
rel_errors = np.array(rel_errors, dtype=float)

total = int(errors.size)
if total == 0:
    mae = float('nan')
    std = float('nan')
else:
    mae = float(np.mean(errors))
    std = float(np.std(errors))

# print(f"Mean Absolute Error: {mae:.4f}")
# print(f"Std Deviation: {std:.4f}")

# MRA (Mean Relative Accuracy)
# C = {0.50, 0.55, ..., 0.95}
# Acc(θ) = mean( |pred-gt|/gt < 1-θ )
# MRA = mean_θ Acc(θ)
C = np.round(np.arange(0.50, 0.951, 0.05), 2)
if total == 0:
    accs = np.zeros_like(C, dtype=float)
else:
    accs = np.array([(rel_errors < (1.0 - theta)).mean() for theta in C], dtype=float)
MRA = float(accs.mean())

# print("\nAcc@θ (relative error < 1-θ)")
# print("--------------------------")
# for theta, acc in zip(C, accs):
#     print(f"θ={theta:.2f}: {acc:.4f}")
# print(f"\nMRA: {MRA:.4f}")

# 方便统计
# print()
# print(f"{mae:.4f}")
# print(f"{std:.4f}")
# for acc in accs:
#     # 放大100倍并保留2位小数
#     print(f"{acc * 100:.2f}")

# MRA 同样处理
print(f"{MRA * 100:.2f}")
