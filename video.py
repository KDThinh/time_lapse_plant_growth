import cv2
import os
from datetime import datetime

def create_video_with_timestamps(image_folder, output_video_name, fps=30):
    """
    Converts images into a video and embeds the timestamp from the filename onto each frame.
    """
    
    # 1. Get and sort image files
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()

    if not images:
        print(f"No images found in {image_folder}")
        return

    # 2. Determine dimensions from the first image
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, _ = frame.shape
    size = (width, height)

    # 3. Initialize Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_name, fourcc, fps, size)

    print(f"Creating video with timestamps: {output_video_name}")

    for filename in images:
        img_path = os.path.join(image_folder, filename)
        img = cv2.imread(img_path)
        
        if img is None:
            continue

        # 4. Extract and Format Timestamp
        # Filename format: img_20240107_140300.jpg
        try:
            # Remove 'img_' prefix and '.jpg' extension
            time_str = filename.replace("img_", "").split(".")[0]
            # Convert to a readable format: YYYY-MM-DD HH:MM:SS
            dt_obj = datetime.strptime(time_str, "%Y%m%d_%H%M%S")
            readable_timestamp = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            # Fallback if filename format is unexpected
            readable_timestamp = "Unknown Time"

        # 5. Draw the Timestamp onto the Frame
        # Position: Bottom-left (20 pixels from left, 50 pixels from bottom)
        position = (20, height - 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        color = (255, 255, 255) # White text
        thickness = 3
        
        # Optional: Add a subtle black outline for better visibility on bright backgrounds
        cv2.putText(img, readable_timestamp, position, font, font_scale, (0, 0, 0), thickness + 4)
        cv2.putText(img, readable_timestamp, position, font, font_scale, color, thickness)

        out.write(img)

    out.release()
    print(f"Video saved successfully as {output_video_name}")

if __name__ == "__main__":
    input_dir = 'my_timelapse' # Folder from time_lapse_camera.py
    output_file = 'timelapse_with_timestamps.mp4'
    create_video_with_timestamps(input_dir, output_file, fps=24)
