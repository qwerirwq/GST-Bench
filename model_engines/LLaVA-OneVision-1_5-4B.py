from transformers import AutoTokenizer, AutoProcessor, AutoModelForCausalLM
from qwen_vl_utils import process_vision_info


class Engine:
    def __init__(self, model_name, model_path):
        if model_path is not None:
            model_name = model_path

        self.model = AutoModelForCausalLM.from_pretrained(
                model_name, torch_dtype="auto", device_map="auto", trust_remote_code=True
            )
        self.processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)


        self.processor.video_processor.max_frames = 64
        self.processor.image_processor.max_pixels = 640 * 512
        self.processor.video_processor.max_pixels = 640 * 512

    def predict(self, formatted_input):

        messages = formatted_input['messages']
        text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")
        unused_params = ['second_per_grid_ts']
        for param in unused_params:
            if param in inputs:
                del inputs[param]
        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            num_beams=1,
        )
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )



        return output_text
