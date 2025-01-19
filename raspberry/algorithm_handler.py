from events_handler import EventHandler
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from database_handler import DataHandler
from speech_recognition_utils import SpeechRecognitionUtils
from facial_recognition_utils import FacialRecognition
import time

SCANNING_FACIAL_RECOGNITION_TIMEOUT = 5 # seconds timeout in seconds for processing face recognition


def algo_open_back_of_the_machine(
    event : EventHandler , 
    voice : VoiceUtils , 
    db : DataHandler, 
    brain : BrainUtils, 
    recognizer : SpeechRecognitionUtils , 
    eyes : FacialRecognition, 
    data : dict):
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
    
    voice.speak(data.get('message', 'Please face my eyes so i can see you if you are a nurse'))
    
    
    

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
    pass
    
    
    
    
    
    

if __name__ == "__main__":
    pass
    
    


