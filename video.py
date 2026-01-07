import cv2
import os
from datetime import datetime

def create_compressed_video(image_folder, output_video_name, fps=30, scale_percent=50):
    """
    Converts images to video with an option to resize (compress) them.
    scale_percent: 50 means the video will be half the width and height of the images.
    """
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()

    if not images:
        return

    # Load first image to get original dimensions
    first_img = cv2.imread(os.path.join(image_folder, images[0]))
    
    # Calculate new dimensions
    width = int(first_img.shape[1] * scale_percent / 100)
    height = int(first_img.shape[0] * scale_percent / 100)
    new_size = (width, height)

    # Use 'avc1' (H.264) for better compression if available, else 'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_name, fourcc, fps, new_size)

    print(f"Creating video at {width}x{height} resolution...")

    for filename in images:
        img = cv2.imread(os.path.join(image_folder, filename))
        if img is None: continue

        # Resize the frame before writing
        resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        
        # (Optional) Add timestamp logic here as shown previously
        
        out.write(resized_img)

    out.release()
    print("Done.")

if __name__ == "__main__":
    # scale_percent=50 reduces 1080p to 540p, which greatly reduces file size.
    create_compressed_video('my_timelapse', 'small_timelapse.mp4', scale_percent=50)
