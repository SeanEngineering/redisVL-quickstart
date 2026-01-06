from fastapi import FastAPI
from app.redis_index import index, init_index
from redisvl.query import VectorQuery
from app.embeddings import embed
from app.models import DocumentIn, SearchRequest
import numpy as np

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
