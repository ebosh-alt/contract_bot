import os
from os import listdir


def del_folder(needed_folder: str) -> None:
    try:
        # direct = [f for f in listdir(f"{needed_folder}")]
        # print(f"\n\n\n_________\n\n\n{direct} and {needed_folder}")
        # if needed_folder in direct:
        files = [f for f in listdir(f"{needed_folder}")]
        for file in files:
            os.remove(f"{needed_folder}/{file}")
            print(f"{file} FOUNDED")
    except Exception as e:
        print(e)

