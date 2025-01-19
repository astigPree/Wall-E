
import json
import threading
import time
from copy import deepcopy
import os
from my_tools import fetch_and_save_image, SERVER_URL, extract_filename

class DataHandler:
    
    images_path = os.path.join(os.getcwd(), "images")
    nurses_image_path = os.path.join(os.getcwd(), "images", "nurse_faces")
    patients_image_path = os.path.join(os.getcwd(), "images", "patient_faces")
    
    nurses_path = os.path.join(os.getcwd(), "databases", "nurses.json")
    patients_path = os.path.join(os.getcwd(), "databases", "patients.json")
    
    nurses : dict = None
    patients : dict = None
    schedules : dict = None
    
    
    # def __init__(self):
    #     self.load_data()
    
    def load_data(self):
        with open(self.nurses_path, "r") as nurses_file:
            self.nurses : dict = json.load(nurses_file)
            
        with open(self.patients_path, "r") as patients_file:
            self.patients : dict = json.load(patients_file)
    
    def write_image_patients(self):
        for patient in self.patients:
            image_url = self.patients[patient].get("face" , None)
            if image_url:
                
                save_path = os.path.join(
                    self.images_path,
                    'patient_faces',
                    extract_filename(image_url)
                )
                
                fetch_and_save_image(
                    image_url = SERVER_URL + image_url, 
                    save_path = save_path
                )
            
     
    def write_image_nurses(self):
        for nurse in self.nurses:
            image_url = self.nurses[nurse].get("face" , None)
            
            if image_url:
                
                save_path = os.path.join(
                    self.images_path,
                    'nurse_faces',
                    extract_filename(image_url)
                )
 
                fetch_and_save_image( 
                    image_url = SERVER_URL + image_url,
                    save_path=save_path
                )
                
        
            
                           
            
    def get_nurses(self):
        for nurse in self.nurses:
            yield self.nurses[nurse]
    
    def get_patients(self):
        for patient in self.patients:
            yield self.patients[patient]
    
    def get_all_people(self):
        for nurse in self.nurses:
            yield self.nurses[nurse]
        
        for patient in self.patients:
            yield self.patients[patient]
            
    
    # ----------------------------------------------------------------
    # BELOW: Related to saving data