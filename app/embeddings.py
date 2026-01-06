from sentence_transformers import SentenceTransformer


# You can change the model based on the list found here: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
# Models like multi-qa-mpnet-base-cos-v1 are tuned for questions
# Models like clip-ViT-L-14 are tuned for Images
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    return model.encode(text).tolist()
