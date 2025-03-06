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
event =  EventHandler()
arduino = ArduinoConnection()
# arduino.initialized() 
eyes.start_camera()
