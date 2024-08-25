import os


def get_file_info(file_path: str) -> dict:
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    return {"file_size": file_size, "file_name": file_name}