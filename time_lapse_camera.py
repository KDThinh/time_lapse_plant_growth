import cv2
import time
import os
from datetime import datetime

def capture_timelapse(interval=5, duration=60, output_folder='timelapse_frames', camera_index=1):
    """
    Captures images from a webcam at a set interval.
    
    Parameters:
    - interval: Time in seconds between captures.
    - duration: Total duration of the timelapse capture in minutes.
    - output_folder: Name of the folder to save images.
    - camera_index: 0 for built-in, 1 (or higher) for external webcam.
    """
    
    # 1. Setup Output Directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    # 2. Initialize Camera
    # Note: Change camera_index to 0 if 1 doesn't work (depends on your setup)
    cap = cv2.VideoCapture(camera_index)

    # Check if camera opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera with index {camera_index}.")
        print("Try changing 'camera_index' to 0 or check your connection.")
        return

    # Set resolution (Optional: 1920x1080)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    print(f"Starting Time-lapse...")
    print(f"Interval: {interval} seconds")
    print(f"Total Duration: {duration} minutes")
    print("Press 'q' in the preview window or Ctrl+C in terminal to stop early.")

    start_time = time.time()
    end_time = start_time + (duration * 60)
    frame_count = 0

    try:
        while time.time() < end_time:
            # 3. Capture Frame
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Failed to capture image.")
                break

            # 4. Generate Filename and Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_folder}/img_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            
            frame_count += 1
            print(f"Saved: {filename} ({frame_count})")

            # 5. Show Preview (Optional)
            cv2.imshow('Time-lapse Preview', frame)

            # Wait for the interval (handling the 'q' key press for exit)
            # waitKey returns the ASCII value of the key pressed
            if cv2.waitKey(int(interval * 1000)) & 0xFF == ord('q'):
                print("Time-lapse stopped by user.")
                break
                
    except KeyboardInterrupt:
        print("\nTime-lapse stopped by Ctrl+C.")
        
    finally:
        # 6. Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print(f"Finished. Total images captured: {frame_count}")

# --- CONFIGURATION ---
if __name__ == "__main__":
    capture_timelapse(
        interval=5,         # Capture every 5 seconds
        duration=10,        # Run for 10 minutes total
        output_folder='my_timelapse',
        camera_index=1      # Try 0 if 1 fails
    )