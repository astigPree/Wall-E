from speech_recognition_utils import SpeechRecognitionUtils
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from facial_recognition_utils import FacialRecognition
from events_handler import EventHandler
from database_handler import DataHandler
from my_tools import text_to_dictionary
from algorithm_handler import algo_open_back_of_the_machine
import rules

import asyncio
import sys
import time
import threading
import os

# Set the event loop policy conditionally for Windows 
if sys.platform == 'win32': 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



database = DataHandler()
# eyes = FacialRecognition()
voice = VoiceUtils()
# recognizer = SpeechRecognitionUtils()
brain = BrainUtils()
event =  EventHandler()



async def main_loop(): 
    text = input("Enter user response : ")

    # if text:
    #     response = await brain.generate_response(rules.rule_for_identifiying_id_by_name.format(text=text , options=options))
    #     print(f"The response is: {response}")
    #     data : dict = text_to_dictionary(response)
    #     if data is not None:
    #         # data = { action , message, data }
    #         if data.get('action') == '2' or data.get('action') == 2:
    #             algo_open_back_of_the_machine(
    #                 event=event, voice=voice, 
    #                 db=database, brain=brain, 
    #                 recognizer=None, eyes=None, 
    #                 data=data
    #             ) 
    
    
    
    

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
    except Exception as e:
        print(f"An error occurred: {e}")
        event.close_down = True
        # eyes.close_camera()
    finally:
        event.close_down = True
        # Safely close the event loop
        try:
            # eyes.close_camera()
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                loop.close()
        except RuntimeError as re:
            print(f"Error closing event loop: {re}")
            # eyes.close_camera()
