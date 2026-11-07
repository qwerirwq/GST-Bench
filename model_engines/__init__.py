import importlib

def get_model_engine(model_name, model_path):
    """Create an inference engine for a model name and checkpoint path."""
    model_map = {
        'Qwen/Qwen3-VL-2B-Instruct': 'Qwen3vl_2B',
        'Qwen/Qwen3-VL-4B-Instruct': 'Qwen3vl_4B',
        'Qwen/Qwen3-VL-8B-Instruct': 'Qwen3vl_8B',
        'Qwen/Qwen3-VL-32B-Instruct': 'Qwen3vl_32B',
        'OpenGVLab/InternVL3_5-2B': 'Internvl_2B',
        'OpenGVLab/InternVL3_5-4B': 'Internvl_4B',
        'OpenGVLab/InternVL3_5-8B': 'Internvl_8B',
        'OpenGVLab/InternVL3_5-38B': 'Internvl_38B',
        'lmms-lab/LLaVA-OneVision-1.5-4B-Instruct': 'LLaVA-OneVision-1_5-4B',
        'lmms-lab/LLaVA-OneVision-1.5-8B-Instruct': 'LLaVA-OneVision-1_5-8B',
        'gpt4o': 'gpt4o',
        'gpt5': 'gpt5',
        'gemini_2_5_pro': 'gemini_2_5_pro',
        'Efficient-Large-Model/NVILA-8B': 'NVILA',
        'Efficient-Large-Model/NVILA-15B': 'NVILA',
        'Efficient-Large-Model/NVILA-8B-Video': 'NVILA',
        'Efficient-Large-Model/NVILA-15B-Video': 'NVILA',
        'Efficient-Large-Model/qwen2-1.5b-longvila-256f': 'NVILA',
        'nvidia/Cosmos-Reason2-8B': 'Cosmos',
        'nvidia/Cosmos-Reason2-2B': 'Cosmos',
        'seed1_8': 'seed1_8',
        'gemini3':'gemini3',
        'robobrain2.5':'Qwen3vl_8B',
    }

    module_name = f"model_engines.{model_map[model_name]}"
    module = importlib.import_module(module_name)

    if hasattr(module, 'Engine'):
        return module.Engine(model_name, model_path)
    else:
        raise AttributeError(f"Module {module_name} must contain an 'Engine' class.")
