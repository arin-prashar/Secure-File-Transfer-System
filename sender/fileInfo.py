import os

def get_file_info(file_path: str) -> tuple:
    file_name = os.path.basename(file_path)
    print(file_name)
    file_size = os.path.getsize(file_path)    # print(file_name.encode("utf-8"))
    return file_name,file_size
# get_file_info = ("")
