
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, Liaobots, Free2GPT
import g4f.debug

g4f.debug.logging = True
g4f.debug.version_check = False

import time



class BrainUtils:
    
    # client = Client()
    client = Client(
        provider=RetryProvider([Free2GPT, Phind,  Liaobots], shuffle=False)
    )
    # model = "gpt-4o-mini"
    model = ""

    debounce = 2



    async def generate_response(self, command : str):
        """
        Generates a response based on the provided text.
        """
        # while True:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": command}],
            )
            self.debounce = 2 # Reset the delay
            # print(f"The response is: {response.choices[0].message.content}")
            return str(response.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(self.debounce)
            self.debounce  = self.debounce * self.debounce
            return await self.generate_response(command)
    








rule_for_identifiying_command = """
    You are a machine that is controlled by a user. Given a user response;
        "{text}"
    Identify what user want and return to me what action does user want.
    Here are the list of the action;
        1. User want the machine to walk.
        2. User want to open the back of the machine or add a pills in the machine.
        3. User want to request a pills or ask when the pills will be distributed.
        4. User want to add new schedule for the pills or add new patient.
        5. User want to check the body temperature of the patient.
        6. User want to talk to you.
        7. You don't know what user want or the command is not in the list.
        8. User want to close the back of the machine.
    
    IMPORTANT: 
        You MUST return to me a python dictionary that contains the following;
        - action: The action that user want for example; "1".
        - message: The message that user want to send to the machine.
        - data : Additional data based on the additional requirements.
        
        Here is the response MUST look like this dictionary and Don't add any further information or text outside the dictionary because i will parse it to dictionary;
            {{"action":"1","message":"message","data":"data"}}
        
            
            
    Here is the bases of message each action;
        1 = message value are message that "asking where to go" if there is no distance provided. If there is distance provided, the message should be like "successfully moved to the `distance` meters".
        2 = message value are message that "asking for verification of the face of the user if the user is a nurse/doctor/admin"
        3 = message value are message that "asking for verification of the face of the user if the user is a patient".
        4 = message value are message that "asking for verification of the face of the user if the user is a nurse/doctor/admin".
        5 = message value are message that "waiting for scanning the body temperature of the patient".
        6 = message value are message that "response or the answer of the user".
        7 = message value are message that "You don't know what user want or the command is not recognized".
        8 = message value are message that "closing the back of the machine".
"""








