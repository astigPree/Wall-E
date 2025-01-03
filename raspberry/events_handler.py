
import os

class EventHandler:
    
    close_down = False # True if we are closing down the system, False otherwise (default)
    
    open_eyes = True # True if you want to open the eyes for reading from the camera
    has_face_scanned = False # True if there is a face scanned
    has_capture_face = False # True if the face is captured
    
    detect_nurse = False # True if you want to detect a nurse face
    detect_patient = False # True if you want to detect a patient face
    
    
    
