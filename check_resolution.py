import cv2

def check_camera_resolution(camera_index=0):
    print(f"--- Checking Camera {camera_index} ---")
    
    # 1. Connect to Camera
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return

    # 2. Read Default Resolution
    # 3 = WIDTH, 4 = HEIGHT in OpenCV properties
    default_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    default_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Default Resolution: {int(default_w)}x{int(default_h)}")

    # 3. Test Common Resolutions
    # We try to force these high resolutions. The camera will reject them
    # and revert to its maximum supported resolution if they are too high.
    test_resolutions = [
        (1920, 1080, "FHD (1080p)"),
        (1280, 720,  "HD (720p)"),
        (640, 480,   "VGA (480p)"),
        (3840, 2160, "4K (UHD)") # Testing for 4K support
    ]

    print("\nTesting capabilities...")
    for w, h, name in test_resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        
        # Read back what the camera actually accepted
        actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        if int(actual_w) == w and int(actual_h) == h:
            print(f" [SUCCESS] Supports {name}: {w}x{h}")
        else:
            print(f" [FAILED]  Requested {name} ({w}x{h}) -> Got {int(actual_w)}x{int(actual_h)}")

    # 4. Cleanup
    cap.release()
    print("-----------------------------------")

if __name__ == "__main__":
    # Check Camera 0
    check_camera_resolution(1)
    
    # If you have your second camera plugged in, uncomment below:
    # check_camera_resolution(1)