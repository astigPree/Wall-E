
rule_for_identifiying_command = """ 
You are a machine controlled by a user. Given a user response "{text}", identify what the user wants and return to me what action the user wants. Here are the list of actions:

1. User wants to check the body temperature of the patient.
2. User wants to talk to you.
3. You don't know what the user wants or the command is not in the list.
4. User wants to close the back of the machine.

IMPORTANT:
You MUST return to me a Python dictionary containing the following:
- action: The action that the user wants (e.g., "1").
- message: The message that the machine should say to the user.
- data: Additional data based on the additional requirements.

Here is the response MUST look like this dictionary and don't add any further information or text outside the dictionary because I will parse it to a dictionary:
{{"action": action based on the user response ,"message": message based on the user response, "data": data based on the below data required for the action}}

Here is the example message for each action and don't copy it directly into the dictionary, it's just for reference:
1. message value should reference the example saying the user that you are waiting for the temperature to be scanned.
2. message value should reference the example responding to the user inquiries/questions or text.
3. message value should reference the example responding to the user inquiries/questions or text.
4. message value should reference the example saying that you will close the back of the machine.

The dictionary should look like this but not copy it directly into the dictionary, it's just for reference:
{{"action": "1", "message": "Your temperature is {{cel}} Celsius. Your temperature is {{fah}} Fahrenheit.", "data": {{"celsius" : "{{cel}}", "fahrenheit": "{{fah}}"}}}}

Here is the example for the data:
1. data value should reference the example "celsius" : "{{cel}}", "fahrenheit": "{{fah}}".
2. data value should reference the example "message": "Got it, thanks for letting me know!".
3. data value should reference the example "message": "I'm not sure what you want or the command isn't recognized".
4. it does not contain any value. 
"""

rule_for_identifiying_id_by_name = """
Based on this text who are the person the text want to find and give me a list of id based on the available options:
Text: "{text}"

Available options:
    "{options}"

Return a list of id based on the available options like this [ "1", "2", "3"].

For example:
    text = "My name is John"
    options :
        patient-1 : John Smith
        nurses-2 : Jane Doe
        patient-3 : Jill Doe
    The output will be: ["patient-1"]    
"""



rules_for_converstaion = """ 
You are currently talking to a patient and based on the user response and your response. Make sure to continue responding to the user response and entertain the user.

You should return a response in programming python dictionary format like this: {{ 'response' : your response here }}

If the user does not respond or the response is a command that is listed below;
1. User wants to check the body temperature of the patient.
2. User wants to talk to you.
3. You don't know what the user wants or the command is not in the list.
4. User wants to close the back of the machine.
Then you should return the corresponding number of the command below for example like this: {{"action": action based on the user response ,"message": message based on the user response}} based on the list of commands

Now here is your past conversations; 
{conversations}
"""

rules_for_temperature = """
Based on this temperature which is {{temp1}} Celsius and {{temp2}} Fahrenheit,
Tell the user how cold or hot and also if it alarming or not. Because you are scanning the temperature of the patient.

Return a response in programming python dictionary format like this: {{ 'message' : your response here }}

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
    
    




