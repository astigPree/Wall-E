
import json
import threading
import time
from copy import deepcopy
import os

class DataHandler:
    
    images_path = os.path.join(os.path.dirname(__file__), "images")
    
    nurses_path = os.path.join(os.path.dirname(__file__), "databases", "nurses.json")
    patients_path = os.path.join(os.path.dirname(__file__), "databases", "patients.json")
    
    nurse : dict = None
    patients : dict = None
    
    
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        with open(self.nurses_path, "r") as nurses_file:
            self.nurses : dict = json.load(nurses_file)
            
        with open(self.patients_path, "r") as patients_file:
            self.patients : dict = json.load(patients_file)
            
            
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
            
        
    