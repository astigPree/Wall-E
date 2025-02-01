from speech_recognition_utils import SpeechRecognitionUtils
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from facial_recognition_utils import FacialRecognition
from events_handler import EventHandler
from database_handler import DataHandler
from arduino_connection import ArduinoConnection
from my_tools import text_to_dictionary , send_post_request, delete_schedule
from algorithm_handler import *
import rules 

import asyncio
import sys
import time
import threading
import os

# Set the event loop policy conditionally for Windows 
if sys.platform == 'win32': 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


OFFSET_MINUTE_TO_CALL_NAME = 10
OFFSET_MINUTE_TO_VALID = 20

database = DataHandler()
eyes = FacialRecognition()
voice = VoiceUtils()
recognizer = SpeechRecognitionUtils()
brain = BrainUtils()
# brain = None
event =  EventHandler()
arduino = ArduinoConnection()
# arduino.initialized()


async def sample_function():
    while True:
        text = recognizer.recognize_speech()
        if text:
            response = await brain.generate_response(text)
            print(f"The response is: {response}")
            voice.speak(response)  
            print(f"You said: {response}")
            print("--------------------------------")
        await asyncio.sleep(2)  # Add a short delay between iterations


def fetch_data(): 
    global database
    global eyes
    global voice
    global recognizer
    global brain
    global event
    global arduino
    
    event.list_of_patients_to_take = []
    """
    list_of_patients_to_take = [ patient_id, patient_id, ...]
    """
    
    while not event.close_down:
        
        time.sleep(1) # sleep for 1 second
        
        if event.api_action == "get_data":
            data = send_post_request()
            # print("\n\nHere is the data ;")
            # print(data)
            if data:
                # print(f"Received data: {data}")
                nurses = data.get('nurses', None)
                patients = data.get('patients', None)
                schedules = data.get('schedules', None)
                
                
                if nurses: 
                    database.write_image_nurses()
                if patients:
                    database.write_image_patients()
                 
                if nurses:
                    database.nurses = nurses
                
                if patients:
                    database.patients = patients
                     
                if schedules:
                    database.schedules = schedules
         
        # TODO: Create an algorithm that check the schedule of the patients
        # TODO: This is an important event and it should check the patient face to verify before despensing pills
        # TODO: This is an important event and it should shout the patients name so they will be notified
        for schedule_id , schedule in database.schedules.items():
            print(type(schedule))
            if schedule.get('set_date' , None):
                
                date_sched = my_tools.check_date_status(schedule.get('set_date' )) 
                print("Date scheduled is in the ", date_sched)
                if date_sched == "Past":
                    # If the schedule is not current date, then we need to skip the action 
                    threading.Thread(target=delete_schedule, args=(schedule_id,)).start() # delete the scheduled that already executed
                    continue
                
            if schedule.get('set_time', None):
                
                time_sched = my_tools.check_time_status(schedule.get('set_time') , OFFSET_MINUTE_TO_VALID)
                
                print("Time scheduled is in the ", time_sched)
                
                if time_sched == "Past": 
                    # If the schedule is not current time, then we need to skip the action
                    continue
                if time_sched == "Future": 
                    # If the schedule is not current time, then we need to skip the action
                    continue
            
            patient_id = schedule.get('patient_id' , None)
            if patient_id is None:
                print("Schedule has no patient_id")
                continue
            
            patient_data = database.patients.get(patient_id)
            if not patient_data:
                print(f"Patient {patient_data.get('id')} not found in database")
                continue
            
            if patient_id not in event.patients_to_take_medication:
            
                print(f"Patient {patient_id} is not in list of patients to take medication, so adding it.")
                event.patients_to_take_medication.append(patient_id)
                
            
            # event.has_important_event = True 
            # patient = database.patients.get(schedule.patient)
            # # TODO : Check if nasa list_of_patients_to_take then skip it
            # if patient:
            #     # TODO: I check kung meron pills ang selected medication
            #     # TODO : Check if lumampas na an specific time na mag take san pills ma send san text message na wra katumar san bulong
            #     voice.speak(f"{patient.get('name', 'No name Patient!')} IT'S TIME TO TAKE YOUR {schedule.get('pill' , 'PILLS').upper()}! DON'T FORGET YOUR MEDICATION!")
            # event.has_important_event = False
        
        
        # ----------------------------------------------------------------
        # TODO: Create an algorithm that actionas the event.list_of_patients_to_take
        print("Starting the main event loop")
        print("These are the ids of the patiens to take medication : ", event.list_of_patients_to_take)

def eyes_loop():
     
    global database
    global eyes
    global voice
    global recognizer
    global brain
    global event
    
    eyes.start_camera()
    
    
    
    while not event.close_down:
        
        if not event.open_eyes:
            continue
        
        
        
        frame = eyes.get_face_by_camera()
        if frame is not None:
            
            if event.activate_scanning and (database.patients or database.nurses): 
                eyes.number_to_try_detection += 1
                
                if event.what_to_search == "patient": 
                    patient_data = database.patients.get(event.person_id)
                    if not patient_data:
                        print(f"Patient {event.person_id} not found in database")
                        continue
                    filename = my_tools.extract_filename(patient_data.get('face')) 
                    if filename:
                        patient_face_path = os.path.join(database.patients_image_path, filename)
                        if not event.has_face_scanned:
                            event.has_face_scanned = eyes.check_face_exists_in_database(face_image=frame, face_in_database=patient_face_path)
                        if not event.detect_patient:
                            event.detect_patient = True if event.has_face_scanned else False
                            event.search_patient_id = patient_id
                
                if event.what_to_search == "nurse":
                    print("Start Scanning Nurses")
                    nurse_data = database.nurses.get(event.person_id)
                    if not nurse_data:
                        print(f"Nurse {event.person_id} not found in database")
                        continue
                    filename = my_tools.extract_filename(nurse_data.get('face')) 
                    if filename:
                        nurse_face_path = os.path.join(database.nurses_image_path, filename)
                        if not event.has_face_scanned:
                            event.has_face_scanned = eyes.check_face_exists_in_database(face_image=frame, face_in_database=nurse_face_path)
                        if not event.detect_nurse:
                            event.detect_nurse = True if event.has_face_scanned else False
                            event.search_nurse_id = nurse_id
                    
                
                if event.what_to_search == "all" or event.what_to_search == "patient":
                    print("Start Scanning Patients")
                    for patient_id , patient_data in database.patients.items():
                        if event.stop_proccess:
                            break
                        if not event.is_searching:
                            break 
                        filename = my_tools.extract_filename(patient_data.get('face')) 
                        if filename:
                            patient_face_path = os.path.join(database.patients_image_path, filename)
                            if not event.has_face_scanned:
                                event.has_face_scanned = eyes.check_face_exists_in_database(face_image=frame, face_in_database=patient_face_path)
                            if not event.detect_patient:
                                event.detect_patient = True if event.has_face_scanned else False
                                event.search_patient_id = patient_id
                
                if event.what_to_search == "all" or event.what_to_search == "nurse":
                    print("Start Scanning Nurses")
                    for nurse_id , nurse_data in database.nurses.items():
                        if event.stop_proccess:
                            break
                        if not event.is_searching:
                            break  
                        filename = my_tools.extract_filename(nurse_data.get('face')) 
                        if filename:
                            nurse_face_path = os.path.join(database.nurses_image_path, filename)
                            if not event.has_face_scanned:
                                event.has_face_scanned = eyes.check_face_exists_in_database(face_image=frame, face_in_database=nurse_face_path)
                            if not event.detect_nurse:
                                event.detect_nurse = True if event.has_face_scanned else False 
                                event.search_nurse_id = nurse_id
                            
        time.sleep(0.5)


def check_schedule(): 
    global database
    global eyes
    global voice
    global recognizer
    global brain
    global event
    
    while not event.close_down:
        pass


async def main_loop():
    
        
    global database
    global eyes
    global voice
    global recognizer
    global brain
    global event
    global arduino
    
    threading.Thread(target=fetch_data).start()
    # threading.Thread(target=eyes_loop).start() # For facial recognition
    while True:
        time.sleep(1)
    
    while not event.close_down: 
        
        if event.has_important_event:
            time.sleep(0.5)
            continue
        
        text = recognizer.recognize_speech()
        print(f"Text received: {text}")
        if text and not event.has_important_event:
            response = await brain.generate_response(rules.rule_for_identifiying_command.format(text=text))
            print(f"The response is: {response}")
            data : dict = text_to_dictionary(response)
            if data is not None:
                # data = { action , message, data }
                
                if data.get('action') == '5' or data.get('action') == 5 and not event.has_important_event:
                    talk_data = algo_user_want_to_talk(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                    action = talk_data.get('action', None)
                    if action is not None:
                        data['action'] = action
                    
                    message = talk_data.get('message', None)
                    if message is not None:
                        data['message'] = message
                    
                    
                
                if data.get("action") == "1" or data.get("action") == 1 and not event.has_important_event:
                    algo_machine_walk(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                
                if data.get('action') == '2' or data.get('action') == 2 and not event.has_important_event:
                    algo_open_back_of_the_machine(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                
                if data.get('action') == '3' or data.get('action') == 3 and not event.has_important_event:
                    algo_check_for_schedules(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                
                if data.get('action') == '4' or data.get('action') == 4 and not event.has_important_event:
                    algo_check_body_temperature(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                
                
                
                if data.get('action') == '6' or data.get('action') == 6 and not event.has_important_event:
                    algo_user_command_not_exist(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                
                if data.get('action') == '7' or data.get('action') == 7 and not event.has_important_event:
                    algo_close_the_back_of_the_machine(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data,
                        user_command=text
                    )
                
                
                voice.speak("Sorry, I think there is a problem. Please try again later.")

            
        await asyncio.sleep(0.5)  # Add a short delay between iterations
    
    
    
    

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Interrupted by user.")
        event.close_down = True
        eyes.close_camera()
    except RuntimeError as re:
        print(f"An error occurred: {re}") 
    except Exception as e:
        print(f"An error occurred: {e}")
        event.close_down = True
        eyes.close_camera()
    finally:
        event.close_down = True
        # Safely close the event loop
        try:
            eyes.close_camera()
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                loop.close()
        except RuntimeError as re:
            print(f"Error closing event loop: {re}")
            eyes.close_camera()
        except Exception as e:
            print(f"An error occurred while closing event loop: {e}")
            
