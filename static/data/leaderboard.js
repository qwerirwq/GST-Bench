window.GST_BENCH_LEADERBOARD = {
  "tasks": [
    {
      "key": "ed_v",
      "group": "Object Localization",
      "label": "Object Localization - Egocentric Direction (Visual)",
      "abbreviation": "EDᵥ",
      "metric": "mAcc"
    },
    {
      "key": "edist_v",
      "group": "Object Localization",
      "label": "Object Localization - Egocentric Distance (Visual)",
      "abbreviation": "EDistᵥ",
      "metric": "MRA"
    },
    {
      "key": "gp_v",
      "group": "Object Localization",
      "label": "Object Localization - Global Position (Visual)",
      "abbreviation": "GPᵥ",
      "metric": "mAcc"
    },
    {
      "key": "ed_s",
      "group": "Object Localization",
      "label": "Object Localization - Egocentric Direction (Semantic)",
      "abbreviation": "EDₛ",
      "metric": "mAcc"
    },
    {
      "key": "edist_s",
      "group": "Object Localization",
      "label": "Object Localization - Egocentric Distance (Semantic)",
      "abbreviation": "EDistₛ",
      "metric": "MRA"
    },
    {
      "key": "gp_s",
      "group": "Object Localization",
      "label": "Object Localization - Global Position (Semantic)",
      "abbreviation": "GPₛ",
      "metric": "mAcc"
    },
    {
      "key": "position",
      "group": "Self Localization",
      "label": "Self Localization - Global Position",
      "abbreviation": "Pos",
      "metric": "mAcc"
    },
    {
      "key": "orientation",
      "group": "Self Localization",
      "label": "Self Localization - Global Orientation",
      "abbreviation": "Ori",
      "metric": "mAcc"
    },
    {
      "key": "tds_easy",
      "group": "Scene Structure Understanding",
      "label": "Scene Structure Understanding - Top-Down Selection (Easy)",
      "abbreviation": "TDSᴱ",
      "metric": "Acc"
    },
    {
      "key": "tds_medium",
      "group": "Scene Structure Understanding",
      "label": "Scene Structure Understanding - Top-Down Selection (Medium)",
      "abbreviation": "TDSᴹ",
      "metric": "Acc"
    },
    {
      "key": "tds_hard",
      "group": "Scene Structure Understanding",
      "label": "Scene Structure Understanding - Top-Down Selection (Hard)",
      "abbreviation": "TDSᴴ",
      "metric": "Acc"
    },
    {
      "key": "trajectory",
      "group": "Scene Structure Understanding",
      "label": "Scene Structure Understanding - Trajectory Selection",
      "abbreviation": "Traj",
      "metric": "Acc"
    }
  ],
  "models": [
    {
      "name": "Gemini-2.5-Pro",
      "type": "Proprietary",
      "scores": {"ed_v": 18.60, "edist_v": 42.00, "gp_v": 31.80, "ed_s": 23.08, "edist_s": 35.40, "gp_s": 32.40, "position": 30.47, "orientation": 21.52, "tds_easy": 97.69, "tds_medium": 80.00, "tds_hard": 41.01, "trajectory": 37.44, "avg": 40.95}
    },
    {
      "name": "Gemini-3-Pro",
      "type": "Proprietary",
      "scores": {"ed_v": 21.73, "edist_v": 25.35, "gp_v": 42.23, "ed_s": 22.11, "edist_s": 27.39, "gp_s": 43.67, "position": 37.47, "orientation": 16.89, "tds_easy": 98.15, "tds_medium": 82.73, "tds_hard": 52.25, "trajectory": 42.18, "avg": 42.68}
    },
    {
      "name": "Gemini-3.1-Pro",
      "type": "Proprietary",
      "scores": {"ed_v": 31.55, "edist_v": 44.87, "gp_v": 51.15, "ed_s": 34.13, "edist_s": 39.47, "gp_s": 62.80, "position": 54.34, "orientation": 35.28, "tds_easy": 99.54, "tds_medium": 89.09, "tds_hard": 56.74, "trajectory": 55.45, "avg": 54.53}
    },
    {
      "name": "GPT-5",
      "type": "Proprietary",
      "scores": {"ed_v": 27.98, "edist_v": 27.35, "gp_v": 34.28, "ed_s": 31.09, "edist_s": 27.39, "gp_s": 43.23, "position": 22.33, "orientation": 16.74, "tds_easy": 97.69, "tds_medium": 79.55, "tds_hard": 43.26, "trajectory": 39.34, "avg": 40.85}
    },
    {
      "name": "GPT-5.5",
      "type": "Proprietary",
      "scores": {"ed_v": 37.65, "edist_v": 35.61, "gp_v": 54.28, "ed_s": 39.90, "edist_s": 36.55, "gp_s": 53.54, "position": 53.02, "orientation": 45.59, "tds_easy": 99.07, "tds_medium": 87.27, "tds_hard": 60.67, "trajectory": 56.40, "avg": 54.96}
    },
    {
      "name": "GPT-4o",
      "type": "Proprietary",
      "scores": {"ed_v": 19.64, "edist_v": 10.09, "gp_v": 22.36, "ed_s": 13.46, "edist_s": 10.13, "gp_s": 25.24, "position": 24.03, "orientation": 15.99, "tds_easy": 81.02, "tds_medium": 71.36, "tds_hard": 45.51, "trajectory": 25.12, "avg": 30.33}
    },
    {
      "name": "Seed1.8",
      "type": "Proprietary",
      "scores": {"ed_v": 16.37, "edist_v": 12.43, "gp_v": 27.96, "ed_s": 20.35, "edist_s": 13.32, "gp_s": 36.07, "position": 28.45, "orientation": 17.79, "tds_easy": 99.07, "tds_medium": 67.27, "tds_hard": 37.64, "trajectory": 31.75, "avg": 34.04}
    },
    {
      "name": "Seed2.1-Pro",
      "type": "Proprietary",
      "scores": {"ed_v": 31.55, "edist_v": 25.74, "gp_v": 37.70, "ed_s": 35.74, "edist_s": 34.87, "gp_s": 44.37, "position": 34.34, "orientation": 23.77, "tds_easy": 100.00, "tds_medium": 87.73, "tds_hard": 49.44, "trajectory": 44.55, "avg": 45.82}
    },
    {
      "name": "GPT-6 Astra",
      "type": "Proprietary",
      "scores": {"ed_v": 61.61, "edist_v": 58.74, "gp_v": 94.87, "ed_s": 67.95, "edist_s": 52.57, "gp_s": 90.83, "position": 94.34, "orientation": 94.02, "tds_easy": 100.00, "tds_medium": 100.00, "tds_hard": 88.76, "trajectory": 94.79, "avg": 83.26}
    },
    {
      "name": "LLaVA-OV-1.5-4B",
      "type": "Open-source",
      "scores": {"ed_v": 17.41, "edist_v": 4.17, "gp_v": 14.28, "ed_s": 17.63, "edist_s": 4.34, "gp_s": 18.86, "position": 20.23, "orientation": 16.29, "tds_easy": 49.54, "tds_medium": 37.27, "tds_hard": 27.53, "trajectory": 25.59, "avg": 21.10}
    },
    {
      "name": "LLaVA-OV-1.5-8B",
      "type": "Open-source",
      "scores": {"ed_v": 17.71, "edist_v": 5.52, "gp_v": 14.22, "ed_s": 18.11, "edist_s": 3.94, "gp_s": 10.83, "position": 13.33, "orientation": 16.89, "tds_easy": 52.78, "tds_medium": 33.18, "tds_hard": 21.91, "trajectory": 26.54, "avg": 19.58}
    },
    {
      "name": "Qwen3-VL-2B",
      "type": "Open-source",
      "scores": {"ed_v": 17.41, "edist_v": 4.13, "gp_v": 9.73, "ed_s": 16.19, "edist_s": 6.55, "gp_s": 18.08, "position": 20.93, "orientation": 18.39, "tds_easy": 88.89, "tds_medium": 25.91, "tds_hard": 21.35, "trajectory": 24.17, "avg": 22.64}
    },
    {
      "name": "Qwen3-VL-4B",
      "type": "Open-source",
      "scores": {"ed_v": 15.33, "edist_v": 4.09, "gp_v": 17.46, "ed_s": 16.66, "edist_s": 6.55, "gp_s": 12.66, "position": 19.61, "orientation": 18.09, "tds_easy": 94.44, "tds_medium": 34.09, "tds_hard": 22.47, "trajectory": 26.07, "avg": 23.96}
    },
    {
      "name": "Qwen3-VL-8B",
      "type": "Open-source",
      "scores": {"ed_v": 18.75, "edist_v": 5.57, "gp_v": 17.35, "ed_s": 12.50, "edist_s": 11.59, "gp_s": 13.01, "position": 24.81, "orientation": 17.64, "tds_easy": 96.76, "tds_medium": 42.27, "tds_hard": 25.28, "trajectory": 25.12, "avg": 25.89}
    },
    {
      "name": "Qwen3-VL-32B",
      "type": "Open-source",
      "scores": {"ed_v": 16.67, "edist_v": 13.96, "gp_v": 18.05, "ed_s": 15.22, "edist_s": 16.19, "gp_s": 26.55, "position": 24.03, "orientation": 17.64, "tds_easy": 94.44, "tds_medium": 60.45, "tds_hard": 32.58, "trajectory": 29.38, "avg": 30.43}
    },
    {
      "name": "InternVL3.5-2B",
      "type": "Open-source",
      "scores": {"ed_v": 18.45, "edist_v": 2.70, "gp_v": 9.50, "ed_s": 18.11, "edist_s": 4.56, "gp_s": 13.97, "position": 12.25, "orientation": 17.34, "tds_easy": 59.72, "tds_medium": 29.09, "tds_hard": 25.84, "trajectory": 25.12, "avg": 19.72}
    },
    {
      "name": "InternVL3.5-4B",
      "type": "Open-source",
      "scores": {"ed_v": 15.63, "edist_v": 4.96, "gp_v": 8.91, "ed_s": 12.02, "edist_s": 5.40, "gp_s": 5.15, "position": 20.62, "orientation": 16.29, "tds_easy": 66.67, "tds_medium": 30.91, "tds_hard": 25.28, "trajectory": 26.07, "avg": 19.83}
    },
    {
      "name": "InternVL3.5-8B",
      "type": "Open-source",
      "scores": {"ed_v": 17.71, "edist_v": 5.57, "gp_v": 19.06, "ed_s": 16.67, "edist_s": 8.36, "gp_s": 14.85, "position": 18.84, "orientation": 13.90, "tds_easy": 75.00, "tds_medium": 35.00, "tds_hard": 25.84, "trajectory": 25.12, "avg": 22.99}
    },
    {
      "name": "InternVL3.5-38B",
      "type": "Open-source",
      "scores": {"ed_v": 21.28, "edist_v": 11.13, "gp_v": 20.29, "ed_s": 20.03, "edist_s": 10.44, "gp_s": 33.10, "position": 22.09, "orientation": 20.63, "tds_easy": 75.00, "tds_medium": 68.64, "tds_hard": 36.52, "trajectory": 29.38, "avg": 30.71}
    },
    {
      "name": "NVILA-8B",
      "type": "Open-source",
      "scores": {"ed_v": 18.15, "edist_v": 7.22, "gp_v": 15.87, "ed_s": 16.02, "edist_s": 7.52, "gp_s": 26.64, "position": 6.67, "orientation": 16.44, "tds_easy": 79.17, "tds_medium": 34.55, "tds_hard": 29.78, "trajectory": 25.59, "avg": 23.64}
    },
    {
      "name": "NVILA-15B",
      "type": "Open-source",
      "scores": {"ed_v": 15.47, "edist_v": 4.74, "gp_v": 8.85, "ed_s": 16.66, "edist_s": 3.10, "gp_s": 10.13, "position": 8.06, "orientation": 17.79, "tds_easy": 74.07, "tds_medium": 40.00, "tds_hard": 32.02, "trajectory": 22.27, "avg": 21.10}
    },
    {
      "name": "Cosmos-Reason2-2B",
      "type": "Embodied-understanding",
      "scores": {"ed_v": 15.18, "edist_v": 3.91, "gp_v": 8.38, "ed_s": 14.10, "edist_s": 7.65, "gp_s": 8.47, "position": 17.75, "orientation": 16.74, "tds_easy": 78.70, "tds_medium": 24.09, "tds_hard": 26.40, "trajectory": 18.48, "avg": 19.99}
    },
    {
      "name": "Cosmos-Reason2-8B",
      "type": "Embodied-understanding",
      "scores": {"ed_v": 13.39, "edist_v": 6.96, "gp_v": 10.86, "ed_s": 16.83, "edist_s": 7.61, "gp_s": 10.57, "position": 19.77, "orientation": 14.50, "tds_easy": 84.26, "tds_medium": 28.64, "tds_hard": 23.60, "trajectory": 22.75, "avg": 21.64}
    },
    {
      "name": "RoboBrain2.5-8B",
      "type": "Embodied-understanding",
      "scores": {"ed_v": 20.24, "edist_v": 10.39, "gp_v": 14.04, "ed_s": 19.23, "edist_s": 11.28, "gp_s": 14.06, "position": 20.31, "orientation": 16.74, "tds_easy": 80.56, "tds_medium": 37.27, "tds_hard": 26.97, "trajectory": 24.17, "avg": 24.61}
    },
    {
      "name": "RynnBrain1.1-9B",
      "type": "Embodied-understanding",
      "scores": {"ed_v": 21.43, "edist_v": 24.09, "gp_v": 20.00, "ed_s": 19.07, "edist_s": 15.71, "gp_s": 22.09, "position": 22.95, "orientation": 17.19, "tds_easy": 83.80, "tds_medium": 44.09, "tds_hard": 29.21, "trajectory": 35.55, "avg": 29.60}
    },
    {
      "name": "Robix-7B",
      "type": "Embodied-understanding",
      "scores": {"ed_v": 17.41, "edist_v": 12.35, "gp_v": 24.13, "ed_s": 18.43, "edist_s": 12.52, "gp_s": 21.83, "position": 22.95, "orientation": 15.99, "tds_easy": 88.43, "tds_medium": 53.18, "tds_hard": 35.96, "trajectory": 25.59, "avg": 29.06}
    },
    {
      "name": "Robix-32B",
      "type": "Embodied-understanding",
      "scores": {"ed_v": 18.90, "edist_v": 24.87, "gp_v": 21.95, "ed_s": 18.91, "edist_s": 20.18, "gp_s": 21.05, "position": 22.48, "orientation": 17.94, "tds_easy": 84.72, "tds_medium": 43.64, "tds_hard": 30.90, "trajectory": 25.59, "avg": 29.26}
    },
    {
      "name": "Random Guessing",
      "type": "Baseline",
      "scores": {"ed_v": 14.88, "edist_v": 23.22, "gp_v": 15.04, "ed_s": 17.31, "edist_s": 20.40, "gp_s": 14.15, "position": 16.51, "orientation": 15.55, "tds_easy": 23.15, "tds_medium": 27.73, "tds_hard": 24.72, "trajectory": 27.49, "avg": 20.01}
    },
    {
      "name": "Human Level (20 samples/task)",
      "type": "Baseline",
      "scores": {"ed_v": 75.00, "edist_v": 41.50, "gp_v": 93.00, "ed_s": 70.00, "edist_s": 41.50, "gp_s": 89.00, "position": 84.00, "orientation": 85.00, "tds_easy": 100.00, "tds_medium": 95.00, "tds_hard": 85.00, "trajectory": 90.00, "avg": 79.08}
    }
  ]
};
