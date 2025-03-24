
from speech_recognition_utils import SpeechRecognitionUtils
from my_tools import text_to_dictionary , send_post_request, delete_schedule
from database_handler import DataHandler
from brain_utils import BrainUtils
from voice_utils import VoiceUtils
from events_handler import EventHandler
from facial_recognition_utils import FacialRecognition
import algorithm_handler as algo
import rules
import static_generated_txt
import my_tools

import time
import threading
import random 
import asyncio
import sys   


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
eyes = FacialRecognition()


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

            # TODO: Create an algorithm that check the schedule of the patients
            # TODO: This is an important event and it should check the patient face to verify before despensing pills
            # TODO: This is an important event and it should shout the patients name so they will be notified
            for schedule_id , schedule in database.schedules.items():
                print(schedule)
                
                if schedule_id in event.done_schedule:
                    print(f"Schedule {schedule_id} has already been executed")
                    threading.Thread(target=delete_schedule, args=(schedule_id,)).start() # delete the scheduled that already executed
                    continue
                
                if schedule_id in event.pending_schedule:
                    print(f"Schedule {schedule_id} is already in pending state")
                    continue
                
                if schedule.get('set_date' , None):
                    
                    date_sched = my_tools.check_date_status(schedule.get('set_date' )) 
                    print("Date scheduled is in the ", date_sched)
                    if date_sched == "Past":
                        # If the schedule is not current date, then we need to skip the action 
                        threading.Thread(target=delete_schedule, args=(schedule_id,)).start() # delete the scheduled that already executed
                        continue
                    
                if schedule.get('set_time', None):
                    
                    time_sched = my_tools.check_time_status(schedule.get('set_time') , OFFSET_MINUTE_TO_VALID)
                    
                    print("Time scheduled is in the ", time_sched)
                    
                    if time_sched == "Past": 
                        # If the schedule is not current time, then we need to skip the action
                        continue
                    if time_sched == "Future": 
                        # If the schedule is not current time, then we need to skip the action
                        continue
                
                
                
                
                patient_id = schedule.get('patient' , None)
                if patient_id is None:
                    print("Schedule has no patient_id")
                    continue
                
                print("Patients Database : ", database.patients)
                patient_data : dict = database.patients.get(str(patient_id))
                if not patient_data:
                    print(f"Patient {patient_id} not found in database")
                    continue
                
                if patient_id not in event.patients_to_take_medication:
                    print(f"Patient {patient_id} is not in list of patients to take medication, so adding it.")
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
            print("Starting the main event loop")
            print("These are the ids of the patiens to take medication : ", event.list_of_schedule_to_take)

        if len(event.list_of_schedule_to_take) < 1:
            # Do nothing if there are no schedules to take for the day
            return None

        event.has_important_event = True
        while len(event.list_of_schedule_to_take) > 0:
            schedule = event.list_of_schedule_to_take.pop(0)
            patient_id = schedule.get('patient' , None)
            if patient_id is None:
                print("Schedule has no patient_id")
                continue
            patient = database.patients.get(str(patient_id))
            if not patient:
                print(f"Patient {patient_id} not found in database")
                continue
            
            # TODO: Apply walking here using arduino
            voice.speak("Walking is currently not supported! Please wait for further updates")
            # Uncomment when the waling is implemented
            # schedule['color'] = patient.get('color' , 'RED')
            # if not algo.algo_machine_walk( event = event, eyes = eyes , voice = voice , recognizer=ear , brain = brain, arduino = None, data = schedule):
            #     # Faild to walk to the patient location
            #     print("Failed to walk to patient")
            #     message = my_tools.SMS_NOT_TAKEN_MEDICATION_TEXT.format(
            #         patient_name = patient.get('name' , 'No name'), 
            #         schedule_time = schedule.get('set_time' , 'No time'), 
            #         pill = schedule.get('pill' , 'No pill')
            #     )
            #     my_tools.send_message(message , patient.get('phone_number' , None))
            #     continue

            # Identify the face of the user before dropping the pills
            algo.algo_machine_drop_pills(event = event, database=database, voice = voice , brain = brain, recognizer = ear , arduino = None, eyes = eyes, data = schedule)
            
            message = my_tools.SMS_TAKEN_MEDICATION_TEXT.format(
                patient_name = patient.get('name' , 'No name'), 
                schedule_time = schedule.get('set_time' , 'No time'), 
                pill = schedule.get('pill' , 'No pill')
            )
            
            my_tools.send_message(message , patient.get('phone_number' , None))
            print("Sent message to patient")
        
        
        # TODO: Apply walking here using arduino going back to its original position
        
        event.has_important_event = False



if __name__ == '__main__': 
    generated_response = brain.generate_response(rules.rules_for_introduction)
    decided_command : dict = text_to_dictionary(generated_response)
    if not decided_command:
        generated_response = brain.generate_cohere_response(rules.rules_for_introduction , rules.rules_for_introduction)
        print("Generated response by cohere: ", generated_response)
        decided_command : dict = text_to_dictionary(generated_response)
        print("Generated response by cohere: ", decided_command)
    if isinstance(decided_command, dict):
        introduction = decided_command.get("message" , "Hello, I am Well-E, your advanced healthcare assistant. I am here to ensure you take the right dosage of your medication at the correct time, monitor your body temperature for your well-being, and securely recognize you using facial recognition. You can interact with me easily through voice commands, and I automate several healthcare and patient management tasks to make your life smoother. How may I assist you today?")
    else:
        introduction = "Hello, I am Well-E, your advanced healthcare assistant. I am here to ensure you take the right dosage of your medication at the correct time, monitor your body temperature for your well-being, and securely recognize you using facial recognition. You can interact with me easily through voice commands, and I automate several healthcare and patient management tasks to make your life smoother. How may I assist you today?"
    voice.speak(introduction)
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
    
    
