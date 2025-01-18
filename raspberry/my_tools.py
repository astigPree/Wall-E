


import json
import re
import requests

def send_post_request():
    url = 'http://127.0.0.1:8000/controller'  # Replace with your actual URL
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        'controller_token': '1234567890'  # Replace with your actual token
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.ok:
        print(response.json())
    else:
        print(f'Server responded with status: {response.status_code}')
        print(f'Error: {response.json()}')

# Example usage
send_post_request()



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