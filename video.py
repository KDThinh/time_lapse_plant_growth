import cv2
import os
from datetime import datetime

def create_final_timelapse(image_folder, output_video_name, fps=30, scale_percent=50):
    # 1. Get and sort image files
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()

    if not images:
        print("No images found.")
        return

    # 2. Setup Dimensions and Video Writer
    first_img = cv2.imread(os.path.join(image_folder, images[0]))
    width = int(first_img.shape[1] * scale_percent / 100)
    height = int(first_img.shape[0] * scale_percent / 100)
    new_size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_name, fourcc, fps, new_size)

    print(f"Processing {len(images)} frames at {width}x{height}...")

    for filename in images:
        img = cv2.imread(os.path.join(image_folder, filename))
        if img is None: continue

        # 3. Resize (to reduce file size)
        img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

        # 4. Extract and Draw Timestamp (from filename)
        try:
            time_str = filename.replace("img_", "").split(".")[0]
            dt_obj = datetime.strptime(time_str, "%Y%m%d_%H%M%S")
            readable_ts = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
            
            # Position text at the bottom-left of the resized frame
            position = (int(20 * scale_percent/100), height - int(30 * scale_percent/100))
            font_scale = 1.0 * (scale_percent / 100) # Adjust font size based on video size
            
            # Draw black outline then white text
            cv2.putText(img, readable_ts, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 3)
            cv2.putText(img, readable_ts, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1)
        except:
            pass # Skip timestamp if filename format is wrong

        out.write(img)

    out.release()
    print(f"Success! Video saved as: {output_video_name}")

if __name__ == "__main__":
    input_dir =  # Folder from time_lapse_camera.py
    output_file = 
    create_final_timelapse(input_dir, output_file, fps=24, scale_percent=25)
