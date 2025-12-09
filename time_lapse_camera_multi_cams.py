import cv2
import time
import os
from datetime import datetime

def capture_hub_safe(interval=300, duration_days=14, output_folder='plant_growth_hub'):
    
    # Define your cameras (Indices might be 0 and 1, or 1 and 2)
    camera_indices = [1, 2] 
    
    # Setup folders
    for i in camera_indices:
        folder = os.path.join(output_folder, f'cam_{i}')
        if not os.path.exists(folder):
            os.makedirs(folder)

    print(f"Starting Hub-Safe Time-lapse for {duration_days} days...")
    print(f"Cameras: {camera_indices}")

    start_time = time.time()
    end_time = start_time + (duration_days * 24 * 60 * 60)

    try:
        while time.time() < end_time:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # LOOP THROUGH CAMERAS ONE BY ONE
            for index in camera_indices:
                print(f"Opening Camera {index}...")
                
                # 1. Initialize Camera (Opens connection)
                cap = cv2.VideoCapture(index)
                
                # 2. Warm up (Crucial for USB hubs to stabilize power)
                # If images are black/dark, increase this to 2 or 3 seconds
                time.sleep(3)
                
                # 3. Set Resolution
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                
                # 4. Capture
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        filename = f"{output_folder}/cam_{index}/img_{timestamp}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"  > Saved: {filename}")
                    else:
                        print(f"  > Error reading frame from Cam {index}")
                
                # 5. RELEASE (Closes connection completely to free up bandwidth)
                cap.release()
                
                # Small buffer before opening the next one
                time.sleep(1)

            print(f"Waiting {interval} seconds...")
            # We subtract the time spent capturing (~6s) to keep interval roughly accurate
            time.sleep(interval - (len(camera_indices) * 3))

    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    capture_hub_safe(interval=600, duration_days=14)