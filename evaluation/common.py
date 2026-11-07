"""Load predictions and report missing results against the benchmark data."""

import json
import sys
from collections import Counter
from pathlib import Path


def add_eval_dir_argument(parser):
    parser.add_argument(
        "--eval_dir",
        "--eval-dir",
        type=Path,
        required=True,
        help="Benchmark data directory used to identify missing inference results.",
    )


def read_task_results(file_path, eval_dir):
    """Read JSONL results and report coverage without changing metric inputs."""
    file_path = Path(file_path)
    task_file = Path(eval_dir) / f"{file_path.stem}.json"
    with task_file.open("r", encoding="utf-8") as handle:
        expected_records = json.load(handle)
    if not isinstance(expected_records, list):
        raise ValueError(f"Expected a JSON array of benchmark samples: {task_file}")

    records = []
    if file_path.is_file():
        with file_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    print(
                        f"Warning: invalid JSON in {file_path}, line {line_number}: {exc}",
                        file=sys.stderr,
                    )
                    continue
                if not isinstance(record, dict):
                    raise ValueError(
                        f"Expected a JSON object in {file_path}, line {line_number}"
                    )
                records.append(record)

    index_counts = Counter(
        record["i_th"]
        for record in records
        if type(record.get("i_th")) is int
    )
    missing_indices = [
        index for index in range(len(expected_records)) if index not in index_counts
    ]
    if missing_indices:
        print(
            f"Warning: {file_path.stem}: missing inference results for "
            f"{len(missing_indices)}/{len(expected_records)} samples:",
            file=sys.stderr,
        )
        for index in missing_indices:
            uid = expected_records[index].get("uid", "<unavailable>")
            print(f"  i_th={index}, uid={uid}", file=sys.stderr)
        print(
            "Warning: this evaluation is incomplete; scores use only the available "
            "result records. Resume inference before reporting benchmark scores.",
            file=sys.stderr,
        )

    duplicate_indices = sorted(index for index, count in index_counts.items() if count > 1)
    if duplicate_indices:
        print(
            f"Warning: {file_path.stem}: duplicate result indices: {duplicate_indices}",
            file=sys.stderr,
        )
    unidentified_count = sum(type(record.get("i_th")) is not int for record in records)
    if unidentified_count:
        print(
            f"Warning: {file_path.stem}: {unidentified_count} result records have no "
            "valid integer i_th; their sample coverage cannot be verified.",
            file=sys.stderr,
        )

    if not file_path.is_file():
        raise FileNotFoundError(f"Inference result file not found: {file_path}")
    return records
