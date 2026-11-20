from PIL import Image
from pathlib import Path

folder = Path("dashboards/screenshots")

for file in folder.glob("*.png"):
    image = Image.open(file).convert("RGB")

    # Resize to 1200 pixels wide, preserving aspect ratio
    if image.width > 1200:
        new_height = int(image.height * 1200 / image.width)
        image = image.resize((1200, new_height), Image.Resampling.LANCZOS)

    output_file = file.with_suffix(".jpg")
    image.save(output_file, "JPEG", quality=85, optimize=True)

    print(f"Compressed: {file.name} -> {output_file.name}")
