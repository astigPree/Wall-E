


import json
import re
import requests
import os

SERVER_URL = "http://WellE.pythonanywhere.com"

def send_post_request():
    try:
        url = SERVER_URL + '/controller'  # Replace with your actual URL
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'controller_token': '1234567890'  # Replace with your actual token
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.ok:
            return response.json()
        else:
            print(f'Server responded with status: {response.status_code}')
            print(f'Error: {response.json()}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None
 

def fetch_and_save_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        
        if response.status_code == 200:
            if not os.path.isfile(save_path):
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Image saved to {save_path}")
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

# Example usage
# image_url = 'http://example.com/image.jpg'  # Replace with your actual image URL
# save_path = 'path/to/save/image.jpg'  # Replace with your desired save path
# fetch_and_save_image(image_url, save_path)


def extract_filename(url):
    pattern = r'/([^/]+)$'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# Example usage
# url = 'http://example.com/media/nurse_faces/nurse_image.jpg'
# filename = extract_filename(url)
# print(filename)  # Output: nurse_image.jpg


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
        

def text_to_list(text):
    # Find the list within the text
    match = re.search(r'\[.*?\]', text)
    if match:
        # Extract the list text
        list_text = match.group(0)
        
        # Convert the list text to a Python list
        try:
            return json.loads(list_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON from the list")
            return None
    else:
        print("No list found in the text")
        return None

# Example usage
# text = "List ['{\"name\": \"John\"}', 'Hello', '{\"age\": 30}']"
# result = extract_and_convert_list(text)
# print(result)  # Output: ['{"name": "John"}', 'Hello', '{"age": 30}']
 

def extract_integer(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group(0))
    else:
        return None

# Example usage
# text = "patient-1"
# integer = extract_integer(text)
# print(integer)  # Output: 1


def extract_integer_and_text(text):
    match = re.search(r'(\D+)-(\d+)', text)
    if match:
        text_part = match.group(1)
        integer_part = int(match.group(2))
        return text_part, integer_part
    else:
        return None, None

# Example usage
# text = "patient-1"
# text_part, integer_part = extract_integer_and_text(text)
# print(f"Text: {text_part}, Integer: {integer_part}")  # Output: Text: patient, Integer: 1
