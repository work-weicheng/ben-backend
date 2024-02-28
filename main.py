import time
from typing import Annotated, Union

import cv2
from fastapi import FastAPI, File, Response, UploadFile
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class Item(BaseModel):
    file: str


@app.post("/file")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    # Save the uploaded file to a temporary location
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # Process the uploaded file using OpenCV
    first_frame, last_frame = process_video(file_location)

    print("yoyoyo")
    print(first_frame)
    # Return the first and last frames as a list of byte strings
    return Response(content=first_frame, media_type="image/jpg")
    return {"first_frame": "dd", "last_frame": "sdd"}


def process_video(file_location):
    # Open the video file using OpenCV
    cap = cv2.VideoCapture(file_location)
    if not cap.isOpened():
        raise ValueError("Could not open video file")

    # Read the first frame of the video
    ret, first_frame = cap.read()
    if not ret:
        raise ValueError("Could not read first frame of video")

    # Go to the last frame of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)

    # Read the last frame of the video
    ret, last_frame = cap.read()
    if not ret:
        raise ValueError("Could not read last frame of video")

    # Close the video capture object
    cap.release()

    # Convert the frames to byte strings
    first_frame_bytes = cv2.imencode(".jpg", first_frame)[1].tobytes()
    last_frame_bytes = cv2.imencode(".jpg", last_frame)[1].tobytes()

    return first_frame_bytes, last_frame_bytes


@app.post("/post")
def process_file(item: Item):
    if item.file == "test":
        return {"file": item.file, "message": "Test file received"}
    time.sleep(2)
    return item
