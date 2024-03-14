import os

from enums import ViolationType


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


def get_file_objects(folder_path):
    file_objects = []
    files = os.listdir(folder_path)

    # return objects with an array of image name and video name that has the same name
    # for example: if there is a file named "result01.mp4", "result01.jpg", "result02.mp4" and "result02.jpg" in the folder, it will return
    # [ { "video": "result01.mp4", "image": "result01.jpg" }, { "video": "result02.mp4", "image": "result02.jpg" } ]
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        if file_extension == ".mp4":
            file_objects.append(
                {
                    "type": ViolationType.CROSSING.value,
                    "isReportable": True,
                    "timestamp": "2021-10-10 10:10:10 - 11:20:00",
                    "video": file,
                    "image": file_name + ".jpg",
                }
            )

    return file_objects
