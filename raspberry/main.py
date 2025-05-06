
from speech_recognition_utils import SpeechRecognitionUtils
from my_tools import text_to_dictionary , send_post_request, delete_schedule
from database_handler import DataHandler
from brain_utils import BrainUtils
from voice_utils import VoiceUtils
from events_handler import EventHandler
from facial_recognition_utils import FacialRecognition
from arduino_connection import ArduinoConnection
import algorithm_handler as algo
import rules
import static_generated_txt
import my_tools
import os
import time
import threading
import random 
import asyncio
import sys   



# sys.setrecursionlimit(2097152)    # adjust numbers
# threading.stack_size(134217728)   # for your needs

# Set the event loop policy conditionally for Windows 
if sys.platform == 'win32': 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
      

OFFSET_MINUTE_TO_CALL_NAME = 10
OFFSET_MINUTE_TO_VALID = 20

event = EventHandler()
database = DataHandler()
ear = SpeechRecognitionUtils()
brain = BrainUtils()
voice = VoiceUtils()
arduino = ArduinoConnection()
arduino.initialized()

is_machine_open = False
listening_thread : threading.Thread = None
fetching_strike = 0 

def start_listening():
    global ear  
    global voice
    global event
    try: 
        while not event.close_down and not event.down_recording:
            if not voice.is_playing:
                print("Waiting for voice command...")
                event.is_recording = True
                text = ear.recognize_speech()
                if text is not None:
                    if not voice.is_playing:
                        event.user_commands.append(text)
                        print("================================")
                        print("Commands : " , event.user_commands)
                        print("================================")
                    event.is_recording = False
                    print(f"Text received: {text}")
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        event.close_down = True
        time.sleep(1)
    print("================ End of listening thread =================")
        

def main():
    global event 
    global listening_thread
    global is_machine_open
    global arduino
    global fetching_strike
    # if listening_thread is None:
    #     print("Starting listening thread...")
    #     listening_thread = threading.Thread(target=start_listening)
    #     listening_thread.start()
    decided_command = None
    prio_command = len(event.user_commands) > 0 and not event.has_important_event
    if len(event.user_commands) > 0:
        # print("Starting to analyze the commands...")
        
        user_overall_commands = " ~ ".join(event.user_commands)
        print("Applying commands : ", user_overall_commands)
        # generated_response = brain.generate_response(rules.rule_for_identifiying_command % user_overall_commands)
        # print("Generated response by gpt4free: ", generated_response)
        # decided_command : dict = text_to_dictionary(generated_response)
        # print("Generated response by gpt4free: ", decided_command)
        # if not decided_command:
        voice.speak("Proccessing Command! Wait a moment!")
        generated_response = brain.generate_cohere_response(user_overall_commands , rules.rule_for_identifiying_command % user_overall_commands)
        print("Generated response by cohere: ", generated_response)
        decided_command : dict = text_to_dictionary(generated_response)
        print("Generated response by cohere: ", decided_command)
        
        # print("Decided command : ", decided_command)
        if not decided_command:
            voice.speak(random.choice(static_generated_txt.list_of_not_recognized_commands_text))
            event.user_commands = []
            return
        
        
        
        if decided_command.get('action') == "2" or decided_command.get('action') == 2:
            # TODO: Simulate talking to the user based on it question
            # print("This should be the user talking")
            decided_command = algo.algo_user_want_to_talk(
                event=event,
                voice=voice,
                brain=brain,
                recognizer=ear,
                data=decided_command,
                user_command=user_overall_commands
            )
        

        if decided_command.get('action') == "1" or decided_command.get('action') == 1:
            # TODO: Simulate the checking of body temperature
            # print("Checking body temperature")
            algo.algo_check_body_temperature(
                event=event,
                voice=voice,
                brain=brain,
                data=decided_command,
                arduino=arduino
            )
        elif decided_command.get('action') == "3" or decided_command.get('action') == 3:
            # TODO: Simulate repeating the questions
            message = decided_command.get('message' , random.choice(static_generated_txt.list_of_not_recognized_commands_text))
            voice.speak(message)
        elif decided_command.get('action') == "4" or decided_command.get('action') == 4:
            # TODO: Simulate closing the back of the machine
            # print("Closing the back of the machine")
            # algo.algo_close_the_back_of_the_machine(
            #     event=event,
            #     voice=voice, 
            #     brain=brain,
            #     recognizer=ear,
            #     arduino=arduino,
            #     data=decided_command,
            #     user_command=user_overall_commands
            # )
            arduino.write("DRAWER")
            time_start = time.time()
            while time.time() - time_start < 10:
                if event.stop_proccess:
                    break
                result = arduino.read()
                if "CLOSE" in result :
                    is_machine_open = False
                    break
                if "OPEN" in result:
                    is_machine_open = True
                    break
                time.sleep(0.1)
                
            if is_machine_open:
                voice.speak(decided_command.get("message", "Wait, I will slowly close the pills drawers."))
                arduino.write("LOCK")
                time_start = time.time()
                while time.time() - time_start < 10:
                    if event.stop_proccess:
                        break
                    if "LOCK" in arduino.read():
                        break
                    time.sleep(0.1)
                is_machine_open = True
            else:
                voice.speak("The pills drawers are already closed.")
            
            # TODO: Create a logic that connect arduino and close the back of the machine
        
        elif decided_command.get('action') == "5" or decided_command.get('action') == 5:
            arduino.write("DRAWER")
            time_start = time.time()
            while time.time() - time_start < 10:
                if event.stop_proccess:
                    break
                result = arduino.read()
                if "CLOSE" in result :
                    is_machine_open = False
                    break
                if "OPEN" in result:
                    is_machine_open = True
                    break
                time.sleep(0.1)
                
            if not is_machine_open:
                voice.speak(decided_command.get("message", "Wait, I will slowly open the pills drawers."))
                arduino.write("UNLOCK")
                time_start = time.time()
                while time.time() - time_start < 10:
                    if event.stop_proccess:
                        break
                    if "UNLOCK" in arduino.read():
                        break
                    time.sleep(0.1)
                is_machine_open = False
            else:
                voice.speak( "The pills drawers are already open.")
                
        
        elif decided_command.get('action') == "6" or decided_command.get('action') == 6:
            # TODO: Simulate the dispensing of pills 
            # print("Dispensing pills")
            pills_response = brain.generate_cohere_response(command=user_overall_commands , system=rules.rules_for_identifying_pills_system)
            pills_command : dict = text_to_dictionary(pills_response) 
            if not isinstance(pills_command, dict):
                voice.speak(random.choice(static_generated_txt.list_of_not_recognized_commands_text))
            else:
                pill = pills_command.get('pill', 'N')
                if pill != 'N':
                    voice.speak(pills_command.get('message', "Wait, I will dispense the pills"))
                    # print("[!] Start pills dispensing...")  
                    # Drop the selected pills  
                    arduino.write(pill) 
                    # print("[!] Start to check if the pills is dispensed...")
                    # Wait for 10 seconds to check if the pills is dispensed
                    start_time = time.time()  
                    while time.time() - start_time < 60:  # 10 seconds timeout
                        if event.stop_proccess:
                            break
                        if "DROP" in arduino.read(): 
                            break
                        time.sleep(0.1) 
                else:
                    voice.speak(pills_command.get('message', "I didn't understand which pill you want to dispense."))
                    
                     
        
        event.user_commands = []
        

    if prio_command and fetching_strike != 0:
        if (fetching_strike + 1) > 1 and (fetching_strike + 1) < 5:
            fetching_strike += 1
            return
        else:
            fetching_strike = 1
    else:
        fetching_strike = 1
    
    data = send_post_request()
    if data:
        # # print(f"Received data: {data}")
        nurses = data.get('nurses', None)
        patients = data.get('patients', None)
        schedules = data.get('schedules', None)
        
        
        if nurses: 
            database.write_image_nurses()
        if patients:
            print("====================")
            database.write_image_patients()
            print("====================")
        
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
            # print(schedule)
            
            if schedule_id in event.done_schedule:
                # print(f"Schedule {schedule_id} has already been executed")
                threading.Thread(target=delete_schedule, args=(schedule_id,)).start() # delete the scheduled that already executed
                continue
            
            if schedule_id in event.pending_schedule:
                # print(f"Schedule {schedule_id} is already in pending state")
                continue
            
            if schedule.get('set_date' , None):
                
                date_sched = my_tools.check_date_status(schedule.get('set_date' )) 
                # print("Date scheduled is in the ", date_sched)
                if date_sched == "Past":
                    # If the schedule is not current date, then we need to skip the action 
                    threading.Thread(target=delete_schedule, args=(schedule_id,)).start() # delete the scheduled that already executed
                    continue
                
            if schedule.get('set_time', None):
                
                time_sched = my_tools.check_time_status(schedule.get('set_time') , OFFSET_MINUTE_TO_VALID)
                
                # print("Time scheduled is in the ", time_sched)
                
                if time_sched == "Past": 
                    # If the schedule is not current time, then we need to skip the action
                    continue
                if time_sched == "Future": 
                    # If the schedule is not current time, then we need to skip the action
                    continue
            
            
            
            
            patient_id = schedule.get('patient' , None)
            if patient_id is None:
                # print("Schedule has no patient_id")
                continue
            
            # print("Patients Database : ", database.patients)
            patient_data : dict = database.patients.get(str(patient_id))
            if not patient_data:
                # print(f"Patient {patient_id} not found in database")
                continue
            
            if patient_id not in event.patients_to_take_medication:
                # print(f"Patient {patient_id} is not in list of patients to take medication, so adding it.")
                event.patients_to_take_medication[str(patient_id)] = patient_data
            
            if schedule_id not in event.pending_schedule:
                event.pending_schedule.append(schedule_id)
                event.list_of_schedule_to_take.append(schedule)
                
            
            # event.has_important_event = True 
            # patient = database.patients.get(schedule.patient)
            # # TODO : Check if nasa list_of_schedule_to_take then skip it
            # if patient:
            #     # TODO: I check kung meron pills ang selected medication
            #     # TODO : Check if lumampas na an specific time na mag take san pills ma send san text message na wra katumar san bulong
            #     voice.speak(f"{patient.get('name', 'No name Patient!')} IT'S TIME TO TAKE YOUR {schedule.get('pill' , 'PILLS').upper()}! DON'T FORGET YOUR MEDICATION!")
            # event.has_important_event = False
        
        
        # ----------------------------------------------------------------
        # TODO: Create an algorithm that actionas the event.list_of_schedule_to_take
        # print("Starting the main event loop")
        print("These are the ids of the patiens to take medication : ", event.list_of_schedule_to_take)

    if len(event.list_of_schedule_to_take) < 1:
        # Do nothing if there are no schedules to take for the day
        return None

    event.has_important_event = True
    has_medications_to_serve = True if len(event.list_of_schedule_to_take) > 0 else False
    
    # TODO: Apply walking here using arduino
    has_reached = False
    if has_medications_to_serve:
        voice.speak("Please excuse me for a moment while I prepare for the medication of the patients")
        has_reached = algo.algo_machine_walk( 
            event = event,  
            arduino = arduino
        )
        
    while len(event.list_of_schedule_to_take) > 0:
        schedule = event.list_of_schedule_to_take.pop(0)
        patient_id = schedule.get('patient' , None)
        if patient_id is None:
            # print("Schedule has no patient_id")
            continue
        patient : dict = database.patients.get(str(patient_id))
        if not patient:
            # print(f"Patient {patient_id} not found in database")
            continue
        
        # TODO: Apply walking here using arduino
        # voice.speak("Walking is currently not supported! Please wait for further updates")
        # Uncomment when the waling is implemented
        schedule['color'] = patient.get('color' , 'RED') 
        
        if not has_reached:
            # Faild to walk to the patient location
            print("Failed to walk to patient")
            message = my_tools.SMS_NOT_TAKEN_MEDICATION_TEXT.format(
                patient_name = patient.get('name' , 'No name'), 
                schedule_time = schedule.get('set_time' , 'No time'), 
                pill = schedule.get('pill' , 'No pill')
            )
            my_tools.send_message(message , patient.get('phone_number' , None))
            continue

        # Identify the face of the user before dropping the pills
        schedule['patient_name'] = patient.get('name' , 'Patient'),
        # schedule['patient_data'] = patient

        # print("[!] Start Camera for pills identification...")
        voice.speak(schedule.get('message', 'if you are a patient and say "Yes" if you are ready while looking at the camera'))
        event.activate_scanning = True
        event.open_eyes = True
        
        timeout = 180  # Timeout duration in seconds (3 minutes)
        start_time = time.time()
        not_received = False
        while event.is_recording or len(event.user_commands) < 1:
            time.sleep(0.5)
            if event.stop_proccess:
                return False
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                # print("3 minutes have passed, returning default response: {}")
                voice.speak(schedule.get('message', 'I think you are not ready to receive the medication. Please try again later'))
                not_received = False  # Automatically return {} if timeout is exceeded
            # print("Waiting for event to be recorded or user commands to be added")
            # it_has_yes = False
            for command in event.user_commands:
                if "yes" in command.lower():
                    # it_has_yes = True
                    not_received = True
                    break
            # if it_has_yes:
            #     # print("User confirmed, starting identification process...")
            #     if listening_thread is not None:
            #         # event.down_recording = True
            #         # listening_thread.join()
            #         # listening_thread = None
            #         print("Down recording")
            #     else:
            #         print("No listening thread found, skipping identification process...")
            #     time.sleep(0.5)
            #     break
        
        if not not_received: 
            continue
        
    
        voice.speak(schedule.get('message', 'Now please face my camera so i can see you if you are the patient'))
        # Find extact face for 5 mins 
        
        start_time = time.time()
        last_speak_time = start_time  # Track the last time the reminder was spoken
        while time.time() - start_time < 300:  # 5 mins timeout
            try:
                if event.stop_proccess:
                    event.activate_scanning = False
                    event.open_eyes = False
                    return False

                frame = eyes.get_face_by_camera()
                if frame is None:
                    # print("Can't Find Face =================")
                    continue

                # print("Try To Find Face =================")
                # Resize the frame immediately after capturing it 
                
                conver_frame_to_rgb = frame
                # conver_frame_to_rgb = eyes.conver_frame_to_rgb(frame)
                # Validate and process the frame
                # patient : dict = schedule.get('patient_data', None)
                if patient is None:
                    raise ValueError("Patient data is missing or invalid.")
                face = patient.get('face', None)
                # print("Check Face =================")
                if face is None:
                    raise ValueError("Face data is missing or invalid.")
                filename = my_tools.extract_filename(face)
                # print(f"Face image file: {filename}")
                if filename:
                    patient_face_path = os.path.join(database.patients_image_path, filename)
                    try:
                        event.has_face_scanned = eyes.check_face_exists_in_database(
                            face_image=conver_frame_to_rgb, face_in_database=patient_face_path
                        )
                    except Exception as e:
                        print(f"Error during face scanning: {e}")
                    print(f"Has face scanned: {event.has_face_scanned}")
                    if event.has_face_scanned:
                        event.detect_patient = True
                        break

                # Speak reminders every 60 seconds
                if time.time() - last_speak_time >= 60:
                    voice.speak(f"Please take your medicine! {schedule.get('patient_name', 'Patient!')}")
                    last_speak_time = time.time()

                # print("[!] Try To Find Face...")
                time.sleep(0.1)
            except Exception as e:
                print(f"Error during face scanning: {e}")
                event.activate_scanning = False
                event.open_eyes = False
            

        if not event.has_face_scanned:
            # print("Failed to find face after 5 minutes")
            voice.speak('I think you are not ready to receive the medication. Please try again later')
            continue
        
        # TODO: Implement the machine drop pills here using arduino
        is_dropped = algo.algo_machine_drop_pills(
            event = event, database=database, 
            voice = voice , brain = brain, 
            recognizer = ear , arduino = arduino, 
            eyes = eyes, data = schedule, 
        )
        
        
        
        if not is_dropped:
            # Faild to drop the pills
            # print("Failed to drop the pills")
            message = my_tools.SMS_MAYBE_TAKEN_OR_NOT_NEED_TO_VERIFY_TEXT.format(
                patient_name = patient.get('name' , 'No name'), 
                schedule_time = schedule.get('set_time' , 'No time'), 
                pill = schedule.get('pill' , 'No pill')
            )
            my_tools.send_message(message , patient.get('phone_number' , None))
        else:
            message = my_tools.SMS_TAKEN_MEDICATION_TEXT.format(
                patient_name = patient.get('name' , 'No name'), 
                schedule_time = schedule.get('set_time' , 'No time'), 
                pill = schedule.get('pill' , 'No pill')
            )
            my_tools.send_message(message , patient.get('phone_number' , None))

        # print("Sent message to patient")
        event.user_commands = []
        time.sleep(0.5)
        # listening_thread = threading.Thread(target=start_listening)
        # listening_thread.start() # start listening in a separate thread
        
    
    # TODO: Apply walking here using arduino going back to its original position
    if has_reached:
        voice.speak("I will now walk back to my original position, please excuse me")
        arduino.write("STEP")
        time.sleep(2) # Give Arduino time to process and respond
        arduino.write("BACK")
        start_time = time.time()
        while time.time() - start_time < 1800:  # 30 mins timeout
            if "ARRIVED" in arduino.read():
                break
            if event.stop_proccess:
                break
            time.sleep(0.1)
    
    event.has_important_event = False
    if has_medications_to_serve:
        voice.speak("I have finished serving all medications. Im available to your inquiries")

if __name__ == '__main__': 
    # generated_response = brain.generate_cohere_response(rules.rules_for_introduction , rules.rules_for_introduction)
    # print("Generated response by cohere: ", generated_response)
    # decided_command : dict = text_to_dictionary(generated_response)
    decided_command = None
    # print("Generated response by cohere: ", decided_command)
    if isinstance(decided_command, dict):
        introduction = decided_command.get("message" , "Hello, I am Pill-ar, your advanced healthcare assistant. I am here to ensure you take the right dosage of your medication at the correct time, monitor your body temperature for your well-being, and securely recognize you using facial recognition. You can interact with me easily through voice commands, and I automate several healthcare and patient management tasks to make your life smoother. How may I assist you today?")
    else:
        introduction = "Hello, I am Pill-ar, your advanced healthcare assistant. I am here to ensure you take the right dosage of your medication at the correct time, monitor your body temperature for your well-being, and securely recognize you using facial recognition. You can interact with me easily through voice commands, and I automate several healthcare and patient management tasks to make your life smoother. How may I assist you today?"
    voice.speak(introduction)
    time.sleep(1)
    listening_thread = threading.Thread(target=start_listening)
    listening_thread.start() # start listening in a separate thread
    time.sleep(1)
    
    eyes = FacialRecognition()
    eyes.start_camera()
    # time.sleep(1)
    # # Check arduino connection if there is an error for 10 second
    # time_start = time.time()
    # while time.time() - time_start < 10: 
    #     if "ERROR" in arduino.read():
    #         voice.speak("There is an error in the arduino connection. Please check the connection so I can work properly")
    #         voice.speak("I will now shutdown and please restart the program so I can work properly")
    #         event.close_down = True
    #         break
    #     time.sleep(0.1) 
    
    try:
        while not event.close_down:
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            print("Starting to analyze the commands...")
            main()
            time.sleep(.5)
    except KeyboardInterrupt:
        print("Interrupted by user.")
        event.close_down = True
    except Exception as e:
        event.close_down = True
        print(f"An error occurred: {e}")
    
    
