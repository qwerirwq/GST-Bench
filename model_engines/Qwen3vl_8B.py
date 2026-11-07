import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

class Engine:
    def __init__(self, model_name, model_path):
        if model_path != None:
            model_name = model_path
        self.processor = AutoProcessor.from_pretrained(
            model_name, num_frames=64, fps=None, trust_remote_code=True
        )
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_name, dtype="auto", device_map="auto", trust_remote_code=True
        ).eval()

    def predict(self, formatted_input):
        messages = formatted_input['messages']

        inputs = self.processor.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True,
            return_dict=True, return_tensors="pt"
        ).to(self.model.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=False,
                num_beams=1,
            )
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            output_text = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
        return output_text[0]
