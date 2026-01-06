# Using Redis VL for Semantic Search
This repo is a quick start guide to using RedisVL (Redis Vector Library). 
A lightweight Python app using FastAPI and Uvicorn will be used to interact with the Redis Server.

The all-MiniLM-L6-v2 model will be used to generate embeddings via the SentenceTransformer library.

This repo has been designed for Mac so alter the commands accordingly for Windows and Linux.

Below is a diagram of how the data flows.
![Flow diagram](image.png)

## Setup Python App

Setup virtual environment
```shell
  python3 -m venv .venv
```
Activate the virtual environment
```shell
source ./.venv/bin/activate
```

Download the python packages
```shell
  pip install -r requirements.txt
```

## Setup and Run Redis via Docker
Run a Redis instance locally using the following command
```shell
  docker run -d --name redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

## Run Python App
```shell
  python -m uvicorn app.main:app --reload
```

## Test Commands
You can add an item into your vector DB using the following command
```shell
  curl -X POST http://localhost:8000/documents \ 
    -H "Content-Type: application/json" \ 
    -d '{
      "id": "1",
      "content": "Red Car"
    }'
```

You can run a semantic search using the following command. Update the "query" parameter to change the search"
```shell
  curl -X POST http://localhost:8000/search \ 
    -H "Content-Type: application/json" \ 
    -d '{"query":"Vehicles","k":3}'
```

## Viewing items in your DB

Assuming everything is working correctly, you should now have a working vector DB running. You can see the items that you have added into the DB using the
<a href="http://localhost:8001/redis-stack/browser">Redis Stack</a> browser app.

## Troubleshooting
If you have Redis running locally then it will interfere with the port forwarding done by docker.

You can check whether it is running using
```shell
  brew service list
```

Kill the process using
```shell
  brew service stop redis
```

## References

<ul>
  <li><a href="https://docs.redisvl.com/en/latest/overview/index.html" target="_blank">RedisVL</a></li>
  <li><a href="https://www.sbert.net/docs/sentence_transformer/pretrained_models.html" target="_blank">SentenceTransformer models</a></li>
  <li><a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a></li>
  <li><a href="https://uvicorn.dev/" target="_blank">uvicorn</a></li>
</ul>
