from sentence_transformers import SentenceTransformer
from PIL import Image
import numpy as np

# You can change the model based on the list found here: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
# Models like multi-qa-mpnet-base-cos-v1 are tuned for questions
# Models like clip-ViT-L-14 are tuned for Images

model = SentenceTransformer("all-MiniLM-L6-v2")

image_model = SentenceTransformer("clip-ViT-B-32")


# For standard text based encodings you can use this
def embed(text: str) -> list[float]:
    return model.encode(text).tolist()


# For image encodings you can use this
def embed_image(image: Image.Image) -> list[float]:
    emb = image_model.encode(image, normalize_embeddings=True)
    return emb.tolist()


def embed_text(text: str) -> list[float]:
    emb = image_model.encode(text, normalize_embeddings=True)
    return emb.tolist()
