import io
import os
import subprocess
import time
from typing import Annotated, Union

import cv2
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from utils import delete_files_in_directory, get_file_objects

origins = [
    "http://localhost:5173",
    # "*",
]
middleware = [Middleware(CORSMiddleware, allow_origins=origins)]
app = FastAPI(middleware=middleware)

RESOURCES_DIR = "./resources"
app.mount("/resources", StaticFiles(directory=RESOURCES_DIR), name="resources")


# @app.get("/resources/{file_path:path}")
# async def download_file(file_path: str, response: Response):
#     # Set the path to the file
#     full_file_path = f"{RESOURCES_DIR}/{file_path}"
#
#     # Set Content-Disposition header to attachment to prompt download
#     response.headers["Content-Disposition"] = f"attachment; filename={file_path}"
#     response.headers["Accept-Ranges"] = "bytes"
#
#     # Return the file as a response
#     return FileResponse(full_file_path)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Model of the request body
class Item(BaseModel):
    file: str


@app.post("/file")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post(
    "/uploadfile",
    # responses={200: {"content": {"image/jpg": {}}}},123
    # response_class=Response,
)
async def create_upload_file(file: UploadFile):
    # Save the uploaded file to a temporary location
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    delete_files_in_directory(RESOURCES_DIR)

    # Process the uploaded file using OpenCV
    first_frame_bytes, last_frame_bytes, first_frame, last_frame = process_video(
        file_location
    )
    process_video_n_seconds(file_location, 1, "01")
    cv2.imwrite(RESOURCES_DIR + "/result01.jpg", first_frame)
    process_video_n_seconds(file_location, 2, "02")
    cv2.imwrite(RESOURCES_DIR + "/result02.jpg", last_frame)
    process_video_n_seconds(file_location, 3, "03")
    cv2.imwrite(RESOURCES_DIR + "/result03.jpg", first_frame)
    process_video_n_seconds(file_location, 4, "04")
    cv2.imwrite(RESOURCES_DIR + "/result04.jpg", last_frame)
    return get_file_objects(RESOURCES_DIR)

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


def process_video_n_seconds(file_location, n_seconds, serial_number):
    cap = cv2.VideoCapture(file_location)
    if not cap.isOpened():
        raise ValueError("Could not open video file")
    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Calculate the number of frames for 5 seconds
    num_frames = int(fps * n_seconds)
    # Create a folder to store the frames
    os.makedirs("frames", exist_ok=True)
    # Read the first 5 seconds of the video and save the frames
    for i in range(num_frames):
        success, frame = cap.read()
        if not success:
            break

        # Save each frame as an image
        cv2.imwrite(f"frames/frame_{i}.jpg", frame)
    # Release the video capture object
    cap.release()
    # Use FFmpeg to encode the frames back into a video file
    subprocess.run(
        [
            "ffmpeg",
            "-framerate",
            str(fps),
            "-i",
            "frames/frame_%d.jpg",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "23",
            "output.mp4",
        ]
    )
    # Move the output video file to the images folder
    os.rename("output.mp4", f"resources/result{serial_number}.mp4")
    # Remove the temporary files and folder
    delete_files_in_directory("./frames")


@app.post("/post")
def process_file(item: Item):
    if item.file == "test":
        return {"file": item.file, "message": "Test file received"}
    time.sleep(2)
    return item
