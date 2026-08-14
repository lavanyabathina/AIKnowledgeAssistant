import shutil
from pathlib import Path
import os


async def create_dataset_from_local(path):
    """Copy local dataset files into ./sources/local/<basename>.

    This is a lightweight generator used by the existing pipeline. If the
    destination already exists it is left untouched.
    """
    src = Path(path)
    if not src.exists():
        print(f"Local source path {src} does not exist. Skipping.")
        return

    dest_root = Path("./sources/local")
    dest_root.mkdir(parents=True, exist_ok=True)

    dest = dest_root / src.name

    if dest.exists():
        print(f"Destination {dest} already exists — skipping copy.")
        return

    try:
        print(f"Copying local dataset from {src} to {dest}")
        # shutil.copytree will copy the entire directory
        shutil.copytree(src, dest)
        print(f"Copied local dataset to {dest}")
    except Exception as e:
        print(f"Failed to copy local dataset: {e}")
        return
