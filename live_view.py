import cv2
import time

def start_live_feed():
    camera_index = 0
    
    print("-----------------------------------------------------")
    print(" LIVE PREVIEW MODE")
    print("-----------------------------------------------------")
    print(" Press 'n' to switch to the next camera.")
    print(" Press 'q' to quit.")
    print("-----------------------------------------------------")

    while True:
        # 1. Initialize the current camera
        print(f"Connecting to Camera {camera_index}...")
        cap = cv2.VideoCapture(camera_index)
        
        # Optional: Set high resolution for accurate focus checking
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        # Optional: Force MJPEG if it's laggy
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

        if not cap.isOpened():
            print(f"Camera {camera_index} not found. Returning to Camera 0.")
            camera_index = 0
            cap.release()
            # Prevent infinite loop if NO cameras are connected
            time.sleep(1) 
            continue

        window_name = f"Live View - Camera {camera_index}"
        cv2.namedWindow(window_name)

        # 2. The Live Loop
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print(f"Failed to grab frame from Camera {camera_index}.")
                break

            # Add text instructions on the screen
            text = f"Cam {camera_index} | 'n': Next Cam | 'q': Quit"
            
            # Draw black background rectangle for text
            cv2.rectangle(frame, (0, 0), (600, 40), (0, 0, 0), -1)
            # Draw white text
            cv2.putText(frame, text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow(window_name, frame)

            # 3. Key Press Logic
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return # Exit the function completely
            
            elif key == ord('n'):
                print("Switching camera...")
                break # Break inner loop to go to next camera

        # Release current camera before switching to the next
        cap.release()
        cv2.destroyWindow(window_name)
        
        # Increment index for the next iteration
        camera_index += 1

if __name__ == "__main__":
    start_live_feed()