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

jsonl_path = args.output_dir / 'Self_Localization_Global_Position.jsonl'


def read_jsonl(file_path, eval_dir):
    return read_task_results(file_path, eval_dir)
def parse_point(s: str):
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    if "<point>" in s and "</point>" in s:
        s = s.replace("<point>", " ").replace("</point>", " ")
    parts = s.replace(",", " ").split()
    if len(parts) < 2:
        return None
    try:
        x = float(parts[0])
        y = float(parts[1])
    except ValueError:
        return None
    return x, y


pred_info = read_jsonl(jsonl_path, args.eval_dir)
max_dist = float(np.hypot(999.0, 999.0))
dists = []

total_gt = 0
for record in pred_info:
    gt_s = record.get("gt")
    # pred_s = record.get("pred")
    if type(record.get('pred', '')) == list:
        pred_s = record.get('pred', '')[0]
    else:
        pred_s = record.get('pred', '')
    gt_xy = parse_point(gt_s)
    if gt_xy is None:
        continue

    total_gt += 1

    pred_xy = parse_point(pred_s)
    if pred_xy is None:
        dists.append(max_dist)
        continue

    gt_x, gt_y = gt_xy
    pred_x, pred_y = pred_xy

    dx = pred_x - gt_x
    dy = pred_y - gt_y
    dists.append(float(np.hypot(dx, dy)))

dists = np.array(dists, dtype=float)

total = int(total_gt)
if total == 0:
    mae = float("nan")
    std = float("nan")
else:
    mae = float(np.mean(dists))
    std = float(np.std(dists))

# print(f"Mean Euclidean Error: {mae:.4f}")
# print(f"Std Deviation: {std:.4f}")

thresholds = np.arange(100, 301, 50, dtype=float)
if total == 0:
    accs = np.zeros_like(thresholds, dtype=float)
else:
    accs = np.array([(dists <= t).mean() for t in thresholds], dtype=float)
macc = float(accs.mean())

# print("\nAccuracy@Threshold")
# print("------------------")
# for t, acc in zip(thresholds, accs):
#     print(f"Acc@{int(t):3}: {acc:.4f}")
# print(f"\nmAcc: {macc:.4f}")

# print()
# print(f"{mae:.4f}")
# print(f"{std:.4f}")
# for acc in accs:
#     # 放大100倍后保留2位小数
#     print(f"{acc * 100:.2f}")

# 同样处理 macc
print(f"{macc * 100:.2f}")
