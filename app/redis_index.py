from redis import Redis
from redisvl.schema import IndexSchema
from redisvl.index import SearchIndex

redis_client = Redis(host="localhost", port=6379, decode_responses=True)

# The below is the schema definition for the model.
# Simply add a record under "fields" to add an additional field. Make sure this is accounted for in the /document endpoint.
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

# Schema used for images
image_schema = IndexSchema.from_dict({
    "index": {
        "name": "images",
        "prefix": "img",
        "storage_type": "hash"
    },
    "fields": [
        {
            "name": "content",
            "type": "text"
        },
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "algorithm": "HNSW",
                "dims": 512,
                "distance_metric": "cosine",
                "type": "FLOAT32"
            }
        }
    ]
})

index = SearchIndex(schema, redis_client)

image_index = SearchIndex(image_schema, redis_client)


def init_index():
    index.create(overwrite=False)
    image_index.create(overwrite=False)
