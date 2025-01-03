
import json
import threading
import time
from copy import deepcopy
import os

class DataHandler(threading.Thread):
    
    images_path = os.path.join(os.path.dirname(__file__), "images")
    
    nurses_path = os.path.join(os.path.dirname(__file__), "databases", "nurses.json")
    patients_path = os.path.join(os.path.dirname(__file__), "databases", "patients.json")
    