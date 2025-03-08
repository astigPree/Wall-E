
from speech_recognition_utils import SpeechRecognitionUtils
from my_tools import text_to_dictionary , send_post_request, delete_schedule
from database_handler import DataHandler
from brain_utils import BrainUtils
from voice_utils import VoiceUtils
from events_handler import EventHandler
import algorithm_handler as algo
import rules
import static_generated_txt

import time
import threading
import random 
import asyncio
import sys   


# Set the event loop policy conditionally for Windows 
if sys.platform == 'win32': 
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
      
  
event = EventHandler()
database = DataHandler()
ear = SpeechRecognitionUtils()
brain = BrainUtils()
voice = VoiceUtils()


def start_listening():
    global ear  
    global voice
    global event
    try: 
        while not event.close_down:
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
        

def main():
    global event 
    if len(event.user_commands) > 0 and not event.has_important_event:
        # print("Starting to analyze the commands...")
        
        user_overall_commands = " ~ ".join(event.user_commands)
        # print("Applying commands : ", user_overall_commands)
        generated_response = brain.generate_response(rules.rule_for_identifiying_command % user_overall_commands)
        print("Generated response by gpt4free: ", generated_response)
        decided_command : dict = text_to_dictionary(generated_response)
        print("Generated response by gpt4free: ", decided_command)
        if not decided_command:
            generated_response = brain.generate_cohere_response(user_overall_commands , rules.rule_for_identifiying_command % user_overall_commands)
            print("Generated response by cohere: ", generated_response)
            decided_command : dict = text_to_dictionary(generated_response)
            print("Generated response by cohere: ", decided_command)
            
            
        if decided_command.get('action') == "2" or decided_command.get('action') == 2:
            # TODO: Simulate talking to the user based on it question
            print("This should be the user talking")
            decided_command = algo.algo_user_want_to_talk(
                event=event,
                voice=voice,
                brain=brain,
                recognizer=ear,
                data=decided_command,
                user_command=user_overall_commands
            )
        
        print("Decided command : ", decided_command)
        if not decided_command:
            voice.speak(random.choice(static_generated_txt.list_of_not_recognized_commands_text))
            event.user_commands = []
            return
        
        if decided_command.get('action') == "1" or decided_command.get('action') == 1:
            # TODO: Simulate the checking of body temperature
            print("Checking body temperature")
            algo.algo_check_body_temperature(
                event=event,
                voice=voice,
                brain=brain,
                data=decided_command,
                arduino=None
            )
        elif decided_command.get('action') == "3" or decided_command.get('action') == 3:
            # TODO: Simulate repeating the questions
            message = decided_command.get('message' , random.choice(static_generated_txt.list_of_not_recognized_commands_text))
            voice.speak(message)
        elif decided_command.get('action') == "4" or decided_command.get('action') == 4:
            # TODO: Simulate closing the back of the machine
            print("Closing the back of the machine")
            algo.algo_close_the_back_of_the_machine(
                event=event,
                voice=voice, 
                brain=brain,
                recognizer=ear,
                data=decided_command,
                user_command=user_overall_commands
            )

        
        event.user_commands = []
        
    else:
        data = send_post_request()
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
        








if __name__ == '__main__':
    threading.Thread(target=start_listening).start() # start listening in a separate thread
    try:
        while not event.close_down:
            main()
            time.sleep(.3)
    except KeyboardInterrupt:
        print("Interrupted by user.")
        event.close_down = True
    except Exception as e:
        event.close_down = True
        print(f"An error occurred: {e}")
    
    
