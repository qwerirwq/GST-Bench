import transformers
import torch
class Engine:
    def __init__(self, model_name, model_path):
        if model_path is not None:
            model_name = model_path
        self.model = transformers.Qwen3VLForConditionalGeneration.from_pretrained(
                    model_name, dtype=torch.float16, device_map="auto", attn_implementation="sdpa"
                )
        self.processor: transformers.Qwen3VLProcessor = (
            transformers.AutoProcessor.from_pretrained(model_name)
        )

    def predict(self, formatted_input):
        messages = formatted_input['messages']
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
            num_frames=64,
            fps=None,
        )
        inputs = inputs.to(self.model.device)

        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            num_beams=1,
        )
        generated_ids_trimmed = [
            out_ids[len(in_ids) :]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids, strict=False)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        return output_text
