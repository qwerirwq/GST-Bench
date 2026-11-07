class BaseEngine:
    def __init__(self, model_name, model_path):
        self.model_path = model_path
        self.model_name = model_name

    def predict(self, formatted_input):
        """Return a text prediction for an input produced by ``load_data``."""
        raise NotImplementedError
