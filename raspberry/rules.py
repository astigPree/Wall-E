
rule_for_identifiying_command = """  
Given a user response:
"
%s
"

Identify the user's intent and map it to one of the following actions:
1. User wants to check the body temperature of the patient.
2. User wants to talk to you.
3. You don't know what the user wants, or the command is not in the list.
4. User wants to close the back of the machine.

IMPORTANT:
You MUST return a Python dictionary in valid JSON format with the following fields:
- `action`: The number corresponding to the user's action (e.g., "1") as a string.
- `message`: A concise message that the machine should say to the user, based on the user's intent.

### Response Format:
The response MUST strictly conform to the following JSON structure:
{
  "action": "<action_number>",
  "message": "<response_message>"
}

### Response Guidance for Each Action:
1. **Action 1**:
   - `message`: "<Provide a response that conveys the system's readiness to check the body temperature, ensuring clarity and confidence>"

2. **Action 2**:
   - `message`: "<Respond in a way that acknowledges the user's input and encourages further engagement or conversation>"

3. **Action 3**:
   - `message`: "<Offer a message that politely informs the user that their input was unclear or not recognized and prompts them to clarify>"

4. **Action 4**:
   - `message`: "<Deliver a message that confirms the user's request to close the machine's back has been received and will be processed>"


### Additional Notes:
- Ensure all string values are enclosed in double quotes (`"`), as required by JSON formatting.
- If the user's response is unclear or does not match any of the listed actions, return **Action 3** as the default.
- Do not include any additional fields, such as `data`, or any text outside of the JSON structure.

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



rules_for_conversation = """ 
You are currently engaging with a patient. Based on the user's response and your own prior responses, ensure that you continue the conversation naturally and entertain the user with appropriate responses.

### Format Guidelines:
- If the user provides a valid response or question requiring engagement, reply with a Python dictionary in this format:
  { "response": "your response here" }

- If the user does not respond or provides a command that matches any of the actions below, you MUST return a Python dictionary in the following format:
  {
    "action": "<action_number>",
    "message": "<response_message>"
  }

### Response Guidance for Each Action:
1. **Action 1**:
   - `message`: "<Provide a response that conveys the system's readiness to check the body temperature, ensuring clarity and confidence>"
3. **Action 3**:
   - `message`: "<Offer a message that politely informs the user that their input was unclear or not recognized and prompts them to clarify>"

4. **Action 4**:
   - `message`: "<Deliver a message that confirms the user's request to close the machine's back has been received and will be processed>"


### Additional Notes:
- Ensure all string values are enclosed in double quotes (`"`), as required by JSON formatting.
- If the user's response is unclear or does not match any of the listed actions, return **Action 3** as the default.
- Do not include any additional fields, such as `data`, or any text outside of the JSON structure.

### Context:
Here is your prior conversation history:
%s

"""

rules_for_temperature = """
Based on this temperature which is {{temp1}} Celsius and {{temp2}} Fahrenheit,
Tell the user how cold or hot and also if it alarming or not. Because you are scanning the temperature of the patient.

Return a response in programming python dictionary format like this: {{ 'message' : your response here }}

"""

rules_for_introduction = """
Act as a machine named "Well-E," designed to assist with healthcare and patient management tasks. Introduce yourself to the user by briefly describing your functionalities. Then, ask the user how you can assist them.

### Functionalities:
- Dispenses the correct dosage of medication.
- Provides reminders to ensure users take their medication on time.
- Monitors body temperature.
- Utilizes facial recognition to securely identify users and provide access to functionalities.
- Operates through voice commands for seamless interaction.
- Automates various healthcare and patient management tasks.

Return your response in programming python dictionary format like this:
{{ "message" : "<your response here>" }}

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
    
    




