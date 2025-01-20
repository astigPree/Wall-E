from events_handler import EventHandler
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from database_handler import DataHandler
from speech_recognition_utils import SpeechRecognitionUtils
from facial_recognition_utils import FacialRecognition
import time
from rules import *
import my_tools

SCANNING_FACIAL_RECOGNITION_TIMEOUT = 5 # seconds timeout in seconds for processing face recognition


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
    if event.stop_proccess:
        return
    
    response = None
    speech_recognizer_maximum_retry = 10
    brain_maximum_retry = 5
    
    name = data.get('name', '')
    message = data.get('message', "Can you provide your name so that I can recognize you")
    if not name:
        # If the name is not specified then the user will be talk the machine his name
        voice.speak(message)
        time.sleep(5)
        for retry in range(speech_recognizer_maximum_retry):
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
    
    convert_response_to_list = my_tools.text_to_list(response)
    if not convert_response_to_list:
        voice.speak("I'm sorry but I can't process right now because there was a problem processing the response. Please try again later")
        return
    
    voice.speak(data.get('message', 'Please face my camera so i can see you if you are a nurse'))
    
    # Scanning face recognition
    
    event.activate_scanning = True
    event.open_eyes = True
    # TODO : Create an algorithm that will scan the face of based on the data before procceding below
    
    
    if event.has_face_scanned and event.detect_nurse:
        voice.speak(data.get('success', "Wait i will open the back so you can put the pills in the machine"))
        event.activate_scanning = False 
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
    
    if not data :
        return None
     
    
    
    
    

if __name__ == "__main__":
    pass
    
    


