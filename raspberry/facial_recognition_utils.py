# from deepface import DeepFace
import cv2
import os
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

    # def check_face_exists_in_database(self, face_image, face_in_database) -> bool: 
    #     if not os.path.exists(face_in_database):
    #         print(f"Database image {face_in_database} does not exist.")
    #         return False

    #     try:
    #         # Log inputs for debugging
    #         print(f"Checking face against database: {face_in_database}")
    #         result = DeepFace.verify(face_image, face_in_database, enforce_detection=False)
    #         print(f"DeepFace result: {result}")
    #         return result['verified']
    #     except Exception as e:
    #         print(f"An error occurred during comparison: {e}")
    #         return False

    def resize_image(self, image):
        return cv2.resize(image, (128, 128)) 
    
    
    
    def check_face_exists_in_database(self, face_image, face_in_database):
        # Convert both images to grayscale
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_database = cv2.imread(face_in_database, cv2.IMREAD_GRAYSCALE)

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
        # Return the number of matches as a similarity score
        return len(matches) > 60

    # # Example usage
    # similarity_score = compare_faces_with_orb(conver_frame_to_rgb, patient_face_path)
    # print(f"ORB similarity score: {similarity_score}")
    # if similarity_score > 50:  # Adjust threshold based on testing
    #     print("Faces are similar!")
    # else:
    #     print("Faces are not similar.")

        
    # def check_face_exists_in_database(self, face_image, face_in_database) -> bool:
    #     try:
    #         # Validate if the database image exists
    #         if not os.path.exists(face_in_database):
    #             print(f"Database image {face_in_database} does not exist.")
    #             return False

    #         # Load the images
    #         face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    #         face_database = cv2.imread(face_in_database, cv2.IMREAD_GRAYSCALE)

    #         if face_database is None:
    #             print(f"Failed to load database image: {face_in_database}")
    #             return False

    #         # Resize both images to the same size for comparison
    #         face_image_rgb = cv2.resize(face_image_rgb, (128, 128))
    #         face_database = cv2.resize(face_database, (128, 128))

    #         # Compute histograms
    #         hist1 = cv2.calcHist([face_image_rgb], [0], None, [256], [0, 256])
    #         hist2 = cv2.calcHist([face_database], [0], None, [256], [0, 256])

    #         # Normalize histograms
    #         hist1 = cv2.normalize(hist1, hist1).flatten()
    #         hist2 = cv2.normalize(hist2, hist2).flatten()

    #         # Compare histograms using correlation
    #         similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    #         print(f"Similarity score: {similarity}")

    #         # Set a threshold for similarity
    #         if similarity > 0.5:  # Adjust threshold based on testing
    #             print(f"Face matches with {face_in_database}")
    #             return True
    #         else:
    #             print(f"Face does not match with {face_in_database}")
    #             return False

    #     except Exception as e:
    #         print(f"An error occurred during comparison: {e}")
    #         return False
    
    # def check_face_exists_in_database(self, face_image , face_in_database) -> bool:
    #     # Convert the frame from BGR to RGB
    #     rgb_frame = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

    #     # Convert the frame to PIL Image
    #     pil_image = Image.fromarray(rgb_frame)

    #     # Compute the hash of the captured frame
    #     frame_hash = imagehash.average_hash(pil_image)

    #     # Print the hash 
    #     hash = imagehash.average_hash(Image.open(face_in_database)) 
    #     if hash - frame_hash <= self.similarity_rate:
    #         print("Face matches with", face_in_database)
    #         return True
    #     else:
    #         return False
            

    # def check_face_exists_in_frame(face_image) -> str:
    #     try:
    #         # Check if there is a face
    #         faces = DeepFace.extract_faces(img_path=None, img=face_image, enforce_detection=False)
    #         if len(faces) == 0:
    #             print("No faces detected.")
    #             return 'empty'
    #         if len(faces) > 1:
    #             print("Multiple faces detected. Please ensure only one face is present.")
    #             return 'multiple'
    #         else:
    #             return 'face'
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return 'error'

    
    def save_face_to_database(self, face_image, face_name):
        try:
            if face_image is not None: 
                cv2.imwrite(os.path.join( os.path.dirname(__file__), "images", f"{face_name}.jpg"), face_image)
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    
# import cv2
# from deepface import DeepFace

# cap = cv2.VideoCapture(0)  # Use the USB camera

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     try:
#         # Extract faces in the frame
#         faces = DeepFace.extract_faces(frame, enforce_detection=False)

#         if len(faces) == 0:
#             print("No faces detected.")
#         else:
#             for face_info in faces:
#                 face_image = face_info['face']  # Extract the face image from the dictionary
                
#                 # Analyze facial attributes
#                 result = DeepFace.analyze(face_image, actions=['emotion', 'gender', 'age', 'race'], enforce_detection=False)
#                 print(result)

#     except Exception as e:
#         print(f"An error occurred: {e}")

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# import cv2
# from deepface import DeepFace

# # Define the path to the saved images
# saved_images = [
#     "path/to/saved_image1.jpg",
#     "path/to/saved_image2.jpg",
#     "path/to/saved_image3.jpg"
# ]

# # Initialize the video capture
# cap = cv2.VideoCapture(0)  # Change the index if using a different camera

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     try:
#         # Extract faces in the frame
#         faces = DeepFace.extract_faces(frame, enforce_detection=False)

#         if len(faces) == 0:
#             print("No faces detected.")
#         else:
#             for face_info in faces:
#                 face_image = face_info['face']  # Extract the face image from the dictionary

#                 # Loop through saved images and compare
#                 for saved_image_path in saved_images:
#                     try:
#                         # Compare the captured face with the saved image
#                         result = DeepFace.verify(face_image, saved_image_path, enforce_detection=False)
#                         if result['verified']:
#                             print(f"Face matches with {saved_image_path}")
#                         else:
#                             print(f"Face does not match with {saved_image_path}")
#                     except Exception as e:
#                         print(f"An error occurred during comparison: {e}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
