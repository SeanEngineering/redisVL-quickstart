from redis import Redis
from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex

redis_client = Redis(host="localhost", port=6379, decode_responses=True)


schema = IndexSchema.from_dict({
    "index": {
        "name": "docs",
        "prefix": "doc",
        "storage_type": "hash"
    },
    "fields": [
        {"name": "id", "type": "tag"},
        {"name": "content", "type": "text"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "algorithm": "HNSW",
                "dims": 384,
                "distance_metric": "cosine"
            }
        }
    ]
})

index = SearchIndex(schema, redis_client)


def init_index():
    index.create(overwrite=False)
