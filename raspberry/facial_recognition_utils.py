from deepface import DeepFace
import cv2


class FacialRecognition:
    
    def __init__(self , camera=0):
        self.cap = cv2.VideoCapture(camera)
    
    def get_face_by_camera(self) -> object | None:
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def close_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
            
    def check_face_exists_in_database(self, face_image , face_in_database) -> bool:
        try:
            # Compare the captured face with the saved image
            result = DeepFace.verify(face_image, face_in_database, enforce_detection=False)
            if result['verified']:
                print(f"Face matches with {face_in_database}")
                return True
            else:
                print(f"Face does not match with {face_in_database}")
                return False
        except Exception as e:
            print(f"An error occurred during comparison: {e}")
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