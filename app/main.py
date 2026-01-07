from fastapi import FastAPI, UploadFile, File
from app.redis_index import index, init_index, image_index
from redisvl.query import VectorQuery
from app.embeddings import embed, embed_image, embed_text
from app.models import DocumentIn, SearchRequest
import numpy as np
from io import BytesIO
from PIL import Image
import uuid

app = FastAPI(title="RedisVL Semantic Search")


@app.on_event("startup")
def startup():
    init_index()


@app.post("/documents")
def add_document(doc: DocumentIn):
    embedding_vector = embed(doc.content)  # This returns a list of floats

    # Convert to float32 numpy array
    vec_np = np.array(embedding_vector, dtype=np.float32)

    # Convert to bytes
    vec_bytes = vec_np.tobytes()

    record = {
        "_id": doc.id,  # Use _id to better differentiate the ids
        "content": doc.content,
        "embedding": vec_bytes
    }

    index.load([record])
    return {"status": "ok"}


@app.post("/search")
def search(req: SearchRequest):
    vector = embed(req.query)

    # build a RedisVL vector query
    query_obj = VectorQuery(
        vector=vector,
        vector_field_name="embedding",
        num_results=req.k,
        return_fields=["_id", "content"]
    )

    # run the search
    results = index.query(query_obj)

    return results


@app.post("/images")
async def add_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    embedding_vector = embed_image(img)

    record = {
        "_id": str(uuid.uuid4()),
        "content": file.filename,
        "embedding": embedding_vector
    }

    image_index.load([record])

    return {"status": "ok", "id": record["_id"]}


@app.post("/search-images")
def search_images(req: SearchRequest):
    vector = embed_text(req.query)

    query_obj = VectorQuery(
        vector=vector,
        vector_field_name="embedding",
        num_results=req.k,
        return_fields=["_id", "content"]
    )

    results = image_index.query(query_obj)
    return results
