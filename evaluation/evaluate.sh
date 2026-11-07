#!/usr/bin/env bash

usage() {
    cat <<'EOF'
Usage:
  bash evaluation/evaluate.sh --model_name MODEL_NAME --output_dir OUTPUT_DIR --eval_dir EVAL_DIR

Arguments:
  --model_name, --model-name  Model name used to normalize predictions.
  --output_dir, --output-dir  Directory containing one JSONL result file per task.
  --eval_dir, --eval-dir      Benchmark data directory used to report missing results.
  -h, --help                  Show this help message.

Example:
  bash evaluation/evaluate.sh \
    --model_name Qwen3-VL-8B-Instruct \
    --output_dir ./outputs/Qwen3-VL-8B-Instruct/results \
    --eval_dir ./data/GST-Bench
EOF
}

MODEL_NAME=""
OUTPUT_DIR=""
EVAL_DIR=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model_name|--model-name)
            [[ $# -ge 2 ]] || { echo "Error: $1 requires a value." >&2; usage >&2; exit 2; }
            MODEL_NAME="$2"
            shift 2
            ;;
        --output_dir|--output-dir)
            [[ $# -ge 2 ]] || { echo "Error: $1 requires a value." >&2; usage >&2; exit 2; }
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --eval_dir|--eval-dir)
            [[ $# -ge 2 ]] || { echo "Error: $1 requires a value." >&2; usage >&2; exit 2; }
            EVAL_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [[ -z "$MODEL_NAME" || -z "$OUTPUT_DIR" || -z "$EVAL_DIR" ]]; then
    echo "Error: --model_name, --output_dir, and --eval_dir are required." >&2
    usage >&2
    exit 2
fi

if [[ ! -d "$OUTPUT_DIR" ]]; then
    echo "Error: Output directory does not exist: $OUTPUT_DIR" >&2
    exit 2
fi

if [[ ! -d "$EVAL_DIR" ]]; then
    echo "Error: Benchmark data directory does not exist: $EVAL_DIR" >&2
    exit 2
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$(cd -- "$OUTPUT_DIR" && pwd)"
EVAL_DIR="$(cd -- "$EVAL_DIR" && pwd)"

TASKS=(
    Object_Localization_Egocentric_Direction_visual
    Object_Localization_Egocentric_Distance_visual
    Object_Localization_Global_Position_visual
    Object_Localization_Egocentric_Direction_semantic
    Object_Localization_Egocentric_Distance_semantic
    Object_Localization_Global_Position_semantic
    Self_Localization_Global_Position
    Self_Localization_Global_Orientation
    Global_Structure_Understanding_Topdown_Selection_Easy
    Global_Structure_Understanding_Topdown_Selection_Medium
    Global_Structure_Understanding_Topdown_Selection_Hard
    Global_Structure_Understanding_Trajectory_Selection
)

echo "Evaluating model: $MODEL_NAME"
echo "Reading results from: $OUTPUT_DIR"

for task in "${TASKS[@]}"; do
    echo "Running $task"
    python3 "$SCRIPT_DIR/$task.py" \
        --model_name "$MODEL_NAME" \
        --output_dir "$OUTPUT_DIR" \
        --eval_dir "$EVAL_DIR"
done

echo "All evaluation tasks completed."
