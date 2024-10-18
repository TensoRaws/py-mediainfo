# download lib from https://github.com/TensoRaws/py-mediainfo/releases/tag/lib
import hashlib
import os
import sys
from pathlib import Path
from typing import Dict, List

import requests
import tqdm

projectPATH = Path(__file__).resolve().parent.parent.resolve()
libPATH = projectPATH / "pymediainfo"

# lib name, url and hash
lib_dict: Dict[str, List[str]] = {
    "libmediainfo.0.dylib": [
        "https://github.com/TensoRaws/py-mediainfo/releases/download/lib/libmediainfo.0.dylib",
        "19eca636459bd2745b45f9e1842f54b1e5560bd90b87273259fa9cd2323afb71",
    ],
    "MediaInfo.dll": [
        "https://github.com/TensoRaws/py-mediainfo/releases/download/lib/MediaInfo.dll",
        "35bc8cc3e334c95ff9597d5ad81ada726f82e5abc3c26cb28cf18067aa0e7cbd",
    ],
}


def get_file_sha256(file_path: str, blocksize: int = 1 << 20) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(blocksize)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def download_lib() -> None:
    if sys.platform == "win32":
        lib_name = "MediaInfo.dll"
    elif sys.platform == "darwin":
        lib_name = "libmediainfo.0.dylib"
    else:
        print("Linux, install libmediainfo-dev from package manager!")
        return

    lib_url, lib_hash = lib_dict[lib_name]
    lib_path = libPATH / lib_name

    if lib_path.exists():
        if get_file_sha256(str(lib_path)) == lib_hash:
            print(f"{lib_name} exists, skip download.")
            return

    print(f"Downloading {lib_name}...")
    response = requests.get(lib_url, stream=True)
    response.raise_for_status()
    with open(lib_path, "wb") as f:
        for chunk in tqdm.tqdm(response.iter_content(chunk_size=8192)):
            f.write(chunk)

    if get_file_sha256(str(lib_path)) != lib_hash:
        print("Download failed, sha256 mismatch.")
        lib_path.unlink()
        return

    print(f"Downloaded {lib_name} successfully.")


if __name__ == "__main__":
    # get all model files sha256
    for root, _, files in os.walk(libPATH):
        for file in files:
            if not file.endswith(".so") and not file.endswith(".dylib") and not file.endswith(".dll"):
                continue
            file_path = os.path.join(root, file)
            name = os.path.basename(file_path)
            print(f"{name}: {get_file_sha256(file_path)}")
