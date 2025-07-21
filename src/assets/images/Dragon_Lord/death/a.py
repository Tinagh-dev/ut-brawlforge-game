from PIL import Image
import os

# Load the sprite sheet
image_path = "dragon_lord_death_160x160.png"  # Adjust to your image name
img = Image.open(image_path).convert("RGBA")

# Output directory
output_dir = "dragon_lord_frames"
os.makedirs(output_dir, exist_ok=True)

# Helper function to check if a column is fully black or transparent
def is_column_empty(img, x):
    for y in range(img.height):
        r, g, b, a = img.getpixel((x, y))
        if a != 0 and (r, g, b) != (0, 0, 0):
            return False
    return True

# Scan and slice
in_frame = False
start_x = 0
frame_index = 0

for x in range(img.width):
    if not in_frame:
        if not is_column_empty(img, x):
            start_x = x
            in_frame = True
    else:
        if is_column_empty(img, x):
            frame = img.crop((start_x, 0, x, img.height))
            frame.save(os.path.join(output_dir, f"{frame_index}.png"))
            frame_index += 1
            in_frame = False

# Final frame (if the image ends while still inside a frame)
if in_frame:
    frame = img.crop((start_x, img.width, img.height))
    frame.save(os.path.join(output_dir, f"{frame_index}.png"))

print(f"✅ Done! Saved {frame_index + 1} frames in '{output_dir}'")
