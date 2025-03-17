from events_handler import EventHandler
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from database_handler import DataHandler
from speech_recognition_utils import SpeechRecognitionUtils
from facial_recognition_utils import FacialRecognition
from arduino_connection import ArduinoConnection
import time
from rules import *
import my_tools

SCANNING_FACIAL_RECOGNITION_TIMEOUT = 50 # seconds timeout in seconds for processing face recognition  
COMPARING_FACIAL_RECOGNITION_TIMEOUT = 2 # number of tries to compare the face recognition
RECORDING_VOICE_TIMEOUT = 3 # number of tries to recording the voice recognition



def algo_open_back_of_the_machine(
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict,
    user_command : str
    ):
    # 2. User want to open the back of the machine or add a pills in the machine.
    # 3. Senario in putting pills (NURSEs);
    #     - The user will ask the machine to open the back of the machine.
    #     - The machine will scan the face of the user.
    #     - If the user is not in the database the machine will not open the back of the machine.
    #     - If the user is in the database the machine will open the back of the machine.
    #     - The stepper motor will go back to its original position.
    #     - The user will put the pills in the pill slot.
    #     - The user will close the back of the machine.
    #     - The user ask the machine to close the back of the machine for security.
    
    speech_recognizer_maximum_retry = 10 # seconds timeout in seconds for processing speech recognition
    brain_maximum_retry = 5 # seconds timeout in seconds for processing brain recognition
    if event.stop_proccess:
        return
    
    response = None
    
    name = data.get('data', {}).get('name', '')
    message = data.get('message', "Can you provide your name so that I can recognize you")
    if not name:
        # If the name is not specified then the user will be talk the machine his name
        voice.speak(message)
        time.sleep(5)
        for retry in range(speech_recognizer_maximum_retry):
            if event.stop_proccess:
                return
            name += recognizer.recognize_speech()
            if len(name) > 10 or (retry > 2 and name != ''):
                break
    # If the name is not specified then the user will not to talk to the machine
    if not name:
        voice.speak("I think you don't cooperate yourself with this message and will not be able to talk to you")
        return
    
    
    options = db.generate_id_and_name_of_nurses()
    options += db.generate_id_and_name_of_patients()
    
    while not response and brain_maximum_retry > 0:
        if event.stop_proccess:
            return
        response = brain.generate_response(rule_for_identifiying_id_by_name.format(text=name , options=options)) 
        brain_maximum_retry -= 1
        
    # DATA : response = { 
    #       "data" : [ "patient-1", "nurse-1"], 
    #       "invalid" : "I'm sorry but I can't find you in the database"
    #       "success" : "Wait i will open the back of the machine "
    # }
    if not response:
        voice.speak("Im sorry for that but I can't find you in the database. Please try again later")
        return
    
    convert_response_to_list = my_tools.my_tools.text_to_dictionary(response)
    if not convert_response_to_list:
        voice.speak("I'm sorry but I can't process right now because there was a problem processing the response. Please try again later")
        return
    
    voice.speak(data.get('message', 'Please face my camera so i can see you if you are a nurse'))
    
    # Scanning face recognition
     
    event.activate_scanning = True
    event.open_eyes = True
    event.what_to_search = "nurse" 
    event.is_searching = True
    
    # TODO : Create an algorithm that will scan the face of based on the data before procceding below 
    while not event.has_face_scanned and eyes.number_to_try_detection < COMPARING_FACIAL_RECOGNITION_TIMEOUT:
        if event.stop_proccess:
            return
        time.sleep(0.5)
        
    event.is_searching = False
    event.activate_scanning = False 
    eyes.number_to_try_detection = 0
    
    if event.has_face_scanned and event.detect_nurse:
        voice.speak(data.get('success', "Wait i will open the back so you can put the pills in the machine"))
        event.activate_scanning = False 
        # TODO : Create an algorithm that will open the back of the machine
        return
    else :
        voice.speak(data.get('invalid', "I'm sorry but I can't find you in the database or you are not a nurse")) 
        return
    

def algo_machine_walk(
    event : EventHandler , 
    voice : VoiceUtils ,  
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils ,  
    arduino : ArduinoConnection,
    eyes : FacialRecognition,
    data : dict):
    
    # 8. Senario in making the machine walk;
    # - The user will ask the machine to move.
    # - The machine will identify what position and where to go.
    # - The machine will move to the position and where to go.
     
    if event.stop_proccess:
        return False
    
    # Goto the located position based on the color
    arduino.write(data.get('color', 'RED').encode())
    # Check if the arduino is in the location already and timeout for 30 mins
    start_time = time.time()
    machine_already_in_location = False
    while time.time() - start_time < 1800:  # 30 mins timeout
        if event.stop_proccess:
            return False
        if arduino.read() == "ARRIVED":
            machine_already_in_location = True
            break
        time.sleep(0.1)
    
    # If the arduino does not arrive in the location in 30 mins then the machine will not move
    if not machine_already_in_location:
        arduino.write("BACK".encode()) # Write the Arduino to go back to its original location
        voice.speak("I'm sorry but i did not arrive in the location in 30 mins. Please try again later")
        return False
    
    return True

def algo_machine_drop_pills(
    event : EventHandler , 
    voice : VoiceUtils ,  
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils ,  
    arduino : ArduinoConnection,
    eyes : FacialRecognition,
    database : DataHandler,
    data : dict):
     
    if event.stop_proccess:
        return False
    
    
    eyes.start_camera()
    voice.speak(data.get('message', 'Please face my camera so i can see you if you are a patient'))
    event.activate_scanning = True
    event.open_eyes = True
    
    # Find extact face for 5 mins
    start_time = time.time()
    while time.time() - start_time < 300:  # 5 mins timeout
        if event.stop_proccess:
            event.activate_scanning = False
            event.open_eyes = False
            return False
        frame = eyes.get_face_by_camera()
        if frame is not None:
            patient = database.patients.get(data.get('patient', '-1'), data.get('patient', '-1'))
            filename = my_tools.extract_filename(patient.get('face')) 
            if filename:
                patient_face_path = os.path.join(database.patients_image_path, filename)
                event.has_face_scanned = eyes.check_face_exists_in_database(face_image=frame, face_in_database=patient_face_path)
                if event.has_face_scanned:
                    event.detect_patient = True
                    break
        time.sleep(0.1)
        
    pill = data.get('pill', 'Biogesic')
    # Drop the selected pills 
    if pill == 'Biogesic':
        voice.speak('Please wait while i dispense the Biogesic pills')
        arduino.write("B".encode())
    elif pill == 'Cremil S':
        voice.speak('Please wait while i dispense the Cremil S pills')
        arduino.write("S".encode())
    elif pill == 'Citerizen':
        voice.speak('Please wait while i dispense the Citerizen pills')
        arduino.write("C".encode())
    elif pill == 'Mefenamic':
        voice.speak('Please wait while i dispense the Mefenamic pills')
        arduino.write("M".encode())
    
    # Wait for 10 seconds to check if the pills is dispensed
    start_time = time.time()
    pill_has_drop = False
    while time.time() - start_time < 10:  # 10 seconds timeout
        if event.stop_proccess:
            return False
        if arduino.read() == "DROP":
            pill_has_drop = True
            break
        time.sleep(0.1)
    
    if not pill_has_drop:
        return False
    
    
    # Go back the arduino and check if the 30 minutes have passed 
    arduino.write("BACK")
    start_time = time.time()
    while (time.time() - start_time) < 1800:  # 30 mins timeout
        if event.stop_proccess:
            event.activate_scanning = False
            event.open_eyes = False
            event.has_face_scanned = False
            event.detect_patient = False
            return True
        if arduino.read() == "ARRIVED":
            break 
        time.sleep(0.1)
    
    event.activate_scanning = False
    event.open_eyes = False
    event.has_face_scanned = False
    event.detect_patient = False
    
    return True
    
def algo_check_for_schedules(
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict,
    user_command : str
    ):
    # 4. Senario in taking pills (PATIENTs);
    # - The user will ask the machine to dispense the pills;
    # - The machine will scan the face of the user.
    # - If the user is not in the database the machine will not dispense the pills.
    # - If the user is in the database the machine will check if the user can take the pills by their schedule.
    # - If the user can take the pills the machine will dispense the pills.

    # 5. Senario in taking pills (Machine will);
    # - The machine will check the schedule of the pills.
    # - If the there is a schedule the machine will speak the schedule and who will take the pills.
    # - If there is no schedule the machine will not speak anything.
    # - The patient must ask the machine to move or patient must move to closest place to the machine.
    # - If the patient is in the closest place to the machine the machine will scan the face of the patient.
    # - If the patient is not in the closest place to the machine the machine will not scan the face of the patient.
    # - If the patient is in the database the machine will dispense the pills. 
    
    speech_recognizer_maximum_retry = 10 # seconds timeout in seconds for processing speech recognition
    brain_maximum_retry = 5 # seconds timeout in seconds for processing brain recognition
    if event.stop_proccess:
        return
     
     
    name = data.get('data', {}).get('name', '')
    message = data.get('message', "Can you provide your name so that I can recognize you")
    if not name:
        # If the name is not specified then the user will be talk the machine his name
        voice.speak(message)
        time.sleep(5)
        for retry in range(speech_recognizer_maximum_retry):
            if event.stop_proccess:
                return
            name += recognizer.recognize_speech()
            if len(name) > 10 or (retry > 2 and name != ''):
                break
    
    # If the name is not specified then the user will not to talk to the machine
    if not name:
        voice.speak("I think you don't cooperate yourself with this message and will not be able to talk to you")
        return
    
    options = db.generate_id_and_name_of_nurses()
    options += db.generate_id_and_name_of_patients()
    
    while not response and brain_maximum_retry > 0:
        if event.stop_proccess:
            return
        response = brain.generate_response(rule_for_identifiying_id_by_name.format(text=name , options=options)) 
        brain_maximum_retry -= 1
        
    # DATA : response = { 
    #       "data" : [ "patient-1", "nurse-1"], 
    #       "invalid" : "I'm sorry but I can't find the named in the database",
    #       "success" : "Here are the schedules for the pills"
    # }
    
    if not response:
        voice.speak("Im sorry for that but I can't find you in the database. Please try again later")
        return
    
    convert_response_to_list = my_tools.my_tools.text_to_dictionary(response)
    if not convert_response_to_list:
        voice.speak("I'm sorry but I can't process right now because there was a problem processing the response. Please try again later")
        return
    
    voice.speak(data.get('message', 'Please face my camera so i can see you if you are a nurse or a patient'))
    
    # Scanning face recognition
    
    event.activate_scanning = True
    event.open_eyes = True
    event.what_to_search = "all" 
    event.is_searching = True
    
    # TODO : Create an algorithm that will scan the face of based on the data before procceding below
    while not event.has_face_scanned and eyes.number_to_try_detection < COMPARING_FACIAL_RECOGNITION_TIMEOUT:
        if event.stop_proccess:
            return
        time.sleep(0.5)
        
    event.is_searching = False
    event.activate_scanning = False 
    eyes.number_to_try_detection = 0
    
        
    if event.has_face_scanned and (event.detect_nurse or event.detect_patient):
        event.activate_scanning = False 
        peoples = response.get('data', None)
        if not peoples:
            voice.speak("I'm sorry but I can't find any patient or nurse in the database in the name you are looking for. Please try again later")
            return
        
        peoples_list = my_tools.text_to_list(peoples) if isinstance(peoples, str) else peoples
        if not peoples_list:
            voice.speak("There is an error in processing the data. Please try again later")
            return
        
        for people in peoples_list:
            people_type, people_id = my_tools.extract_integer_and_text(people)
            if people_type == 'nurse':
                find_person = db.nurses.get(people_id , None)
                if find_person:
                    voice.speak(f"{find_person.first_name} {find_person.last_name} is a nurse and only patients has the scheduling")
            elif people_type == 'patient':
                find_person = db.patients.get(people_id, None)
                if find_person:
                    selected_scheduleds = {"daily" : [] , "once" : []}
                    voice.speak(f"{find_person.first_name} {find_person.last_name} is a patient and has the scheduling." + "Here are the schedules of the patient")
                    for schedule_id, schedule in db.schedules.items():
                        if schedule.patient_id == people_id:
                            if schedule.is_daily:
                                selected_scheduleds['daily'].append(schedule)
                            else:
                                selected_scheduleds['once'].append(schedule)

                    # TODO : Create an algorithm that will say all the schedules of the person
                    
        # TODO : Create an algorithm that will say goodbye 
        return
    else :
        voice.speak(data.get('invalid', "I'm sorry but I can't find you in the database or you are not a nurse")) 
        return
    
    
    
    
def algo_check_body_temperature(
    event: EventHandler, 
    voice: VoiceUtils, 
    brain: BrainUtils, 
    data: dict, 
    arduino: ArduinoConnection
):
    # Prompt the user to begin body temperature scanning
    if event.stop_proccess:
        return
    
    voice.speak(data.get("message", "Please scan the body temperature using my machine's temperature sensor."))
    arduino.write("BODYTEMP".encode())

    # Initialize variables for collecting readings
    temps = []
    MAX_READINGS = 10
    TIMEOUT = 30  # Timeout in seconds
    start_time = time.time()

    while len(temps) < MAX_READINGS:
        if event.stop_proccess:
            return

        try:
            temp = arduino.read()  # Read data from Arduino
            if temp:
                # Check for termination signal
                if temp.strip().upper() == "DONE":
                    break

                # Validate and process temperature data
                temp = float(temp.strip())
                if 30.0 <= temp <= 45.0:  # Validate within human body temperature range
                    temps.append(temp)
                    print(f"Received temperature: {temp}°C")
                else:
                    print(f"Warning: Unusual temperature reading: {temp}°C")
            else:
                print("No data received, retrying...")

        except ValueError as e:
            print(f"Invalid temperature reading: {e}")

        # Handle timeout to prevent infinite loops
        if time.time() - start_time > TIMEOUT:
            print("Timeout: No valid readings received.")
            voice.speak("No valid temperature readings could be collected. Please try again.")
            return
        
        time.sleep(1)  # Short delay between read attempts

    # Ensure readings were collected
    if not temps:
        voice.speak("I couldn't detect any temperature data. Please ensure the sensor is working properly.")
        return

    # Compute average temperature
    avg_temp_celsius = sum(temps) / len(temps)
    avg_temp_fahrenheit = (avg_temp_celsius * 1.8) + 32

    # Generate the response message
    response_message = brain.generate_response(
        rules_for_temperature.format(temp1=avg_temp_celsius, temp2=avg_temp_fahrenheit)
    )
    voice.speak(
        response_message.get(
            "message", 
            f"The scanned body temperature is {avg_temp_celsius:.2f}°C and {avg_temp_fahrenheit:.2f}°F."
        )
    )

    return  # Successfully complete the process



def algo_user_want_to_talk(
    event : EventHandler , 
    voice : VoiceUtils ,  
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils ,  
    data : dict,
    user_command : str
    ):
    
    # 8. Senario in making the machine walk;
    # - The user will ask the machine to move.
    # - The machine will identify what position and where to go.
    # - The machine will move to the position and where to go.
    
    print("algo_user_want_to_talk")
    if event.stop_proccess:
        return {}
    
    past_conversation : list[str] = []
    
    user_conversation_placeholder = "\nUser Response : {conversation}"
    bot_conversation_placeholder = "\nYour Response : {conversation}"
    past_conversation.append(user_conversation_placeholder.format(conversation=user_command))
    bot_message = data.get("message", "Hello There! Could you repeat your request because i did not understand the message")
    past_conversation.append(bot_conversation_placeholder.format(conversation=bot_message))
    event.user_commands = []
    voice.speak(bot_message)
    
    while True:
        print("Inside of conversation while loop")
        start_time = time.time()  # Record the start time
        timeout = 180  # Timeout duration in seconds (3 minutes)
        if event.stop_proccess:
            return {}
        
        while event.is_recording or len(event.user_commands) < 1:
            time.sleep(0.5)
            if event.stop_proccess:
                return {}
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                print("3 minutes have passed, returning default response: {}")
                return {}  # Automatically return {} if timeout is exceeded
            print("Waiting for event to be recorded or user commands to be added")
        
        response = ".".join(event.user_commands)
        past_conversation.append(user_conversation_placeholder.format(conversation=response))
        event.user_commands = [] # reset user commands
        
        if event.stop_proccess:
            return {}
        
        print("Thinking about the response...")
        bot_response = brain.generate_response(rules_for_conversation % "".join(past_conversation))
        print("Response:", bot_response)
            
        if event.stop_proccess:
            return {}
        
        data : dict = my_tools.text_to_dictionary(bot_response)
        if not data:
            bot_response = brain.generate_cohere_response(command=rules_for_conversation % "".join(past_conversation), system=None)
            data : dict = my_tools.text_to_dictionary(bot_response)
            if not data:
                voice.speak("Sorry, there was a problem. Please try again later.")
                return {}
        
        bot_message = data.get("response" , None)
        if not bot_message:
            action = data.get("action", None)
            if action is not None:
                return data
            voice.speak("Sorry, there was a problem. Please try again later.")
            return {}
        
        
        
        past_conversation.append(user_conversation_placeholder.format(conversation=response))
        past_conversation.append(bot_conversation_placeholder.format(conversation=bot_message))
        voice.speak(bot_message)
        

def algo_user_command_not_exist(
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict,
    user_command : str
    ):
    
    voice.speak(data.get("message", "The command you are looking for does not exist. Please try again"))


def algo_close_the_back_of_the_machine(
    event : EventHandler , 
    voice : VoiceUtils ,  
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils ,  
    data : dict,
    user_command : str
    ):
    if event.stop_proccess:
        return
    
    
    voice.speak(data.get("message", "Wait, I will slowly close the pills drawers."))
    
    # TODO: Create a logic that connect arduino and close the back of the machine
    
    return



    



if __name__ == "__main__":
    pass
    
    


