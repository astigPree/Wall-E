


import json
import re
import requests

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
    response = requests.get(image_url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {save_path}")
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")

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