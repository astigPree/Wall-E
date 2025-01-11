from speech_recognition_utils import SpeechRecognitionUtils
from voice_utils import VoiceUtils
from brain_utils import *
from facial_recognition_utils import FacialRecognition
from events_handler import EventHandler
from database_handler import DataHandler
from my_tools import text_to_dictionary
from algorithm_handler import algo_open_back_of_the_machine

import asyncio
import sys
import time
import threading
import os

# Set the event loop policy conditionally for Windows 
if sys.platform == 'win32': 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



database = DataHandler()
eyes = FacialRecognition()
voice = VoiceUtils()
recognizer = SpeechRecognitionUtils()
brain = BrainUtils()
event =  EventHandler()


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


def eyes_loop():
    while not event.close_down:
        
        if not event.open_eyes:
            continue
        
        
        frame = eyes.get_face_by_camera()
        if frame is not None:
            
            if event.detect_nurse:
                people = database.get_nurses()
            elif event.detect_patient:
                people = database.get_patients()
            else :
                people = database.get_all_people()
            
            for person in people:
                
                event.has_face_scanned = eyes.check_face_exists_in_database(frame, event.selected_face)
                
                if event.has_face_scanned:
                    # TODO: Create a logic here
                    print("Face recognized")
                else:
                    print("Face not recognized")
                
        time.sleep(0.5)


async def main_loop():
    
    # threading.Thread(target=eyes_loop).start() # For facial recognition
    
    while not event.close_down: 
        text = recognizer.recognize_speech()
        if text:
            response = await brain.generate_response(rule_for_identifiying_command.format(text=text))
            print(f"The response is: {response}")
            data : dict = text_to_dictionary(response)
            if data is not None:
                # data = { action , message, data }
                if data.get('action') == '2' or data.get('action') == 2:
                    algo_open_back_of_the_machine(
                        event=event, voice=voice, 
                        db=database, brain=brain, 
                        recognizer=recognizer, eyes=eyes, 
                        data=data
                    )

            
        await asyncio.sleep(0.5)  # Add a short delay between iterations
    
    
    
    

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
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
