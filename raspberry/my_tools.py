


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
            try:
                data_dict = json.loads(json_text)
                
                # Print the dictionary
                return data_dict
            except json.JSONDecodeError:
                print("Failed to parse JSON from the response")
                return None
        else:
            print("No match found")
            return None