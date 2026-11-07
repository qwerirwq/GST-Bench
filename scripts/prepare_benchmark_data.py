"""Split the combined benchmark into the task files expected by inference."""

import argparse
import json
import os
import tempfile
from pathlib import Path


ALL_TASKS = (
    "Global_Structure_Understanding_Topdown_Selection_Easy",
    "Global_Structure_Understanding_Topdown_Selection_Hard",
    "Global_Structure_Understanding_Topdown_Selection_Medium",
    "Global_Structure_Understanding_Trajectory_Selection",
    "Object_Localization_Egocentric_Direction_semantic",
    "Object_Localization_Egocentric_Direction_visual",
    "Object_Localization_Egocentric_Distance_semantic",
    "Object_Localization_Egocentric_Distance_visual",
    "Object_Localization_Global_Position_semantic",
    "Object_Localization_Global_Position_visual",
    "Self_Localization_Global_Orientation",
    "Self_Localization_Global_Position",
)

TASK_ALIASES = {
    "Global_Structure_Understanding_Trajection_Selection":
        "Global_Structure_Understanding_Trajectory_Selection",
}


def prepare_benchmark_data(source, output_dir, overwrite=False):
    """Preserve each task's record order and normalize only its task name."""
    source = Path(source).resolve()
    output_dir = Path(output_dir).resolve()
    with source.open("r", encoding="utf-8") as handle:
        records = json.load(handle)
    if not isinstance(records, list):
        raise ValueError(f"Expected a JSON array of benchmark records: {source}")

    grouped = {task: [] for task in ALL_TASKS}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} must be a JSON object.")
        task = record.get("task")
        if not isinstance(task, str):
            raise ValueError(f"Record {index} has no valid task name.")
        task = TASK_ALIASES.get(task, task)
        if task not in grouped:
            raise ValueError(f"Record {index} has an unsupported task: {task}")
        normalized = dict(record)
        normalized["task"] = task
        grouped[task].append(normalized)

    missing_tasks = [task for task, rows in grouped.items() if not rows]
    if missing_tasks:
        raise ValueError("Source data is missing tasks: " + ", ".join(missing_tasks))

    # Check every destination before creating or replacing any task file.
    pending = []
    for task, rows in grouped.items():
        destination = output_dir / f"{task}.json"
        if destination == source:
            raise ValueError(f"A task output would overwrite the source: {source}")
        if destination.exists():
            try:
                with destination.open("r", encoding="utf-8") as handle:
                    identical = json.load(handle) == rows
            except (OSError, ValueError):
                identical = False
            if identical:
                continue
            if not overwrite:
                raise ValueError(
                    f"Existing task file differs from the source: {destination}. "
                    "Review the difference before using --overwrite."
                )
        pending.append((destination, rows))

    output_dir.mkdir(parents=True, exist_ok=True)
    for destination, rows in pending:
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=output_dir,
                prefix=f".{destination.stem}.", suffix=".tmp", delete=False,
            ) as handle:
                temporary_path = Path(handle.name)
                json.dump(rows, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            os.replace(temporary_path, destination)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    return {task: len(rows) for task, rows in grouped.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, required=True,
        help="Combined JSON array, such as GST-full.json.",
    )
    parser.add_argument(
        "--output_dir", "--output-dir", type=Path, required=True,
        help="Data directory in which the 12 task JSON files will be created.",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Replace existing task files that differ from the source records.",
    )
    args = parser.parse_args()
    try:
        counts = prepare_benchmark_data(args.source, args.output_dir, args.overwrite)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for task, count in counts.items():
        print(f"{task}: {count}")
    print(f"Prepared {len(counts)} task files containing {sum(counts.values())} samples.")


if __name__ == "__main__":
    main()
