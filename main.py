import io
import os
import time
from typing import Annotated, Union

import cv2
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
IMAGE_DIR = "./images"
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")


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


@app.post(
    "/uploadfile",
    # responses={200: {"content": {"image/jpg": {}}}},
    # response_class=Response,
)
async def create_upload_file(file: UploadFile):
    # Save the uploaded file to a temporary location
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    delete_files_in_directory("./images")

    # Process the uploaded file using OpenCV
    first_frame_bytes, last_frame_bytes, first_frame, last_frame = process_video(
        file_location
    )
    cv2.imwrite("./images/first_image.jpg", first_frame)
    cv2.imwrite("./images/last_image.jpg", last_frame)

    # Return all file names in images directory
    return os.listdir(IMAGE_DIR)

    # Return the first and last frames as a list of byte strings
    # return Response(content=first_frame_bytes, media_type="image/jpg")


@app.post("/stream")
async def stream_response(file: UploadFile):
    data = b"hello world\n" * 20000
    stream = io.BytesIO(data)
    return StreamingResponse(stream, media_type="text/plain")
    # # Save the uploaded file to a temporary location
    # file_location = f"/tmp/{file.filename}"
    # with open(file_location, "wb") as buffer:
    #     buffer.write(await file.read())
    #
    # # Process the uploaded file using OpenCV
    # first_frame, last_frame = process_video(file_location)
    #
    # # Return the first and last frames as a list of byte strings
    # return Response(content=last_frame, media_type="image/jpg")
    # return {"first_frame": "dd", "last_frame": "sdd"}


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

    # Convert the frames to jpg format
    # first_frame_bytes = cv2.imencode(".jpg", first_frame)[1]
    # last_frame_bytes = cv2.imencode(".jpg", last_frame)[1]

    return first_frame_bytes, last_frame_bytes, first_frame, last_frame


def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


@app.post("/post")
def process_file(item: Item):
    if item.file == "test":
        return {"file": item.file, "message": "Test file received"}
    time.sleep(2)
    return item
