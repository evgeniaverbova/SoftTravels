import os
import shutil


def save_image_to_assets(source_path):
    if not source_path:
        return None

    assets_dir = os.path.join(os.getcwd(), "assets", "tours")
    os.makedirs(assets_dir, exist_ok=True)

    file_name = os.path.basename(source_path)
    destination_path = os.path.join(assets_dir, file_name)

    if os.path.abspath(source_path) != os.path.abspath(destination_path):
        shutil.copy2(source_path, destination_path)

    return os.path.join("assets", "tours", file_name).replace("\\", "/")