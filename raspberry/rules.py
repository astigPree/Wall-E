
rule_for_identifiying_command = """
You are a machine controlled by a user. Given a user response "{text}", identify what the user wants and return to me what action the user wants. Here are the list of actions:

1. User wants the machine to walk.
2. User wants to open the back of the machine or add pills in the machine.
3. User wants to request a pill or ask when the pill will be distributed.
4. User wants to add a new schedule for the pills or add a new patient.
5. User wants to check the body temperature of the patient.
6. User wants to talk to you.
7. You don't know what the user wants or the command is not in the list.
8. User wants to close the back of the machine.

IMPORTANT:
You MUST return to me a Python dictionary containing the following:
- action: The action that the user wants (e.g., "1").
- message: The message that the machine should say to the user.
- data: Additional data based on the additional requirements.

Here is the response MUST look like this dictionary and don't add any further information or text outside the dictionary because I will parse it to a dictionary:
{{"action": action based on the user response ,"message": message based on the user response, "data": data based on the below data required for the action}}

Here is the example message for each action and don't copy it directly into the dictionary, it's just for reference:
1. message value should reference the example "How many distance you want me to move?" if there is no distance provided. If there is a distance provided, the message should reference "Successfully moved to the `distance` meters".
2. message value should reference the example "Could you please tell me your name?".
3. message value should reference the example "Could you please tell me your name?".
4. message value should reference the example "Could you please tell me your name?".
5. message value should reference the example "I'm waiting to scan the patient's body temperature".
6. message value should reference the example "Got it, thanks for letting me know!".
7. message value should reference the example "I'm not sure what you want or the command isn't recognized".
8. message value should reference the example "Alright, I'm closing the back of the machine now".
 
The dictionary should look like this but not copy it directly into the dictionary, it's just for reference:
{{"action": "1", "message": "Successfully moved to the `distance` meters", "data": {{"distance": "10" , "type": "meters"}}}}

Here is the example for the data:
1. data value should reference the example "distance": "10" , "type": "meters" if the distance is provided by the user and if not provided by the user then the data should be "None".
2. data value should reference the example "name": "John Doe".
3. data value should reference the example "name": "John Doe".
4. data value should reference the example "name": "John Doe".
5. data value should reference the example "celcius" : "Your temperature is {{cel}} celcius" , "fahrenheit" : "Your temperature is {{fah}} fahrenheit".
6. data value should reference the example "message": "Got it, thanks for letting me know!".
7. data value should reference the example "message": "I'm not sure what you want or the command isn't recognized".

"""






if __name__ == "__main__":
    
    from brain_utils import BrainUtils
    from my_tools import *
    import asyncio
    
    brain = BrainUtils()
    
    async def main_loop():
     
         
        text = input("Enter your text: ")
        if text:
            print(rule_for_identifiying_command.format(text=text))
            response = await brain.generate_response(rule_for_identifiying_command.format(text=text))
            print(f"The response is: {response}") 
            print(f"To object : {text_to_dictionary(response)}")
            
        await asyncio.sleep(0.5)
        
        await main_loop()
        
    try:
        asyncio.run(main_loop())
    except Exception as e:
        print(f"An error occurred: {e}")
    
    




