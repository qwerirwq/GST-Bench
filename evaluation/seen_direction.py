import argparse
import json
from pathlib import Path

if __package__:
    from .common import add_eval_dir_argument, read_task_results
else:
    from common import add_eval_dir_argument, read_task_results

import numpy as np


def read_jsonl(file_path, eval_dir):
    return read_task_results(file_path, eval_dir)


def process_pred(pred, model_name):
    pred = pred.replace("°", "")
    pred = float(pred)
    return pred


def angular_abs_error(gt: float, pred: float) -> float:
    diff = abs(gt - pred) % 360
    return min(diff, 360 - diff)


def main():
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
    parser.add_argument(
        "--task",
        type=str,
        required=False,
        default="semantic_target_direction_seen",
        help="Task name, e.g., Object_Localization_Egocentric_Direction_visual",
    )
    add_eval_dir_argument(parser)
    args = parser.parse_args()

    jsonl_path = args.output_dir / f"{args.task}.jsonl"

    pred_info = read_jsonl(jsonl_path, args.eval_dir)
    errors = []
    for record in pred_info:
        if not record.get("gt"):
            continue
        try:
            gt = float(record["gt"])
            if type(record.get('pred', '')) == list:
                pred_str = record.get('pred', '')[0].strip()
            else:
                pred_str = record.get('pred', '').strip()
            pred = process_pred(pred_str, args.model)
            errors.append(angular_abs_error(gt, pred))
        except Exception:
            error = 180.0
            errors.append(error)
            continue

    errors = np.array(errors, dtype=float)
    total = int(errors.size)

    if total == 0:
        mae = float("nan")
        std = float("nan")
    else:
        mae = float(np.mean(errors))
        std = float(np.std(errors))

    print(f"Mean Absolute Error: {mae:.4f}°")
    print(f"std: {std:.4f} (°²)")

    thresholds = np.array([15, 30, 45], dtype=float)
    if total == 0:
        accs = np.zeros_like(thresholds, dtype=float)
    else:
        accs = np.array([(errors <= t).mean() for t in thresholds], dtype=float)
    macc = float(accs.mean())

    print("\nAccuracy@Threshold (°)")
    print("----------------------")
    for t, acc in zip(thresholds, accs):
        print(f"Acc@{int(t):3}°: {acc:.4f}")
    print(f"\nmAcc: {macc:.4f}")

    print(f"{mae:.4f}")
    print(f"{std:.4f}")
    for acc in accs:
        print(f"{acc * 100:.2f}")

    print(f"{macc * 100:.2f}")


if __name__ == "__main__":
    main()
