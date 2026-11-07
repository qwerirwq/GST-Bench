import llava
from transformers import GenerationConfig

class Engine:
    def __init__(self, model_name, model_path):
        if model_path is not None:
            model_name = model_path

        model = llava.load(model_name)
        model.config.do_sample = False

        model.config.num_video_frames = 64
        model.config.video_max_tiles = 1
        model.llm.config.video_max_tiles = 1

        self.gen_cfg = GenerationConfig(
            max_new_tokens=1024,
            do_sample=False,
            num_beams=1,
        )
        self.model = model
    def predict(self, formatted_input):
        prompt = formatted_input['prompt']

        resp = self.model.generate_content(prompt, generation_config=self.gen_cfg)
        return resp
