
import os
import threading
import datetime

class EventHandler:
    
    user_commands : list[str] = []
    is_recording : bool = False
    
    close_down = False # True if we are closing down the system, False otherwise (default)
    
    has_important_event = False # True if there is a important event in the system, False otherwise (default)
    on_proccess = False # True if we are on the process, False otherwise (default)
    
    open_eyes = True # True if you want to open the eyes for reading from the camera
    activate_scanning = False # True if you want to activate the scanning of the patients and nurses
    has_face_scanned = False # True if there is a face scanned
    has_capture_face = False # True if the face is captured
    
    detect_nurse = False # True if nurse is detected
    detect_patient = False # True if patient is detected 
    
    patients = {} # List of patients ; patients = {patient : dict, patient : dict, patient : dict, patient : dict, patient : dict, patient : dict}
    patients_to_take_medication = {} # List of patients to take a medication 
    there_is_patient_need_to_take_medication = False # True if here is a patient need to take medication
    
    stop_proccess = False # True if we are stopping the procedure and we are not waiting for it to complete
    
    nurses = {} # List of nurses ; nurses = { nurse : dict, nurse : dict, nurse : dict, nurse : dict, nurse : dict, nurse : dict }
    
    schedules = {} # List of schedules for the patient 
    
    what_to_search = "nobody" # what to search for in the camera : all, patient, nurse, nobody , nurse, patient
    person_id = None # the id of the person we are searching for based on the database ( patient or nurses )
    
    is_searching = False # True if we are searching for something in the 
    
    search_patient_id = None # The id of the patient we are searching for
    search_nurse_id = None # The id of the nurse we are searching for
    
    api_action = "get_data" # get_data = Get the data , delete_data = Delete the schedule, taken_medication = Modify the data in server in taken
    
    
    
    no_pills_biogesic = False # no_pills_biogesic = True if there is no pills in biogesic
    no_pills_cremil_s = False # no_pills_cremil_s = True if there is no pills in cremil_s
    no_pills_citerizen = False # no_pills_citerizen = True if there is no pills in citerizen
    no_pills_mefenamic = False # no_pills_mefenamic = True if there is no pills in mefenamic
    
    
    list_of_patients_to_take = []
    """
    list_of_patients_to_take = [ patient_id, patient_id, ...]
    """
    
    
    def update_patients(self, patients):
        self.patients = patients
         
    def check_schedule(self):
        def event():
            while not self.close_down:
                for patient in self.patients:
                    # Loop through the patients
                    for schedule in patient["schedule"]:
                        # Check if schedule is today's scheduled
                        day : str = schedule["day"]
                        time_range_str : str = schedule["time"]
                        medication : str = schedule["medication"]

                        # Parse the time range
                        start_time_str, end_time_str = time_range_str.split(' - ')
                        start_time = datetime.datetime.strptime(start_time_str, "%I:%M %p").time()
                        end_time = datetime.datetime.strptime(end_time_str, "%I:%M %p").time()

                        # Get the current date and time
                        now = datetime.datetime.now()

                        # Combine the times with today's date
                        start_datetime = datetime.datetime.combine(now.date(), start_time)
                        end_datetime = datetime.datetime.combine(now.date(), end_time) + datetime.timedelta(minutes=30)

                        # Check if the current time is within the range and if the day matches
                        if day == now.strftime("%A") and start_datetime <= now <= end_datetime:
                            print("Patient " + patient["name"] + " is scheduled to take " + medication + " between " + time_range_str)
                            if patient["id"] not in self.patients_to_take_medication:  # Check if the patient is already in the list
                                self.patients_to_take_medication.append(patient["id"])  # Add patient to the list of patients to take medication
                                self.there_is_patient_need_to_take_medication = True

        
        
        
        
        threading.Thread(target=event).start()

    
    def person_take_medication(self, patient_id):
        if patient_id in self.patients_to_take_medication:
            self.patients_to_take_medication.remove(patient_id)
            self.there_is_patient_need_to_take_medication = True if self.patients_to_take_medication else False
            print("Patient " + patient_id + " has taken medication")
        else:
            print("Patient " + patient_id + " has not taken medication")



