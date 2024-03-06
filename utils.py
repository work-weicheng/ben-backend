import os


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

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_type = (
                "video"
                if file_name.endswith((".mp4", ".avi", ".mov"))
                else "image"
                if file_name.endswith((".jpg", ".jpeg", ".png", ".gif"))
                else "unknown"
            )
            file_objects.append({"type": file_type, "name": file_name})

    return file_objects
