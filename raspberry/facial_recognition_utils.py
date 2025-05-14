# from deepface import DeepFace
import cv2
import os
import numpy as np
# from PIL import Image
# import imagehash

class FacialRecognition:
    def __init__(self):
        self.cap = None  # Instance-level variable

    def start_camera(self, camera=0):
        if not self.cap:
            self.cap = cv2.VideoCapture(camera)
            if not self.cap.isOpened():
                print(f"Failed to open camera {camera}.")
                self.cap = None

    def get_face_by_camera(self):
        try:
            if self.cap is None or not self.cap.isOpened():
                print("Camera is not initialized or failed to open.")
                return None

            ret, frame = self.cap.read()
            if not ret or frame is None:
                print("Failed to capture frame from camera.")
                return None

            return frame
        except Exception as e:
            print(f"Error in get_face_by_camera: {e}")
            return None

    # def conver_frame_to_rgb(self, frame):
    #     # Convert the frame to RGB format
    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     return frame_rgb

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()
        else:
            print("Camera was not initialized.")

    def resize_image(self, image):
        return cv2.resize(image, (128, 128)) 


    # def check_face_exists_in_database(self, face_image, face_in_database):
    #     # Convert input image to grayscale early
    #     face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    #     face_database = cv2.imread(face_in_database, cv2.IMREAD_GRAYSCALE)

    #     if face_database is None:
    #         print(f"Error: Unable to load image {face_in_database}.")
    #         return False

    #     # Resize images for lower memory usage
    #     face_image = cv2.resize(face_image, (64, 64))
    #     face_database = cv2.resize(face_database, (64, 64))

    #     # Compute LBP features
    #     def compute_lbp(image):
    #         lbp = np.zeros_like(image)
    #         for i in range(1, image.shape[0] - 1):
    #             for j in range(1, image.shape[1] - 1):
    #                 center = image[i, j]
    #                 binary_string = (image[i-1:i+2, j-1:j+2] >= center).astype(int)
    #                 lbp[i, j] = np.dot(binary_string.flatten(), [1, 2, 4, 8, 16, 32, 64, 128])
    #         return lbp

    #     lbp_face = compute_lbp(face_image)
    #     lbp_database = compute_lbp(face_database)

    #     # Compute similarity using Histogram comparison
    #     hist_face = cv2.calcHist([lbp_face], [0], None, [256], [0, 256])
    #     hist_database = cv2.calcHist([lbp_database], [0], None, [256], [0, 256])

    #     similarity = cv2.compareHist(hist_face, hist_database, cv2.HISTCMP_CORREL)
    #     print(f"Similarity Score: {similarity}")

    #     return similarity > 0.85  # Threshold for match

    
        
    def check_face_exists_in_database(self, face_image, face_in_database):
        # Convert input image to grayscale
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

        # Load the face database image
        face_database = cv2.imread(face_in_database, cv2.IMREAD_GRAYSCALE)

        # Ensure the image was loaded properly
        if face_database is None:
            print(f"Error: Unable to load image {face_in_database}. Check the file path.")
            return False

        # Resize images for consistency
        face_image = cv2.resize(face_image, (128, 128))
        face_database = cv2.resize(face_database, (128, 128))

        # Initialize ORB detector
        orb = cv2.ORB_create()

        # Detect keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(face_image, None)
        kp2, des2 = orb.detectAndCompute(face_database, None)

        if des1 is None or des2 is None:
            print("No keypoints found in one or both images.")
            return False

        # Match descriptors using Brute Force Matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        print(f"Number of matches: {len(matches)}")
        return len(matches) > 20



    
    def save_face_to_database(self, face_image, face_name):
        try:
            if face_image is not None: 
                cv2.imwrite(os.path.join( os.path.dirname(__file__), "images", f"{face_name}.jpg"), face_image)
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    