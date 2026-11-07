import importlib
import json
import os
from urllib.parse import urlsplit


def _resolve_media_paths(record, eval_dir):
    """Resolve dataset-relative media paths without modifying the source record."""
    def resolve_path(path):
        if not isinstance(path, str) or not path:
            return path
        if os.path.isabs(path) or urlsplit(path).scheme:
            return path
        return os.path.normpath(os.path.join(eval_dir, path))

    resolved_record = dict(record)
    for key in ('video_path', 'image_path'):
        if key not in resolved_record:
            continue
        value = resolved_record[key]
        if isinstance(value, list):
            resolved_record[key] = [resolve_path(path) for path in value]
        else:
            resolved_record[key] = resolve_path(value)
    return resolved_record


def get_data_loader(model_name, task_name, eval_dir):
    """Yield model-formatted inputs and ground-truth answers for a task."""
    eval_dir = os.path.abspath(os.fspath(eval_dir))
    try:
        module_path = f"load_data.model_configs.{model_name}"
        model_module = importlib.import_module(module_path)
    except ImportError:
        raise ImportError(
            f"Model configuration module not found: {module_path}. "
            "Add the corresponding Python module under load_data/model_configs."
        )

    process_func = model_module.TASK_MAP.get(task_name)
    if not process_func:
        raise AttributeError(
            f"Model configuration {model_name} does not support task {task_name}; "
            "the task is not defined in TASK_MAP."
        )

    task_file = os.path.join(eval_dir, task_name)+'.json'
    if not os.path.exists(task_file):
        raise FileNotFoundError(f"Task data file not found: {task_file}")

    data_path = task_file

    with open(data_path, 'r', encoding='utf-8') as f:
        # Accept both JSON arrays and line-delimited JSON records.
        if data_path.endswith('.jsonl'):
            data_list = [json.loads(line) for line in f]
        else:
            data_list = json.load(f)

    for i, record in enumerate(data_list):
        try:
            resolved_record = _resolve_media_paths(record, eval_dir)
            formatted_input, gt = process_func(resolved_record)
        except Exception as exc:
            uid = record.get('uid', '<unavailable>') if isinstance(record, dict) else '<unavailable>'
            print(f"Error formatting sample {i} (uid={uid}) in task {task_name}: {exc}")
            continue

        yield i, formatted_input, gt
