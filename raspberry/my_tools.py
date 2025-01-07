


import json
import re


def text_to_dictionary(response : str):
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r'\{.*?\}', response) 
        if match:
            # Extracted text
            json_text = match.group(0)
            
            # Convert to dictionary
            data_dict = json.loads(json_text)
            
            # Print the dictionary
            print(data_dict)
            return data_dict
        else:
            print("No match found")
            return None