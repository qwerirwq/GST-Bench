import torch
from transformers import AutoModel, AutoTokenizer

class Engine:
    def __init__(self, model_name, model_path):
        if model_path is not None:
            model_name = model_path

        self.model = AutoModel.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            load_in_8bit=False,
            low_cpu_mem_usage=True,
            use_flash_attn=True,
            trust_remote_code=True,
            device_map="auto").eval()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, use_fast=False)
        self.generation_config = dict(
            max_new_tokens=1024,
            do_sample=False,
            num_beams=1,
        )

    def predict(self, formatted_input):
        pixel_values = formatted_input['pixel_values']
        question = formatted_input['question']
        num_patches_list = formatted_input['num_patches_list']

        response, history = self.model.chat(self.tokenizer, pixel_values, question, self.generation_config,
                            num_patches_list=num_patches_list, history=None, return_history=True)

        return response
