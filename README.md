# Backend Service for Car Violation Detection

A simple backend service for car violation detection using OpenCV and FastAPI, which is a modern, fast (high-performance), web framework for building APIs. It provides a easy way to return the video that someone uploaded and the result of the car violation detection.

## Stack

- Python 3.11
- FastAPI
- OpenCV
- Docker
- Docker Compose

## How to run locally

1. install the dependencies (Optional: depends on your environment, you may need to use `pip3`, `pip` or `conda`)

```bash
pip install -r requirements.txt
```

2. Run the following command to start the server

```bash
uvicorn main:app --reload
```

3. Open your browser and go to `http://localhost:8000/docs` to see the API documentation

## How to run in docker

1. Clone the repository
2. Run the following command to build and run the docker container

```bash
docker-compose up --build
```

3. Open your browser and go to `http://localhost:8000/docs` to see the API documentation
