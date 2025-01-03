import asyncio
from speech_recognition_utils import SpeechRecognitionUtils
from voice_utils import VoiceUtils
from brain_utils import BrainUtils
from facial_recognition_utils import FacialRecognition
from events_handler import EventHandler
import sys
import time
import threading

# Set the event loop policy conditionally for Windows 
if sys.platform == 'win32': 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())




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
    while True:
        
        if not event.open_eyes:
            continue
        
        
        frame = eyes.get_face_by_camera()
        if frame is not None:
            frame = eyes.check_face_exists_in_database(frame, "face.jpg")
            if frame:
                event.has_face_scanned = True
                # TODO: Create a logic here
                print("Face recognized")
            else:
                print("Face not recognized")
                
        time.sleep(0.5)


async def main_loop():
    
    threading.Thread(target=eyes_loop).start()
    
    while True:
        pass
    
    
    
    

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Safely close the event loop
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                loop.close()
        except RuntimeError as re:
            print(f"Error closing event loop: {re}")
