from sentence_transformers import SentenceTransformer
from threading import Event
import logging

class ModelEmbeddingService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.model_loaded = Event()

    def load_model(self):
        logging.info(f"Loading model {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        logging.info(f"Model {self.model_name} loaded successfully")
        self.model_loaded.set()
    
    def encode(self, text):
        if self.model is None:
            raise ValueError("Model is not loaded yet.")
        return self.model.encode(text).tolist()