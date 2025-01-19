
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
    
    def generate_id_and_name_of_nurses(self):
        text = ""
        for nurse in self.nurses:
            formated_text = f"\n{nurse} -> {self.nurses[nurse]['first_name']} {self.nurses[nurse]['middle_name']} {self.nurses[nurse]['last_name']} "
            text += formated_text
        
        return text

    def generate_id_and_name_of_patients(self):
        text = ""
        for patient in self.patients:
            formated_text = f"\n{patient} -> {self.patients[patient]['first_name']} {self.patients[patient]['middle_name']} {self.patients[patient]['last_name']} "
            text += formated_text
        
        return text

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
                
        
    def get_user_by_name(self, name : str):
        people = {}
        for nurse in self.nurses:
            if name.lower() in self.nurses[nurse]["name"].lower():
                people[nurse] = self.nurses[nurse]
        for patient in self.patients:
            if name.lower() in self.patients[patient]["name"].lower():
                people[patient] = self.patients[patient]
                
        return people
    
            
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