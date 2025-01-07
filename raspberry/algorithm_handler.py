from events_handler import EventHandler
from voice_utils import VoiceUtils


def algo_open_backe_of_the_machine(event : EventHandler , voice : VoiceUtils):
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
    
    
    
    


