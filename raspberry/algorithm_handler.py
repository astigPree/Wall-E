from events_handler import EventHandler
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from database_handler import DataHandler
from speech_recognition_utils import SpeechRecognitionUtils
from facial_recognition_utils import FacialRecognition
import time
from rules import *
import my_tools

SCANNING_FACIAL_RECOGNITION_TIMEOUT = 50 # seconds timeout in seconds for processing face recognition  
COMPARING_FACIAL_RECOGNITION_TIMEOUT = 2 # number of tries to compare the face recognition
RECORDING_VOICE_TIMEOUT = 3 # number of tries to recording the voice recognition



async def algo_open_back_of_the_machine(
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
        response = await brain.generate_response(rule_for_identifiying_id_by_name.format(text=name , options=options)) 
        brain_maximum_retry -= 1
        
    # DATA : response = { 
    #       "data" : [ "patient-1", "nurse-1"], 
    #       "invalid" : "I'm sorry but I can't find you in the database"
    #       "success" : "Wait i will open the back of the machine "
    # }
    if not response:
        voice.speak("Im sorry for that but I can't find you in the database. Please try again later")
        return
    
    convert_response_to_list = my_tools.text_to_dictionary(response)
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
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict):
    
    # 8. Senario in making the machine walk;
    # - The user will ask the machine to move.
    # - The machine will identify what position and where to go.
    # - The machine will move to the position and where to go.
    
    
    speech_recognizer_maximum_retry = 10 # seconds timeout in seconds for processing speech recognition
    brain_maximum_retry = 5 # seconds timeout in seconds for processing brain recognition
    if event.stop_proccess:
        return
    
    
    
async def algo_check_for_schedules(
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
        response = await brain.generate_response(rule_for_identifiying_id_by_name.format(text=name , options=options)) 
        brain_maximum_retry -= 1
        
    # DATA : response = { 
    #       "data" : [ "patient-1", "nurse-1"], 
    #       "invalid" : "I'm sorry but I can't find the named in the database",
    #       "success" : "Here are the schedules for the pills"
    # }
    
    if not response:
        voice.speak("Im sorry for that but I can't find you in the database. Please try again later")
        return
    
    convert_response_to_list = my_tools.text_to_dictionary(response)
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
    
    
async def algo_check_body_temperature( 
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict,
    user_command : str
    ):
    # 7. Senario in checking body temperature (NURSEs);
    # - The user can get the body temperature of the patient by using the machine tools.
    # - The machine will identify the body temperature of the patient.
    # - The machine will display the body temperature of the patient and speak the body temperature of the patient.
    if event.stop_proccess:
        return
    
    
    voice.speak(data.get("message", "Please scan the body temperature using my machine tools body temperature sensor."))
    
    # TODO: Create a logic that connect arduino and raspberry pi using a wiring then get the body temperature from the arduino
    
    voice.speak("The body temperature of the patient is: 5 degrees")
    
    return



async def algo_user_want_to_talk(
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict,
    user_command : str
    ):
    
    # 8. Senario in making the machine walk;
    # - The user will ask the machine to move.
    # - The machine will identify what position and where to go.
    # - The machine will move to the position and where to go.
    
    if event.stop_proccess:
        return {}
    
    past_conversation : list[str] = []
    
    user_conversation_placeholder = "\nUser Response : {conversation}"
    bot_conversation_placeholder = "\nYour Response : {conversation}"
    past_conversation.append(user_conversation_placeholder.format(conversation=user_command))
    bot_message = data.get("message", "Hello There! Could you repeat your request because i did not understand the message")
    past_conversation.append(bot_conversation_placeholder.format(conversation=bot_message))
    
    voice.speak(bot_message)
    
    while True:
        response = ""
        for tries in range(RECORDING_VOICE_TIMEOUT):
            
            if event.stop_proccess:
                return {}
            
            response += recognizer.recognize_speech()
            
            if event.stop_proccess:
                return {}
            
            if response and tries > 2 :
                bot_response = await brain.generate_response(rules_for_converstaion.format(conversations=past_conversation.join("")))
                    
                if event.stop_proccess:
                    return {}
                
                data : dict = text_to_dictionary(bot_response)
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
                
                break

async def algo_user_command_not_exist(
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


async def algo_close_the_back_of_the_machine(
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
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
    
    


